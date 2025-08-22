# downloader.py
"""
DownloaderCore - handles Streamlink download operations and stream state management.
Separated from UI so it can be reused in CLI or automated scripts.
"""

import os
import subprocess
import threading
import time
from datetime import datetime

class DownloaderCore:
    def __init__(self, logger=None, ui_updater=None, status_callback=None):
        """
        :param logger: Logger instance or object with log_to_console() & log_streamlink() methods
        :param ui_updater: function(name) to refresh UI treeview item
        :param status_callback: function(message) to update status bar
        """
        self.log = logger.log_to_console if logger else print
        self.log_streamlink = logger.log_streamlink if logger else print
        self.update_tree_item = ui_updater if ui_updater else lambda name: None
        self.update_status = status_callback if status_callback else lambda msg: None

        self.streams = {}
        self.output_folder = os.path.join(os.path.expanduser("~"), "Documents", "YTS", "M3U8")
        os.makedirs(self.output_folder, exist_ok=True)
        self.selected_quality = "best"

        # Compression settings
        self.compression_enabled = False
        self.compression_preset = "medium"  # ultrafast, superfast, veryfast, faster, fast, medium, slow, slower, veryslow
        self.compression_crf = 23  # 0-51, lower = better quality, higher = smaller file
        self.compression_audio_bitrate = "128k"  # Audio bitrate for compression

    def add_stream(self, name, url, delay=1, test_url_callback=None):
        """Add a stream to the active downloads list"""
        if name in self.streams:
            self.log(f"Stream already exists: {name}")
            return False

        # Optional URL test
        if test_url_callback and not url.startswith('file://') and not os.path.exists(url):
            if not test_url_callback(url):
                self.log(f"Warning: URL may not be accessible: {url}")

        self.streams[name] = {
            'url': url,
            'process': None,
            'state': 'Stopped',
            'delay': delay,
            'restart_timer': None,
            'restart_seconds': 0,
            'retry_count': 0,
            'last_error_time': None,
            'backoff_level': 0
        }
        self.log(f"Added stream: {name}")
        return True

    def get_selected_streams(self, names):
        """Filter streams from given names list"""
        return [n for n in names if n in self.streams]

    def start_stream(self, name):
        """Start a single stream"""
        if self.streams[name]['state'] == 'Running':
            return
        if not self.check_streamlink_available():
            self.log("Streamlink not available.")
            return
        if self.compression_enabled and not self.check_ffmpeg_available():
            self.log("Compression enabled but FFmpeg not available. Please install FFmpeg.")
            return
        self._start_stream_internal(name)

    def stop_stream(self, name):
        """Stop a running stream"""
        self.log(f"Stopping stream: {name}")

        # Cancel restart
        if self.streams[name]['restart_timer']:
            self.streams[name]['restart_timer'].cancel() if hasattr(self.streams[name]['restart_timer'], 'cancel') \
                else None
            self.streams[name]['restart_timer'] = None

        proc = self.streams[name]['process']
        if proc:
            try:
                self.log_streamlink(f"[{name}] Terminating process...")
                
                # Stop streamlink process if compression is enabled
                if self.compression_enabled and 'streamlink_proc' in self.streams[name]:
                    streamlink_proc = self.streams[name]['streamlink_proc']
                    try:
                        streamlink_proc.terminate()
                        streamlink_proc.wait(timeout=3)
                    except subprocess.TimeoutExpired:
                        streamlink_proc.kill()
                        streamlink_proc.wait()
                    except Exception as e:
                        self.log_streamlink(f"[{name}] Error stopping streamlink: {e}")
                
                # Stop main process
                proc.terminate()
                try:
                    proc.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    self.log_streamlink(f"[{name}] Force killing process...")
                    proc.kill()
                    proc.wait()
                self.log_streamlink(f"[{name}] Process stopped")
            except Exception as e:
                self.log_streamlink(f"[{name}] Error stopping process: {e}")

        self.streams[name]['state'] = 'Stopped'
        self.streams[name]['process'] = None
        self.streams[name]['restart_seconds'] = 0
        self.update_tree_item(name)
        self.log(f"Stream stopped: {name}")

    def restart_stream(self, name):
        """Restart a stream after stopping it"""
        self.stop_stream(name)
        threading.Timer(2, lambda: self._start_stream_internal(name)).start()

    def set_delay(self, name, delay):
        """Set restart delay for a stream in minutes"""
        self.streams[name]['delay'] = max(0, delay)
        self.update_tree_item(name)

    def set_compression_settings(self, enabled, preset="medium", crf=23, audio_bitrate="128k"):
        """Set compression settings"""
        self.compression_enabled = enabled
        self.compression_preset = preset
        self.compression_crf = crf
        self.compression_audio_bitrate = audio_bitrate
        self.log(f"Compression settings updated: enabled={enabled}, preset={preset}, crf={crf}, audio={audio_bitrate}")

    def _start_stream_internal(self, name):
        """Actual start & monitoring logic"""
        def run():
            try:
                url = self.streams[name]['url']
                quality = self.selected_quality
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

                safe_name = ''.join(c for c in name if c.isalnum() or c in (' ', '-', '_')).rstrip()
                folder = os.path.join(self.output_folder, safe_name)
                os.makedirs(folder, exist_ok=True)
                output = os.path.join(folder, f"{safe_name}_{timestamp}.mp4")

                self.log(f"Starting stream: {name} -> {output}")
                self.log_streamlink(f"[{name}] Starting download with quality: {quality}")

                if self.compression_enabled:
                    self.log_streamlink(f"[{name}] Compression enabled: preset={self.compression_preset}, crf={self.compression_crf}")
                    # Use FFmpeg for real-time compression
                    cmd = [
                        'streamlink', '--loglevel', 'info', '--force',
                        '--retry-streams', '3', '--retry-max', '3',
                        '--stdout', url, quality
                    ]
                    # Pipe to FFmpeg for compression
                    ffmpeg_cmd = [
                        'ffmpeg', '-i', 'pipe:0',
                        '-c:v', 'libx264', '-preset', self.compression_preset,
                        '-crf', str(self.compression_crf),
                        '-c:a', 'aac', '-b:a', self.compression_audio_bitrate,
                        '-y', output
                    ]
                    self.log_streamlink(f"[{name}] FFmpeg command: {' '.join(ffmpeg_cmd)}")
                else:
                    # Standard download without compression
                cmd = [
                    'streamlink', '--loglevel', 'info', '--force',
                    '--retry-streams', '3', '--retry-max', '3',
                    url, quality, '-o', output
                ]

                if self.compression_enabled:
                    # Create piped process: streamlink | ffmpeg
                    streamlink_proc = subprocess.Popen(
                        cmd,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True,
                        bufsize=1,
                        universal_newlines=True
                    )
                    
                    ffmpeg_proc = subprocess.Popen(
                        ffmpeg_cmd,
                        stdin=streamlink_proc.stdout,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True,
                        bufsize=1,
                        universal_newlines=True
                    )
                    
                    # Close streamlink stdout in parent process
                    streamlink_proc.stdout.close()
                    
                    # Use ffmpeg process as main process
                    proc = ffmpeg_proc
                    self.streams[name]['streamlink_proc'] = streamlink_proc
                else:
                proc = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1,
                    universal_newlines=True
                )

                self.streams[name]['process'] = proc
                self.streams[name]['state'] = 'Running'
                self.update_tree_item(name)

                def log_output():
                    try:
                        while proc.poll() is None:
                            line = proc.stdout.readline()
                            if line:
                                self.log_streamlink(f"[{name}] {line.strip()}")
                            else:
                                time.sleep(0.1)
                        
                        # Log stderr for compression mode
                        if self.compression_enabled and hasattr(self.streams[name], 'streamlink_proc'):
                            streamlink_proc = self.streams[name]['streamlink_proc']
                            if streamlink_proc.stderr:
                                streamlink_stderr = streamlink_proc.stderr.read()
                                if streamlink_stderr:
                                    for line in streamlink_stderr.splitlines():
                                        self.log_streamlink(f"[{name}] [Streamlink] {line.strip()}")
                        
                        # flush remaining output
                        remaining_output = proc.stdout.read()
                        if remaining_output:
                            for line in remaining_output.splitlines():
                                self.log_streamlink(f"[{name}] {line.strip()}")
                    except Exception as e:
                        self.log_streamlink(f"[{name}] Logging error: {e}")

                threading.Thread(target=log_output, daemon=True).start()

                return_code = proc.wait()
                if return_code == 0:
                    self.log_streamlink(f"[{name}] Download completed successfully")
                    self.log(f"Download completed: {name}")
                    # Reset retry count on successful completion
                    self.reset_retry_count(name)
                else:
                    self.log_streamlink(f"[{name}] Download failed - code: {return_code}")
                    self.log(f"Download failed: {name} (code: {return_code})")
                    # Schedule error retry with progressive backoff
                    if self.streams[name]['delay'] > 0:
                        self.schedule_restart(name, is_error_retry=True)

                self.streams[name]['state'] = 'Stopped'
                self.streams[name]['process'] = None
                self.update_tree_item(name)

                # Only schedule normal restart if not already scheduled for error retry
                if self.streams[name]['delay'] > 0 and return_code == 0:
                    self.schedule_restart(name)

            except Exception as e:
                err = f"Error starting stream {name}: {e}"
                self.log(err)
                self.log_streamlink(f"[{name}] {err}")
                self.streams[name]['state'] = 'Stopped'
                self.streams[name]['process'] = None
                self.update_tree_item(name)

        threading.Thread(target=run, daemon=True).start()

    def calculate_retry_delay(self, name):
        """Calculate dynamic retry delay based on error pattern"""
        stream = self.streams[name]
        retry_count = stream['retry_count']
        
        # Progressive backoff schedule
        backoff_schedule = [30, 60, 120, 300, 600, 1800]  # 30s, 1m, 2m, 5m, 10m, 30m
        max_backoff = 1800  # 30 minutes max
        
        if retry_count < len(backoff_schedule):
            base_delay = backoff_schedule[retry_count]
        else:
            base_delay = max_backoff
        
        # Add random jitter (±10% of base delay)
        import random
        jitter = random.uniform(-0.1, 0.1) * base_delay
        final_delay = max(5, base_delay + jitter)  # Minimum 5 seconds
        
        return int(final_delay)

    def reset_retry_count(self, name):
        """Reset retry count when stream starts successfully"""
        if name in self.streams:
            self.streams[name]['retry_count'] = 0
            self.streams[name]['backoff_level'] = 0
            self.log(f"Reset retry count for {name}")

    def schedule_restart(self, name, is_error_retry=False):
        """Schedule restart with dynamic delay"""
        if is_error_retry:
            # Error-based retry with progressive backoff
            delay_seconds = self.calculate_retry_delay(name)
            self.streams[name]['retry_count'] += 1
            self.log(f"Scheduling error retry for {name} in {delay_seconds}s (attempt {self.streams[name]['retry_count']})")
        else:
            # Normal scheduled restart
        delay_seconds = self.streams[name]['delay'] * 60
            self.log(f"Scheduling normal restart for {name} in {delay_seconds}s")
        
        self.streams[name]['restart_seconds'] = delay_seconds
        self.streams[name]['state'] = 'Restarting'
        self.update_tree_item(name)

        def countdown():
            if name not in self.streams or self.streams[name]['state'] != 'Restarting':
                return
            self.streams[name]['restart_seconds'] -= 1
            self.update_tree_item(name)
            if self.streams[name]['restart_seconds'] <= 0:
                self._start_stream_internal(name)
            else:
                self.streams[name]['restart_timer'] = threading.Timer(1, countdown)
                self.streams[name]['restart_timer'].start()

        countdown()

    def check_streamlink_available(self):
        """Check if Streamlink CLI is installed and accessible"""
        try:
            result = subprocess.run(['streamlink', '--version'],
                                    capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                self.log(f"Streamlink available: {result.stdout.strip()}")
                return True
            else:
                self.log("Streamlink not working properly")
                return False
        except Exception as e:
            self.log(f"Error checking Streamlink: {e}")
            return False

    def check_ffmpeg_available(self):
        """Check if FFmpeg is installed and accessible"""
        try:
            result = subprocess.run(['ffmpeg', '-version'],
                                    capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                self.log(f"FFmpeg available: {result.stdout.split()[2]}")
                return True
            else:
                self.log("FFmpeg not working properly")
                return False
        except Exception as e:
            self.log(f"Error checking FFmpeg: {e}")
            return False

    def update_download_progress(self, name, output_file):
        """Log current file size for a running download"""
        try:
            if os.path.exists(output_file):
                size = self.get_file_size(output_file)
                self.log_streamlink(f"[{name}] Current file size: {size}")
        except Exception as e:
            self.log_streamlink(f"[{name}] Progress error: {e}")

    def get_file_size(self, file_path):
        """Human-readable file size"""
        try:
            size = os.path.getsize(file_path)
            for unit in ['B', 'KB', 'MB', 'GB']:
                if size < 1024.0:
                    return f"{size:.1f} {unit}"
                size /= 1024.0
            return f"{size:.1f} TB"
        except Exception:
            return "Unknown"

    def test_stream_url(self, url):
        """Quickly check if Streamlink can handle URL"""
        try:
            result = subprocess.run(['streamlink', '--can-handle-url', url],
                                    capture_output=True, text=True, timeout=30)
            return result.returncode == 0
        except Exception as e:
            self.log(f"Error testing URL {url}: {e}")
            return False

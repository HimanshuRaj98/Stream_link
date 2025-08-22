# video_tools.py
"""
VideoTools - utility functions for video file operations
such as merging MP4 files into a single video using FFmpeg.
"""

import os
import subprocess

class VideoTools:
    def __init__(self, logger=None, status_updater=None, file_picker=None, messagebox=None):
        """
        :param logger: function for logging messages (e.g., print or UI log)
        :param status_updater: function to update UI status label
        :param file_picker: function to select a folder (UI-specific)
        :param messagebox: UI messagebox module (optional)
        """
        self.log = logger if logger else print
        self.update_status = status_updater if status_updater else lambda msg: None
        self.pick_folder = file_picker
        self.mb = messagebox

    def merge_videos(self, folder=None):
        """
        Merge multiple MP4 files in a folder into a single video using ffmpeg.
        If folder is not provided, and file_picker is set, prompts user for one.
        """
        # Ask for folder if not provided
        if folder is None:
            if self.pick_folder:
                folder = self.pick_folder()
            else:
                raise ValueError("No folder provided and no picker available")

        if not folder:
            return

        try:
            original_dir = os.getcwd()
            os.chdir(folder)

            mp4_files = [f for f in os.listdir(folder) if f.lower().endswith('.mp4')]
            if not mp4_files:
                msg = "No .mp4 files found in the selected folder."
                self.update_status(msg)
                if self.mb:
                    self.mb.showerror("Error", msg)
                return

            mp4_files.sort()
            output_name = os.path.splitext(mp4_files[0])[0] + "_.mp4"
            self.update_status(f"Found {len(mp4_files)} MP4 files. Starting merge...")
            self.log(f"Video Tools: Starting merge of {len(mp4_files)} files")

            # Write input list for ffmpeg
            with open("input.txt", "w", encoding='utf-8') as f:
                for file in mp4_files:
                    f.write(f"file '{file}'\n")

            # Merge with ffmpeg
            try:
                self.update_status("Merging videos with FFmpeg...")
                subprocess.run(
                    ["ffmpeg", "-f", "concat", "-safe", "0", "-i", "input.txt", "-c", "copy", output_name],
                    capture_output=True,
                    text=True,
                    check=True
                )
                msg = f"Videos merged successfully: {output_name}"
                self.log(f"Video Tools: {msg}")
                self.update_status(msg)
                if self.mb:
                    self.mb.showinfo("Success", msg)

            except subprocess.CalledProcessError as e:
                err_msg = f"FFmpeg Error: Failed to merge videos.\n{e}"
                if e.stderr:
                    err_msg += f"\n\nFFmpeg Output:\n{e.stderr}"
                self.update_status(err_msg)
                self.log(f"Video Tools: {err_msg}")
                if self.mb:
                    self.mb.showerror("FFmpeg Error", err_msg)
                return

            except FileNotFoundError:
                err_msg = "FFmpeg not found. Please install FFmpeg and ensure it's in your system PATH."
                self.update_status(err_msg)
                self.log(f"Video Tools: {err_msg}")
                if self.mb:
                    self.mb.showerror("FFmpeg Not Found", err_msg)
                return

            except Exception as e:
                err_msg = f"Unexpected error during video merge: {str(e)}"
                self.update_status(err_msg)
                self.log(f"Video Tools: {err_msg}")
                if self.mb:
                    self.mb.showerror("Error", err_msg)
                return

        finally:
            # Cleanup
            if os.path.exists("input.txt"):
                os.remove("input.txt")
            try:
                os.chdir(original_dir)
            except Exception:
                pass

# app.py
"""
Streamlink Downloader - Aero Edition (Complete Modular)
Application entry point with all modular UI tabs
"""
import tkinter as tk
from tkinter import ttk

# Import AeroStyle directly
from aero_style import AeroStyle

from ui.ui_base import BaseUI
from ui.ui_main_tab import MainTab
from ui.ui_log_tab import LogTab
from ui.ui_csv_tools_tab import CSVToolsTab
from ui.ui_settings_tab import SettingsTab
from ui.ui_handlers import UIHandlers

from downloader import DownloaderCore
from csv_tools import CSVTools
from video_tools import VideoTools
from logger import Logger

class StreamlinkDownloader(BaseUI):
    def __init__(self):
        super().__init__()
        
        # Setup window
        self.setup_window()
        self.create_status_bar()
        
        # Initialize modules
        self.init_modules()
        
        # Setup UI tabs
        self.setup_tabs()
        
        # Setup event bindings
        self.setup_event_bindings()
        
        # Start animation and logging
        self.animate_startup()
        self.logger.log_to_console(f"Application started. Output folder: {self.output_folder}")

    def init_modules(self):
        """Initialize all modules"""
        # Initialize logger first
        self.logger = Logger(
            status_updater=self.update_status,
            app_log_widget=None,  # Will be set when log tab is created
            streamlink_log_widget=None
        )

        # Initialize downloader
        self.downloader = DownloaderCore(
            logger=self.logger,
            ui_updater=self.update_tree_item,
            status_callback=self.update_status
        )
        self.downloader.output_folder = self.output_folder
        self.downloader.selected_quality = self.selected_quality.get()
        
        # Initialize compression settings
        self.downloader.set_compression_settings(
            enabled=self.compression_enabled.get(),
            preset=self.compression_preset.get(),
            crf=self.compression_crf.get(),
            audio_bitrate=self.compression_audio_bitrate.get()
        )

        # Initialize CSV tools
        self.csv_tools = CSVTools(
            logger=self.logger.log_to_console,
            status_updater=self.update_status
        )

        # Initialize video tools
        from tkinter import filedialog, messagebox
        self.video_tools = VideoTools(
            logger=self.logger.log_to_console,
            status_updater=self.update_status,
            file_picker=lambda: filedialog.askdirectory(title="Select folder with MP4 files"),
            messagebox=messagebox
        )

        # Initialize handlers
        self.handlers = UIHandlers(self, self.downloader, self.logger)

    def setup_tabs(self):
        """Setup tab control and individual tabs"""
        # Main container
        main_container = self.components.create_glass_frame(self.root)
        main_container.pack(fill='both', expand=True, padx=10, pady=10)

        # Title bar
        self.create_title_bar(main_container)

        # Tab control
        self.tab_control = ttk.Notebook(main_container, style='Aero.TNotebook')
        
        # Create tab frames
        self.main_tab_frame = self.components.create_glass_frame(self.tab_control)
        self.log_tab_frame = self.components.create_glass_frame(self.tab_control)
        self.csv_tools_tab_frame = self.components.create_glass_frame(self.tab_control)
        self.settings_tab_frame = self.components.create_glass_frame(self.tab_control)

        # Add tabs to notebook
        self.tab_control.add(self.main_tab_frame, text='📺 Main')
        self.tab_control.add(self.log_tab_frame, text='📋 Log')
        self.tab_control.add(self.csv_tools_tab_frame, text='📊 CSV & Video Tools')
        self.tab_control.add(self.settings_tab_frame, text='⚙️ Settings')
        
        self.tab_control.pack(fill='both', expand=True, padx=5, pady=5)

        # Initialize individual tab modules
        self.main_tab = MainTab(self.main_tab_frame, self, self.downloader, self.logger)
        self.log_tab = LogTab(self.log_tab_frame, self, self.logger)
        self.csv_tools_tab = CSVToolsTab(self.csv_tools_tab_frame, self, self.csv_tools, self.video_tools)
        self.settings_tab = SettingsTab(self.settings_tab_frame, self, self.logger)

    def create_title_bar(self, parent):
        """Create title bar with enhanced styling"""
        title_frame = self.components.create_glass_frame(parent)
        title_frame.pack(fill='x', padx=5, pady=(5, 10))

        # Create gradient-like effect for title - Fixed AeroStyle reference
        title_bg = tk.Frame(title_frame, bg=AeroStyle.ACCENT_LIGHT_BLUE, height=50)
        title_bg.pack(fill='x')
        title_bg.pack_propagate(False)

        title_content = tk.Frame(title_bg, bg=AeroStyle.ACCENT_LIGHT_BLUE)
        title_content.pack(expand=True)

        title_label = self.components.create_styled_label(
            title_content,
            "🎬 Streamlink Downloader",
            style='header'
        )
        title_label.config(
            font=('Segoe UI', 18, 'bold'),
            bg=AeroStyle.ACCENT_LIGHT_BLUE,
            fg=AeroStyle.ACCENT_DARK_BLUE
        )
        title_label.pack(side='left', pady=12)

        subtitle_label = self.components.create_styled_label(
            title_content,
            "Aero Edition - Complete Modular",
            style='secondary'
        )
        subtitle_label.config(bg=AeroStyle.ACCENT_LIGHT_BLUE)
        subtitle_label.pack(side='left', padx=(10, 0), pady=12)

    def setup_event_bindings(self):
        """Setup event bindings for keyboard shortcuts"""
        # Keyboard shortcuts
        self.root.bind('<Control-o>', lambda e: self.main_tab.load_csv())
        self.root.bind('<Control-s>', lambda e: self.main_tab.save_download_list())
        self.root.bind('<Control-l>', lambda e: self.main_tab.load_download_list())
        self.root.bind('<F5>', lambda e: self.refresh_streams())
        self.root.bind('<Delete>', lambda e: self.handlers.remove_stream())

    def update_tree_item(self, name):
        """Update tree item display for a stream"""
        if hasattr(self.main_tab, 'tree'):
            for item in self.main_tab.tree.get_children():
                if self.main_tab.tree.item(item)['text'] == name:
                    stream = self.downloader.streams[name]
                    state = stream['state']
                    delay = stream['delay']
                    restart_time = stream.get('restart_seconds', 0)
                    self.main_tab.tree.item(item, values=(state, delay, restart_time), tags=(state,))
                    break

    def refresh_streams(self):
        """Refresh stream display"""
        for name in self.downloader.streams:
            self.update_tree_item(name)

    def run(self):
        """Start the main application loop"""
        self.root.mainloop()

def main():
    app = StreamlinkDownloader()
    app.run()

if __name__ == "__main__":
    main()

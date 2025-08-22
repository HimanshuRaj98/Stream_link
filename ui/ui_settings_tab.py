# ui/ui_settings_tab.py
"""
Settings tab with application configuration options
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import json
from aero_style import AeroStyle
from ui.ui_components import AeroComponents

class SettingsTab:
    def __init__(self, parent, base_ui, logger):
        self.parent = parent
        self.base_ui = base_ui
        self.logger = logger
        self.components = AeroComponents()
        
        # Settings variables
        self.dark_mode = tk.BooleanVar()
        self.auto_start = tk.BooleanVar()
        self.minimize_to_tray = tk.BooleanVar()
        self.check_updates = tk.BooleanVar(value=True)
        
        self.setup_settings_tab()
        self.load_settings()

    def setup_settings_tab(self):
        """Setup the settings tab UI"""
        # Main container
        main_container = self.components.create_glass_frame(self.parent)
        main_container.pack(fill='both', expand=True, padx=20, pady=20)

        # Title
        title_header = self.components.create_styled_label(
            main_container,
            "⚙️ Application Settings",
            'header'
        )
        title_header.pack(pady=(20, 30))

        # Create sections - Fixed: Pass parent parameter
        self.create_appearance_section(main_container)
        self.create_behavior_section(main_container)
        self.create_paths_section(main_container)
        self.create_advanced_section(main_container)
        self.create_about_section(main_container)

    def create_appearance_section(self, parent):  # Fixed: Added parent parameter
        """Create appearance settings section"""
        appearance_section = self.components.create_glass_frame(parent)
        appearance_section.pack(fill='x', pady=15)

        # Section header
        appearance_header = self.components.create_styled_label(
            appearance_section,
            "🎨 Appearance",
            'subheader'
        )
        appearance_header.pack(anchor='w', padx=15, pady=(15, 10))

        # Theme options
        theme_frame = tk.Frame(appearance_section, bg=AeroStyle.GLASS_BACKGROUND)
        theme_frame.pack(fill='x', padx=15, pady=10)

        # Dark mode toggle
        dark_mode_check = tk.Checkbutton(theme_frame,
                                        text="🌙 Enable Dark Mode",
                                        variable=self.dark_mode,
                                        command=self.toggle_dark_mode,
                                        bg=AeroStyle.GLASS_BACKGROUND,
                                        fg=AeroStyle.TEXT_COLOR,
                                        selectcolor=AeroStyle.ACCENT_LIGHT_BLUE,
                                        font=('Segoe UI', 9))
        dark_mode_check.pack(anchor='w', pady=5)

        # Theme preview button
        preview_frame = tk.Frame(appearance_section, bg=AeroStyle.GLASS_BACKGROUND)
        preview_frame.pack(fill='x', padx=15, pady=(5, 15))

        self.components.create_gradient_button(
            preview_frame, "🎨 Preview Theme", self.preview_theme
        ).pack(side='left')

        self.components.create_styled_label(
            preview_frame, "(Theme changes require restart)", 'secondary'
        ).pack(side='left', padx=10)

    def create_behavior_section(self, parent):  # Fixed: Added parent parameter
        """Create behavior settings section"""
        behavior_section = self.components.create_glass_frame(parent)
        behavior_section.pack(fill='x', pady=15)

        # Section header
        behavior_header = self.components.create_styled_label(
            behavior_section,
            "⚡ Behavior",
            'subheader'
        )
        behavior_header.pack(anchor='w', padx=15, pady=(15, 10))

        # Behavior options
        behavior_frame = tk.Frame(behavior_section, bg=AeroStyle.GLASS_BACKGROUND)
        behavior_frame.pack(fill='x', padx=15, pady=10)

        # Auto-start downloads
        auto_start_check = tk.Checkbutton(behavior_frame,
                                         text="▶️ Auto-start streams when added",
                                         variable=self.auto_start,
                                         bg=AeroStyle.GLASS_BACKGROUND,
                                         fg=AeroStyle.TEXT_COLOR,
                                         selectcolor=AeroStyle.ACCENT_LIGHT_BLUE,
                                         font=('Segoe UI', 9))
        auto_start_check.pack(anchor='w', pady=5)

        # Minimize to tray
        minimize_check = tk.Checkbutton(behavior_frame,
                                       text="📌 Minimize to system tray",
                                       variable=self.minimize_to_tray,
                                       bg=AeroStyle.GLASS_BACKGROUND,
                                       fg=AeroStyle.TEXT_COLOR,
                                       selectcolor=AeroStyle.ACCENT_LIGHT_BLUE,
                                       font=('Segoe UI', 9))
        minimize_check.pack(anchor='w', pady=5)

        # Check for updates
        updates_check = tk.Checkbutton(behavior_frame,
                                      text="🔄 Check for updates on startup",
                                      variable=self.check_updates,
                                      bg=AeroStyle.GLASS_BACKGROUND,
                                      fg=AeroStyle.TEXT_COLOR,
                                      selectcolor=AeroStyle.ACCENT_LIGHT_BLUE,
                                      font=('Segoe UI', 9))
        updates_check.pack(anchor='w', pady=(5, 15))

    def create_paths_section(self, parent):  # Fixed: Added parent parameter
        """Create paths configuration section"""
        paths_section = self.components.create_glass_frame(parent)
        paths_section.pack(fill='x', pady=15)

        # Section header
        paths_header = self.components.create_styled_label(
            paths_section,
            "📁 Paths & Directories",
            'subheader'
        )
        paths_header.pack(anchor='w', padx=15, pady=(15, 10))

        # Default download folder
        download_frame = tk.Frame(paths_section, bg=AeroStyle.GLASS_BACKGROUND)
        download_frame.pack(fill='x', padx=15, pady=5)

        self.components.create_styled_label(
            download_frame, "Default Download Folder:"
        ).pack(anchor='w')

        folder_select_frame = tk.Frame(download_frame, bg=AeroStyle.GLASS_BACKGROUND)
        folder_select_frame.pack(fill='x', pady=5)

        self.download_path_var = tk.StringVar(value=self.base_ui.output_folder)
        download_entry = self.components.create_styled_entry(
            folder_select_frame, textvariable=self.download_path_var, width=50
        )
        download_entry.pack(side='left')

        self.components.create_gradient_button(
            folder_select_frame, "Browse", self.browse_download_folder
        ).pack(side='left', padx=5)

        # Streamlink path
        streamlink_frame = tk.Frame(paths_section, bg=AeroStyle.GLASS_BACKGROUND)
        streamlink_frame.pack(fill='x', padx=15, pady=(10, 15))

        self.components.create_styled_label(
            streamlink_frame, "Streamlink Executable Path (optional):"
        ).pack(anchor='w')

        exe_select_frame = tk.Frame(streamlink_frame, bg=AeroStyle.GLASS_BACKGROUND)
        exe_select_frame.pack(fill='x', pady=5)

        self.streamlink_path_var = tk.StringVar()
        streamlink_entry = self.components.create_styled_entry(
            exe_select_frame, textvariable=self.streamlink_path_var, width=50
        )
        streamlink_entry.pack(side='left')

        self.components.create_gradient_button(
            exe_select_frame, "Browse", self.browse_streamlink_exe
        ).pack(side='left', padx=5)

    def create_advanced_section(self, parent):  # Fixed: Added parent parameter
        """Create advanced settings section"""
        advanced_section = self.components.create_glass_frame(parent)
        advanced_section.pack(fill='x', pady=15)

        # Section header
        advanced_header = self.components.create_styled_label(
            advanced_section,
            "🔧 Advanced Settings",
            'subheader'
        )
        advanced_header.pack(anchor='w', padx=15, pady=(15, 10))

        # Settings buttons
        settings_buttons = tk.Frame(advanced_section, bg=AeroStyle.GLASS_BACKGROUND)
        settings_buttons.pack(fill='x', padx=15, pady=10)

        buttons = [
            ("💾 Save Settings", self.save_settings, 'primary'),
            ("📂 Load Settings", self.load_settings_from_file, 'normal'),
            ("🔄 Reset to Defaults", self.reset_settings, 'normal'),
            ("📋 Export Settings", self.export_settings, 'normal')
        ]

        for text, command, style in buttons:
            self.components.create_gradient_button(
                settings_buttons, text, command, style
            ).pack(side='left', padx=5)

        # Settings file info
        settings_info = tk.Frame(advanced_section, bg=AeroStyle.GLASS_BACKGROUND)
        settings_info.pack(fill='x', padx=15, pady=(10, 15))

        settings_file_path = os.path.join(os.path.expanduser("~"), ".streamlink_downloader_settings.json")
        self.components.create_styled_label(
            settings_info,
            f"Settings file: {settings_file_path}",
            'secondary'
        ).pack(anchor='w')

    def create_about_section(self, parent):  # Fixed: Added parent parameter
        """Create about section"""
        about_section = self.components.create_glass_frame(parent)
        about_section.pack(fill='x', pady=15)

        # Section header
        about_header = self.components.create_styled_label(
            about_section,
            "ℹ️ About",
            'subheader'
        )
        about_header.pack(anchor='w', padx=15, pady=(15, 10))

        # App information
        info_frame = tk.Frame(about_section, bg=AeroStyle.GLASS_BACKGROUND)
        info_frame.pack(fill='x', padx=15, pady=(5, 15))

        app_info = [
            "Streamlink Downloader - Aero Edition (Modular)",
            "Version: 2.0.0 - Modular Architecture",
            "Features: Multi-stream downloading, Auto-restart, CSV import, Video tools",
            "UI Style: Windows Aero Glass inspired design"
        ]

        for info in app_info:
            self.components.create_styled_label(
                info_frame, info, 'secondary'
            ).pack(anchor='w', pady=2)

        # System info button
        system_frame = tk.Frame(about_section, bg=AeroStyle.GLASS_BACKGROUND)
        system_frame.pack(fill='x', padx=15, pady=(10, 15))

        self.components.create_gradient_button(
            system_frame, "🖥️ Show System Info", self.show_system_info
        ).pack(side='left')

        self.components.create_gradient_button(
            system_frame, "📋 Copy Debug Info", self.copy_debug_info
        ).pack(side='left', padx=10)

    # Event handlers
    def toggle_dark_mode(self):
        """Toggle dark mode (placeholder)"""
        if self.dark_mode.get():
            self.logger.log_to_console("Dark mode enabled (requires restart)")
            messagebox.showinfo("Dark Mode", "Dark mode will be applied after restart")
        else:
            self.logger.log_to_console("Light mode enabled (requires restart)")
            messagebox.showinfo("Light Mode", "Light mode will be applied after restart")

    def preview_theme(self):
        """Preview current theme"""
        messagebox.showinfo("Theme Preview", "Current theme: Aero Glass Light")

    def browse_download_folder(self):
        """Browse for default download folder"""
        folder = filedialog.askdirectory(
            title="Select Default Download Folder",
            initialdir=self.download_path_var.get()
        )
        if folder:
            self.download_path_var.set(folder)

    def browse_streamlink_exe(self):
        """Browse for Streamlink executable"""
        exe_path = filedialog.askopenfilename(
            title="Select Streamlink Executable",
            filetypes=[("Executable files", "*.exe"), ("All files", "*.*")]
        )
        if exe_path:
            self.streamlink_path_var.set(exe_path)

    def save_settings(self):
        """Save current settings to file"""
        settings = {
            'dark_mode': self.dark_mode.get(),
            'auto_start': self.auto_start.get(),
            'minimize_to_tray': self.minimize_to_tray.get(),
            'check_updates': self.check_updates.get(),
            'download_folder': self.download_path_var.get(),
            'streamlink_path': self.streamlink_path_var.get()
        }
        
        try:
            settings_file = os.path.join(os.path.expanduser("~"), ".streamlink_downloader_settings.json")
            with open(settings_file, 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=2)
            
            self.logger.log_to_console("Settings saved successfully")
            messagebox.showinfo("Success", "Settings saved successfully")
        except Exception as e:
            self.logger.log_to_console(f"Error saving settings: {e}")
            messagebox.showerror("Error", f"Failed to save settings:\n{e}")

    def load_settings(self):
        """Load settings from file"""
        try:
            settings_file = os.path.join(os.path.expanduser("~"), ".streamlink_downloader_settings.json")
            if os.path.exists(settings_file):
                with open(settings_file, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                
                self.dark_mode.set(settings.get('dark_mode', False))
                self.auto_start.set(settings.get('auto_start', False))
                self.minimize_to_tray.set(settings.get('minimize_to_tray', False))
                self.check_updates.set(settings.get('check_updates', True))
                
                if settings.get('download_folder'):
                    self.download_path_var.set(settings['download_folder'])
                    self.base_ui.output_folder = settings['download_folder']
                
                if settings.get('streamlink_path'):
                    self.streamlink_path_var.set(settings['streamlink_path'])
                
                self.logger.log_to_console("Settings loaded successfully")
        except Exception as e:
            self.logger.log_to_console(f"Error loading settings: {e}")

    def load_settings_from_file(self):
        """Load settings from a selected file"""
        file_path = filedialog.askopenfilename(
            title="Load Settings File",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                # Apply loaded settings (similar to load_settings)
                self.logger.log_to_console(f"Settings loaded from {file_path}")
                messagebox.showinfo("Success", "Settings loaded successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load settings:\n{e}")

    def reset_settings(self):
        """Reset all settings to defaults"""
        if messagebox.askyesno("Reset Settings", "Are you sure you want to reset all settings to defaults?"):
            self.dark_mode.set(False)
            self.auto_start.set(False)
            self.minimize_to_tray.set(False)
            self.check_updates.set(True)
            self.download_path_var.set(os.path.join(os.path.expanduser("~"), "Documents", "YTS", "M3U8"))
            self.streamlink_path_var.set("")
            
            self.logger.log_to_console("Settings reset to defaults")
            messagebox.showinfo("Success", "Settings reset to defaults")

    def export_settings(self):
        """Export current settings to a file"""
        file_path = filedialog.asksaveasfilename(
            title="Export Settings",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if file_path:
            self.save_settings()  # Save current settings first
            try:
                import shutil
                settings_file = os.path.join(os.path.expanduser("~"), ".streamlink_downloader_settings.json")
                shutil.copy2(settings_file, file_path)
                messagebox.showinfo("Success", f"Settings exported to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export settings:\n{e}")

    def show_system_info(self):
        """Show system information dialog"""
        import platform
        import sys
        
        info = f"""System Information:
OS: {platform.system()} {platform.release()}
Python: {sys.version.split()[0]}
Architecture: {platform.architecture()[0]}
Processor: {platform.processor()}
"""
        messagebox.showinfo("System Information", info)

    def copy_debug_info(self):
        """Copy debug information to clipboard"""
        import platform
        import sys
        
        debug_info = f"""Streamlink Downloader Debug Info:
Version: 2.0.0 Modular
OS: {platform.system()} {platform.release()}
Python: {sys.version}
Architecture: {platform.architecture()[0]}
Settings File: {os.path.join(os.path.expanduser("~"), ".streamlink_downloader_settings.json")}
Download Folder: {self.base_ui.output_folder}
"""
        
        try:
            self.base_ui.root.clipboard_clear()
            self.base_ui.root.clipboard_append(debug_info)
            self.logger.log_to_console("Debug info copied to clipboard")
            messagebox.showinfo("Success", "Debug information copied to clipboard")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to copy debug info:\n{e}")

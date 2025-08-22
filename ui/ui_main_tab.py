# ui/ui_main_tab.py
"""
Main tab with stream management functionality
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import os
import csv
import json
import platform
import subprocess
from aero_style import AeroStyle
from ui.ui_components import AeroComponents

class MainTab:
    def __init__(self, parent, base_ui, downloader, logger):
        self.parent = parent
        self.base_ui = base_ui
        self.downloader = downloader
        self.logger = logger
        self.components = AeroComponents()
        
        self.setup_main_tab()

    def setup_main_tab(self):
        """Setup the main tab UI"""
        # Control panel
        control_panel = self.components.create_glass_frame(self.parent)
        control_panel.pack(fill='x', padx=10, pady=(10, 5))

        self.create_top_controls(control_panel)
        self.create_output_display()
        self.create_search_controls()
        self.create_content_area()



    def create_top_controls(self, parent):
        """Create top control buttons and settings"""
        top_controls = tk.Frame(parent, bg=AeroStyle.GLASS_BACKGROUND)
        top_controls.pack(fill='x', padx=10, pady=10)

        # Left side controls
        left_controls = tk.Frame(top_controls, bg=AeroStyle.GLASS_BACKGROUND)
        left_controls.pack(side='left', fill='x', expand=True)

        self.components.create_gradient_button(
            left_controls, "📁 Load CSV", self.load_csv, 'primary'
        ).pack(side='left')
        
        self.components.create_gradient_button(
            left_controls, "➕ Add Link", self.add_manual_link, 'primary'
        ).pack(side='left', padx=5)

        self.csv_label = self.components.create_styled_label(
            left_controls, "No CSV loaded", 'secondary'
        )
        self.csv_label.pack(side='left', padx=15)

        # Center controls
        center_controls = tk.Frame(top_controls, bg=AeroStyle.GLASS_BACKGROUND)
        center_controls.pack(side='left', padx=15)

        self.components.create_gradient_button(
            center_controls, "📂 Set Output", self.set_output_folder
        ).pack(side='left')
        
        self.components.create_gradient_button(
            center_controls, "📁 Show Folder", self.show_output_folder
        ).pack(side='left', padx=5)

        # Right side controls - ensure they stay visible
        self.create_right_controls(top_controls)

    def create_right_controls(self, parent):
        """Create delay and quality controls"""
        right_controls = tk.Frame(parent, bg=AeroStyle.GLASS_BACKGROUND)
        right_controls.pack(side='right')

        # Default delay setting
        delay_frame = tk.Frame(right_controls, bg=AeroStyle.GLASS_BACKGROUND)
        delay_frame.pack(side='left', padx=5)

        self.components.create_styled_label(
            delay_frame, "Default Delay (min):"
        ).pack(side='left')

        delay_entry = self.components.create_styled_entry(
            delay_frame, textvariable=self.base_ui.default_delay, width=5
        )
        delay_entry.pack(side='left', padx=5)

        # Quality selector
        quality_frame = tk.Frame(right_controls, bg=AeroStyle.GLASS_BACKGROUND)
        quality_frame.pack(side='left', padx=15)

        self.components.create_styled_label(quality_frame, "Quality:").pack(side='left')

        quality_combo = ttk.Combobox(quality_frame,
                                   textvariable=self.base_ui.selected_quality,
                                   values=["best", "720p", "480p", "360p", "160p"],
                                   width=8,
                                   style='Aero.TCombobox',
                                   state='readonly')
        quality_combo.pack(side='left', padx=5)

        # Compression controls
        compression_frame = tk.Frame(right_controls, bg=AeroStyle.GLASS_BACKGROUND)
        compression_frame.pack(side='left', padx=15)

        # Compression checkbox
        compression_check = tk.Checkbutton(
            compression_frame,
            text="🗜️ Compress",
            variable=self.base_ui.compression_enabled,
            bg=AeroStyle.GLASS_BACKGROUND,
            fg=AeroStyle.TEXT_COLOR,
            selectcolor=AeroStyle.ACCENT_LIGHT_BLUE,
            font=('Segoe UI', 9),
            command=self.update_compression_controls
        )
        compression_check.pack(side='left')

        # Compression preset
        preset_frame = tk.Frame(compression_frame, bg=AeroStyle.GLASS_BACKGROUND)
        preset_frame.pack(side='left', padx=5)

        self.components.create_styled_label(preset_frame, "Preset:").pack(side='left')

        preset_combo = ttk.Combobox(preset_frame,
                                   textvariable=self.base_ui.compression_preset,
                                   values=["ultrafast", "superfast", "veryfast", "faster", "fast", "medium", "slow", "slower", "veryslow"],
                                   width=8,
                                   style='Aero.TCombobox',
                                   state='readonly')
        preset_combo.pack(side='left', padx=2)

        # CRF slider frame
        crf_frame = tk.Frame(compression_frame, bg=AeroStyle.GLASS_BACKGROUND)
        crf_frame.pack(side='left', padx=5)

        self.components.create_styled_label(crf_frame, "CRF:").pack(side='left')

        crf_scale = tk.Scale(crf_frame,
                            from_=18, to=28,
                            orient='horizontal',
                            variable=self.base_ui.compression_crf,
                            bg=AeroStyle.GLASS_BACKGROUND,
                            fg=AeroStyle.TEXT_COLOR,
                            highlightthickness=0,
                            length=60,
                            showvalue=True,
                            font=('Segoe UI', 8))
        crf_scale.pack(side='left', padx=2)

        # Compression info tooltip
        info_label = self.components.create_styled_label(
            compression_frame, "ℹ️", 'secondary'
        )
        info_label.pack(side='left', padx=5)
        self.create_tooltip(info_label, 
            "Compression reduces file size during download:\n"
            "• Preset: Speed vs quality trade-off\n"
            "• CRF: 18-23 (high quality), 24-28 (smaller files)\n"
            "• Requires FFmpeg to be installed")

    def create_output_display(self):
        """Create output folder display"""
        output_frame = self.components.create_glass_frame(self.parent)
        output_frame.pack(fill='x', padx=10, pady=5)

        self.output_label = self.components.create_styled_label(
            output_frame,
            f"📁 Output: {self.base_ui.output_folder}",
            anchor='w'
        )
        self.output_label.config(fg=AeroStyle.ACCENT_BLUE)
        self.output_label.pack(fill='x', padx=10, pady=8)

    def create_search_controls(self):
        """Create search and action buttons"""
        search_frame = self.components.create_glass_frame(self.parent)
        search_frame.pack(fill='x', padx=10, pady=5)

        search_controls = tk.Frame(search_frame, bg=AeroStyle.GLASS_BACKGROUND)
        search_controls.pack(fill='x', padx=10, pady=10)

        # Search
        self.components.create_styled_label(
            search_controls, "🔍 Search:", 'subheader'
        ).pack(side='left')

        self.base_ui.search_var.trace('w', self.filter_streams)
        search_entry = self.components.create_styled_entry(
            search_controls, textvariable=self.base_ui.search_var, width=35
        )
        search_entry.pack(side='left', padx=10)
        
        # Add right-click paste functionality to search entry
        search_entry.bind('<Button-3>', self.show_search_context_menu)
        
        # Create search context menu
        self.search_context_menu = tk.Menu(search_entry, tearoff=0)
        self.search_context_menu.add_command(label="📋 Paste", command=lambda: self.paste_to_search(search_entry))
        self.search_context_menu.add_command(label="📋 Copy", command=lambda: self.copy_from_search(search_entry))
        self.search_context_menu.add_command(label="✂️ Cut", command=lambda: self.cut_from_search(search_entry))

        # Action buttons
        self.create_action_buttons(search_controls)
        self.create_save_load_buttons(search_controls)

    def create_action_buttons(self, parent):
        """Create stream action buttons"""
        buttons_frame = tk.Frame(parent, bg=AeroStyle.GLASS_BACKGROUND)
        buttons_frame.pack(side='left', padx=15)

        buttons = [
            ("➕ Add Selected", self.add_selected, 'primary'),
            ("▶️ Start Selected", self.start_stream, 'normal'),
            ("⏹️ Stop Selected", self.stop_stream, 'normal'),
            ("🗑️ Remove Selected", self.remove_stream, 'normal')
        ]

        for text, command, style in buttons:
            self.components.create_gradient_button(
                buttons_frame, text, command, style
            ).pack(side='left', padx=5)

    def create_save_load_buttons(self, parent):
        """Create save/load buttons"""
        save_load_frame = tk.Frame(parent, bg=AeroStyle.GLASS_BACKGROUND)
        save_load_frame.pack(side='right', padx=15)

        self.components.create_gradient_button(
            save_load_frame, "💾 Save List", self.save_download_list
        ).pack(side='left', padx=5)
        
        self.components.create_gradient_button(
            save_load_frame, "📂 Load List", self.load_download_list
        ).pack(side='left', padx=5)

    def create_content_area(self):
        """Create main content area with trees"""
        content_frame = self.components.create_glass_frame(self.parent)
        content_frame.pack(fill='both', expand=True, padx=10, pady=10)

        splitter = tk.PanedWindow(content_frame,
                                 orient='horizontal',
                                 sashrelief='flat',
                                 sashwidth=8,
                                 bg=AeroStyle.BORDER_COLOR)
        splitter.pack(fill='both', expand=True, padx=5, pady=5)

        # Left panel - Available streams
        left_panel = self.components.create_glass_frame(splitter)
        right_panel = self.components.create_glass_frame(splitter)
        splitter.add(left_panel, stretch='always')
        splitter.add(right_panel, stretch='always')

        self.create_csv_tree(left_panel)
        self.create_download_tree(right_panel)

    def create_csv_tree(self, parent):
        """Create CSV streams tree"""
        header = self.components.create_styled_label(
            parent, "📺 Available Streams", 'subheader'
        )
        header.pack(anchor='w', padx=10, pady=(10, 5))

        tree_container = tk.Frame(parent, bg=AeroStyle.GLASS_BACKGROUND)
        tree_container.pack(fill='both', expand=True, padx=10, pady=(0, 10))

        self.csv_tree = self.components.create_styled_treeview(
            tree_container, columns=('URL',)
        )
        self.csv_tree.heading('#0', text='📁 Name')
        self.csv_tree.heading('URL', text='🔗 URL')
        self.csv_tree.column('#0', width=300)
        self.csv_tree.column('URL', width=450)

        # Scrollbar
        csv_scrollbar = ttk.Scrollbar(tree_container, orient='vertical', 
                                     command=self.csv_tree.yview)
        csv_scrollbar.pack(side='right', fill='y')
        self.csv_tree.configure(yscrollcommand=csv_scrollbar.set)
        self.csv_tree.pack(side='left', fill='both', expand=True)

        # Bind double-click
        self.csv_tree.bind('<Double-1>', self.on_csv_double_click)

    def create_download_tree(self, parent):
        """Create active downloads tree"""
        header = self.components.create_styled_label(
            parent, "⬇️ Active Downloads", 'subheader'
        )
        header.pack(anchor='w', padx=10, pady=(10, 5))

        tree_container = tk.Frame(parent, bg=AeroStyle.GLASS_BACKGROUND)
        tree_container.pack(fill='both', expand=True, padx=10, pady=(0, 10))

        self.tree = self.components.create_styled_treeview(
            tree_container, columns=('State', 'Delay', 'Restart', 'Retries')
        )
        
        # Configure headers with sorting
        self.tree.heading('#0', text='📁 Name', 
                         command=lambda: self.sort_tree_column('#0', False))
        self.tree.heading('State', text='⚡ State',
                         command=lambda: self.sort_tree_column('State', False))
        self.tree.heading('Delay', text='⏰ Delay (min)',
                         command=lambda: self.sort_tree_column('Delay', False))
        self.tree.heading('Restart', text='🔄 Restart (s)',
                         command=lambda: self.sort_tree_column('Restart', False))
        self.tree.heading('Retries', text='🔄 Retries',
                         command=lambda: self.sort_tree_column('Retries', False))

        # Configure columns
        self.tree.column('#0', width=200)
        self.tree.column('State', width=80)
        self.tree.column('Delay', width=80)
        self.tree.column('Restart', width=80)
        self.tree.column('Retries', width=60)

        # Configure tags for state colors
        self.tree.tag_configure('Running', foreground='white', 
                               background=AeroStyle.SUCCESS_COLOR)
        self.tree.tag_configure('Restarting', foreground='white',
                               background=AeroStyle.WARNING_COLOR)
        self.tree.tag_configure('Stopped', foreground='white',
                               background=AeroStyle.ERROR_COLOR)

        # Scrollbar
        tree_scrollbar = ttk.Scrollbar(tree_container, orient='vertical',
                                      command=self.tree.yview)
        tree_scrollbar.pack(side='right', fill='y')
        self.tree.configure(yscrollcommand=tree_scrollbar.set)
        self.tree.pack(side='left', fill='both', expand=True)

        # Bind events
        self.tree.bind('<Button-3>', self.show_context_menu)
        self.tree.bind('<Double-1>', self.on_tree_double_click)

        # Create context menus
        self.create_context_menus()
        self.create_context_menu()

    def create_context_menu(self):
        """Create context menu for download tree"""
        self.context_menu = tk.Menu(self.base_ui.root,
                                   tearoff=0,
                                   bg=AeroStyle.GLASS_BACKGROUND,
                                   fg=AeroStyle.TEXT_COLOR,
                                   activebackground=AeroStyle.ACCENT_LIGHT_BLUE,
                                   activeforeground=AeroStyle.TEXT_COLOR,
                                   relief='solid',
                                   bd=1)
        
        menu_items = [
            ("▶️ Start", self.start_stream),
            ("⏹️ Stop", self.stop_stream),
            ("🗑️ Remove", self.remove_stream),
            ("🔄 Restart", self.restart_stream),
            ("⏰ Set Delay", self.set_delay)
        ]
        
        for text, command in menu_items:
            self.context_menu.add_command(label=text, command=command)

    # Event handlers - These were missing from the original modular structure
    def load_csv(self):
        """Load CSV file with stream data"""
        file_path = filedialog.askopenfilename(
            title="Select CSV file",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )

        if file_path:
            self.base_ui.csv_data.clear()
            self.csv_tree.delete(*self.csv_tree.get_children())
            
            try:
                with open(file_path, newline='', encoding='utf-8') as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        name = row.get('name', '')
                        url = row.get('url', '')
                        if name and url:
                            self.base_ui.csv_data.append({'name': name, 'url': url})
                            self.csv_tree.insert('', 'end', text=name, values=(url,))

                self.csv_label.config(
                    text=f"Loaded: {len(self.base_ui.csv_data)} streams from {os.path.basename(file_path)}"
                )
                self.logger.log_to_console(f"Loaded {len(self.base_ui.csv_data)} streams from {file_path}")
                
            except Exception as e:
                self.csv_label.config(text="Error loading CSV")
                self.logger.log_to_console(f"Error loading CSV: {e}")
                messagebox.showerror("Error", f"Could not load CSV file:\n{e}")

    def add_manual_link(self):
        """Add a manual stream link"""
        name = simpledialog.askstring("Add Stream", "Enter stream name:")
        if not name:
            return

        url = simpledialog.askstring("Add Stream", "Enter stream URL:")
        if not url:
            return

        self.base_ui.csv_data.append({'name': name, 'url': url})
        self.csv_tree.insert('', 'end', text=name, values=(url,))
        self.logger.log_to_console(f"Added manual stream: {name}")

    def set_output_folder(self):
        """Set output folder for downloads"""
        folder = filedialog.askdirectory(
            title="Select output folder",
            initialdir=self.base_ui.output_folder
        )

        if folder:
            self.base_ui.output_folder = folder
            self.downloader.output_folder = folder
            self.output_label.config(text=f"📁 Output: {folder}")
            self.logger.log_to_console(f"Output folder set to: {folder}")

    def show_output_folder(self):
        """Open output folder in file explorer"""
        try:
            if platform.system() == "Windows":
                os.startfile(self.base_ui.output_folder)
            elif platform.system() == "Darwin":  # macOS
                subprocess.Popen(["open", self.base_ui.output_folder])
            else:  # Linux
                subprocess.Popen(["xdg-open", self.base_ui.output_folder])
        except Exception as e:
            self.logger.log_to_console(f"Error opening folder: {e}")

    def filter_streams(self, *args):
        """Filter streams based on search text"""
        search_text = self.base_ui.search_var.get().lower()
        
        # Clear and repopulate tree
        self.csv_tree.delete(*self.csv_tree.get_children())
        for item in self.base_ui.csv_data:
            name = item['name']
            url = item['url']
            if search_text in name.lower() or search_text in url.lower():
                self.csv_tree.insert('', 'end', text=name, values=(url,))

    def add_selected(self):
        """Add selected streams to download list"""
        selected = self.csv_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select streams to add")
            return

        added_count = 0
        for item in selected:
            name = self.csv_tree.item(item)['text']
            url = self.csv_tree.item(item)['values'][0]
            delay = float(self.base_ui.default_delay.get())
            
            if self.downloader.add_stream(name, url, delay):
                self.tree.insert('', 'end', text=name, 
                               values=('Stopped', delay, '0', '0'), 
                               tags=('Stopped',))
                added_count += 1

        if added_count > 0:
            self.logger.log_to_console(f"Added {added_count} streams to download list")
            
            # Auto-start streams if enabled
            if hasattr(self, 'settings_tab') and self.settings_tab.auto_start.get():
                self.logger.log_to_console("Auto-start enabled - starting streams automatically")
                # Start all newly added streams
                for item in selected:
                    name = self.csv_tree.item(item)['text']
                    if name in self.downloader.streams:
                        self.downloader.start_stream(name)

    def update_compression_controls(self):
        """Update compression control states based on checkbox"""
        # This method can be used to enable/disable compression controls
        # based on the checkbox state if needed
        pass

    def sort_tree_column(self, col, reverse):
        """Sort tree by column"""
        try:
            # Get all items from the tree
            items = [(self.tree.set(item, col), item) for item in self.tree.get_children('')]
            
            # Sort items
            if col == '#0':  # Name column
                items.sort(key=lambda x: x[0].lower(), reverse=reverse)
            elif col in ['Delay', 'Restart']:  # Numeric columns
                items.sort(key=lambda x: float(x[0]) if x[0].replace('.', '').isdigit() else 0, reverse=reverse)
            else:  # String columns
                items.sort(key=lambda x: x[0].lower(), reverse=reverse)
            
            # Rearrange items in sorted positions
            for index, (val, item) in enumerate(items):
                self.tree.move(item, '', index)
            
            # Reverse sort next time
            self.tree.heading(col, command=lambda: self.sort_tree_column(col, not reverse))
            
        except Exception as e:
            self.logger.log_to_console(f"Error sorting column {col}: {e}")

    def create_tooltip(self, widget, text):
        """Create a tooltip for a widget"""
        def show_tooltip(event):
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
            
            label = tk.Label(tooltip, text=text, justify='left',
                           background="#ffffe0", relief='solid', borderwidth=1,
                           font=("Segoe UI", 8))
            label.pack()
            
            def hide_tooltip(event):
                tooltip.destroy()
            
            widget.bind('<Leave>', hide_tooltip)
            tooltip.bind('<Leave>', hide_tooltip)
        
        widget.bind('<Enter>', show_tooltip)

    def start_stream(self):
        """Start selected streams"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select streams to start")
            return

        # Update quality setting
        self.downloader.selected_quality = self.base_ui.selected_quality.get()
        
        # Update compression settings
        self.downloader.set_compression_settings(
            enabled=self.base_ui.compression_enabled.get(),
            preset=self.base_ui.compression_preset.get(),
            crf=self.base_ui.compression_crf.get(),
            audio_bitrate=self.base_ui.compression_audio_bitrate.get()
        )

        for item in selected:
            name = self.tree.item(item)['text']
            if name in self.downloader.streams:
                self.downloader.start_stream(name)

    def stop_stream(self):
        """Stop selected streams"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select streams to stop")
            return

        for item in selected:
            name = self.tree.item(item)['text']
            if name in self.downloader.streams:
                self.downloader.stop_stream(name)

    def remove_stream(self):
        """Remove selected streams from download list"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select streams to remove")
            return

        for item in selected:
            name = self.tree.item(item)['text']
            if name in self.downloader.streams:
                self.downloader.stop_stream(name)
                del self.downloader.streams[name]
                self.tree.delete(item)

        self.logger.log_to_console(f"Removed {len(selected)} streams")

    def restart_stream(self):
        """Restart selected streams"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select streams to restart")
            return

        for item in selected:
            name = self.tree.item(item)['text']
            if name in self.downloader.streams:
                self.downloader.restart_stream(name)

    def set_delay(self):
        """Set delay for selected streams"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select streams to set delay")
            return

        delay = simpledialog.askfloat("Set Delay", "Enter delay in minutes:", minvalue=0)
        if delay is not None:
            for item in selected:
                name = self.tree.item(item)['text']
                if name in self.downloader.streams:
                    self.downloader.set_delay(name, delay)

    def save_download_list(self):
        """Save current download list to JSON"""
        file_path = filedialog.asksaveasfilename(
            title="Save download list",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )

        if file_path:
            try:
                data = []
                for name, stream in self.downloader.streams.items():
                    data.append({
                        'name': name,
                        'url': stream['url'],
                        'delay': stream['delay']
                    })

                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                
                self.logger.log_to_console(f"Download list saved to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not save download list:\n{e}")

    def load_download_list(self):
        """Load download list from JSON"""
        file_path = filedialog.askopenfilename(
            title="Load download list",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )

        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                # Clear current list
                for item in self.tree.get_children():
                    self.tree.delete(item)
                self.downloader.streams.clear()

                # Load new data
                for item in data:
                    name = item['name']
                    url = item['url']
                    delay = item.get('delay', 1)
                    
                    self.downloader.add_stream(name, url, delay)
                    self.tree.insert('', 'end', text=name, 
                                   values=('Stopped', delay, '0', '0'), 
                                   tags=('Stopped',))

                self.logger.log_to_console(f"Download list loaded from {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not load download list:\n{e}")

    def sort_tree_column(self, col, reverse):
        """Sort tree by column"""
        data = [(self.tree.set(child, col), child) for child in self.tree.get_children('')]
        
        # Handle numeric sorting for delay and restart columns
        if col in ('Delay', 'Restart'):
            data.sort(key=lambda x: float(x[0]) if x[0].replace('.', '').isdigit() else 0, reverse=reverse)
        else:
            data.sort(reverse=reverse)

        for index, (val, child) in enumerate(data):
            self.tree.move(child, '', index)

        # Toggle sort direction for next click
        self.tree.heading(col, command=lambda: self.sort_tree_column(col, not reverse))

    def create_context_menus(self):
        """Create context menus for trees"""
        # Context menu for download tree
        self.download_context_menu = tk.Menu(self.tree, tearoff=0)
        self.download_context_menu.add_command(label="▶️ Start", command=self.start_stream)
        self.download_context_menu.add_command(label="⏹️ Stop", command=self.stop_stream)
        self.download_context_menu.add_command(label="🔄 Restart", command=self.restart_stream)
        self.download_context_menu.add_separator()
        self.download_context_menu.add_command(label="🗑️ Remove", command=self.remove_stream)
        self.download_context_menu.add_separator()
        self.download_context_menu.add_command(label="📋 Copy Name", command=self.copy_stream_name)
        self.download_context_menu.add_command(label="🔗 Copy URL", command=self.copy_stream_url)

        # Context menu for CSV tree
        self.csv_context_menu = tk.Menu(self.csv_tree, tearoff=0)
        self.csv_context_menu.add_command(label="➕ Add to Downloads", command=self.add_selected)
        self.csv_context_menu.add_separator()
        self.csv_context_menu.add_command(label="📋 Copy Name", command=self.copy_csv_name)
        self.csv_context_menu.add_command(label="🔗 Copy URL", command=self.copy_csv_url)

        # Bind right-click to CSV tree
        self.csv_tree.bind('<Button-3>', self.show_csv_context_menu)

    def show_context_menu(self, event):
        """Show context menu on right-click for download tree"""
        try:
            self.download_context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.download_context_menu.grab_release()

    def show_csv_context_menu(self, event):
        """Show context menu on right-click for CSV tree"""
        try:
            self.csv_context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.csv_context_menu.grab_release()

    def copy_stream_name(self):
        """Copy selected stream name to clipboard"""
        selected = self.tree.selection()
        if selected:
            name = self.tree.item(selected[0])['text']
            self.base_ui.root.clipboard_clear()
            self.base_ui.root.clipboard_append(name)
            self.logger.log_to_console(f"Copied stream name: {name}")

    def copy_stream_url(self):
        """Copy selected stream URL to clipboard"""
        selected = self.tree.selection()
        if selected:
            name = self.tree.item(selected[0])['text']
            if name in self.downloader.streams:
                url = self.downloader.streams[name]['url']
                self.base_ui.root.clipboard_clear()
                self.base_ui.root.clipboard_append(url)
                self.logger.log_to_console(f"Copied stream URL: {url}")

    def copy_csv_name(self):
        """Copy selected CSV stream name to clipboard"""
        selected = self.csv_tree.selection()
        if selected:
            name = self.csv_tree.item(selected[0])['text']
            self.base_ui.root.clipboard_clear()
            self.base_ui.root.clipboard_append(name)
            self.logger.log_to_console(f"Copied CSV name: {name}")

    def copy_csv_url(self):
        """Copy selected CSV stream URL to clipboard"""
        selected = self.csv_tree.selection()
        if selected:
            url = self.csv_tree.item(selected[0])['values'][0]
            self.base_ui.root.clipboard_clear()
            self.base_ui.root.clipboard_append(url)
            self.logger.log_to_console(f"Copied CSV URL: {url}")

    def show_search_context_menu(self, event):
        """Show context menu for search entry"""
        try:
            self.search_context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.search_context_menu.grab_release()

    def paste_to_search(self, entry_widget):
        """Paste clipboard content to search entry"""
        try:
            clipboard_content = self.base_ui.root.clipboard_get()
            entry_widget.delete(0, tk.END)
            entry_widget.insert(0, clipboard_content)
            self.logger.log_to_console("Pasted content to search box")
        except Exception as e:
            self.logger.log_to_console(f"Error pasting to search: {e}")

    def copy_from_search(self, entry_widget):
        """Copy search entry content to clipboard"""
        try:
            content = entry_widget.get()
            self.base_ui.root.clipboard_clear()
            self.base_ui.root.clipboard_append(content)
            self.logger.log_to_console("Copied search content to clipboard")
        except Exception as e:
            self.logger.log_to_console(f"Error copying from search: {e}")

    def cut_from_search(self, entry_widget):
        """Cut search entry content to clipboard"""
        try:
            content = entry_widget.get()
            self.base_ui.root.clipboard_clear()
            self.base_ui.root.clipboard_append(content)
            entry_widget.delete(0, tk.END)
            self.logger.log_to_console("Cut search content to clipboard")
        except Exception as e:
            self.logger.log_to_console(f"Error cutting from search: {e}")

    def start_all_streams(self):
        """Start all stopped streams"""
        stopped_streams = []
        for item in self.tree.get_children():
            name = self.tree.item(item)['text']
            if name in self.downloader.streams and self.downloader.streams[name]['state'] == 'Stopped':
                stopped_streams.append(name)
        
        if not stopped_streams:
            messagebox.showinfo("Info", "No stopped streams to start")
            return
        
        # Update settings
        self.downloader.selected_quality = self.base_ui.selected_quality.get()
        self.downloader.set_compression_settings(
            enabled=self.base_ui.compression_enabled.get(),
            preset=self.base_ui.compression_preset.get(),
            crf=self.base_ui.compression_crf.get(),
            audio_bitrate=self.base_ui.compression_audio_bitrate.get()
        )
        
        # Start all stopped streams
        for name in stopped_streams:
            self.downloader.start_stream(name)
        
        self.logger.log_to_console(f"Started {len(stopped_streams)} streams")

    def stop_all_streams(self):
        """Stop all running streams"""
        running_streams = []
        for item in self.tree.get_children():
            name = self.tree.item(item)['text']
            if name in self.downloader.streams and self.downloader.streams[name]['state'] == 'Running':
                running_streams.append(name)
        
        if not running_streams:
            messagebox.showinfo("Info", "No running streams to stop")
            return
        
        # Stop all running streams
        for name in running_streams:
            self.downloader.stop_stream(name)
        
        self.logger.log_to_console(f"Stopped {len(running_streams)} streams")

    def update_stream_counters(self):
        """Update the stream counters in the header"""
        try:
            total_count = len(self.tree.get_children())
            active_count = 0
            
            for item in self.tree.get_children():
                name = self.tree.item(item)['text']
                if name in self.downloader.streams and self.downloader.streams[name]['state'] == 'Running':
                    active_count += 1
            
            if hasattr(self, 'active_count_label'):
                self.active_count_label.config(text=f"Active: {active_count}")
            if hasattr(self, 'total_count_label'):
                self.total_count_label.config(text=f"Total: {total_count}")
        except Exception as e:
            self.logger.log_to_console(f"Error updating counters: {e}")

    def on_csv_double_click(self, event):
        """Handle double-click on CSV tree"""
        selected = self.csv_tree.selection()
        if selected:
            name = self.csv_tree.item(selected[0])['text']
            url = self.csv_tree.item(selected[0])['values'][0]
            delay = float(self.base_ui.default_delay.get())
            
            if self.downloader.add_stream(name, url, delay):
                self.tree.insert('', 'end', text=name, 
                               values=('Stopped', delay, '0', '0'), 
                               tags=('Stopped',))

    def on_tree_double_click(self, event):
        """Handle double-click on download tree"""
        selected = self.tree.selection()
        if selected:
            name = self.tree.item(selected[0])['text']
            if name in self.downloader.streams:
                if self.downloader.streams[name]['state'] == 'Stopped':
                    self.downloader.start_stream(name)
                else:
                    self.downloader.stop_stream(name)

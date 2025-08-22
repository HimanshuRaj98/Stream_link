# ui/ui_csv_tools_tab.py
"""
CSV & Video Tools tab with file operations and video processing
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from aero_style import AeroStyle
from ui.ui_components import AeroComponents

class CSVToolsTab:
    def __init__(self, parent, base_ui, csv_tools, video_tools):
        self.parent = parent
        self.base_ui = base_ui
        self.csv_tools = csv_tools
        self.video_tools = video_tools
        self.components = AeroComponents()
        
        # Variables for file paths
        self.main_file_path = tk.StringVar()
        self.source_file_path = tk.StringVar()
        self.columns_to_copy = tk.StringVar(value="name,url")
        
        self.setup_csv_tools_tab()

    def setup_csv_tools_tab(self):
        """Setup the CSV & Video Tools tab"""
        # Title header
        title_header = self.components.create_styled_label(
            self.parent,
            "📊 CSV & Video Tools",
            'header'
        )
        title_header.pack(pady=(20, 15))

        # Create scrollable main container
        self.create_scrollable_container()
        
        # Create sections
        self.create_file_selection_section()
        self.create_csv_operations_section()
        self.create_video_tools_section()
        self.create_status_section()

    def create_scrollable_container(self):
        """Create scrollable container for all content"""
        # Main container
        main_container = tk.Frame(self.parent, bg=AeroStyle.GLASS_BACKGROUND)
        main_container.pack(fill='both', expand=True, padx=20, pady=10)

        # Create canvas for scrolling
        self.canvas = tk.Canvas(main_container, 
                               bg=AeroStyle.GLASS_BACKGROUND, 
                               highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_container, 
                                 orient="vertical", 
                                 command=self.canvas.yview)
        
        self.scrollable_frame = tk.Frame(self.canvas, bg=AeroStyle.GLASS_BACKGROUND)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        # Pack scrollable components
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Bind mousewheel to canvas
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)

    def on_mousewheel(self, event):
        """Handle mouse wheel scrolling"""
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def create_file_selection_section(self):
        """Create file selection section"""
        file_section = self.components.create_glass_frame(self.scrollable_frame)
        file_section.pack(fill='x', padx=10, pady=10)

        # Section header
        file_header = self.components.create_styled_label(
            file_section,
            "📁 File Selection",
            'subheader'
        )
        file_header.pack(anchor='w', padx=15, pady=(15, 10))

        # Main CSV file selection
        self.create_file_picker(file_section, 
                               "Main CSV File:", 
                               self.main_file_path, 
                               self.browse_main_file)

        # Source CSV file selection  
        self.create_file_picker(file_section,
                               "Source CSV File:",
                               self.source_file_path,
                               self.browse_source_file)

        # Columns configuration
        self.create_columns_config(file_section)

    def create_file_picker(self, parent, label_text, var, command):
        """Create a file picker row"""
        frame = tk.Frame(parent, bg=AeroStyle.GLASS_BACKGROUND)
        frame.pack(fill='x', padx=15, pady=5)

        # Label
        label = self.components.create_styled_label(frame, label_text)
        label.pack(side='left')

        # Entry
        entry = self.components.create_styled_entry(frame, textvariable=var, width=50)
        entry.pack(side='left', padx=10)

        # Browse button
        browse_btn = self.components.create_gradient_button(frame, "Browse", command)
        browse_btn.pack(side='left', padx=5)

    def create_columns_config(self, parent):
        """Create columns configuration"""
        columns_frame = tk.Frame(parent, bg=AeroStyle.GLASS_BACKGROUND)
        columns_frame.pack(fill='x', padx=15, pady=(5, 15))

        self.components.create_styled_label(
            columns_frame, "Columns to Copy:"
        ).pack(side='left')

        columns_entry = self.components.create_styled_entry(
            columns_frame, textvariable=self.columns_to_copy, width=30
        )
        columns_entry.pack(side='left', padx=10)

        self.components.create_styled_label(
            columns_frame, "(comma-separated)", 'secondary'
        ).pack(side='left', padx=5)

    def create_csv_operations_section(self):
        """Create CSV operations section"""
        operations_section = self.components.create_glass_frame(self.scrollable_frame)
        operations_section.pack(fill='x', padx=10, pady=10)

        # Section header
        operations_header = self.components.create_styled_label(
            operations_section,
            "🔧 CSV Operations",
            'subheader'
        )
        operations_header.pack(anchor='w', padx=15, pady=(15, 10))

        # Operations buttons container
        ops_buttons_frame = tk.Frame(operations_section, bg=AeroStyle.GLASS_BACKGROUND)
        ops_buttons_frame.pack(fill='x', padx=15, pady=10)

        # First row of operations
        ops_row1 = tk.Frame(ops_buttons_frame, bg=AeroStyle.GLASS_BACKGROUND)
        ops_row1.pack(fill='x', pady=5)

        self.components.create_gradient_button(
            ops_row1, "🔀 Merge CSVs", self.merge_csvs, 'primary'
        ).pack(side='left', padx=5)

        self.components.create_gradient_button(
            ops_row1, "🔤 Sort Main CSV", self.sort_main_csv
        ).pack(side='left', padx=5)

        self.components.create_gradient_button(
            ops_row1, "🧹 Remove Duplicates", self.remove_duplicates
        ).pack(side='left', padx=5)

        # Second row of operations
        ops_row2 = tk.Frame(ops_buttons_frame, bg=AeroStyle.GLASS_BACKGROUND)
        ops_row2.pack(fill='x', pady=5)

        self.components.create_gradient_button(
            ops_row2, "💾 Export Cleaned", self.export_cleaned_csv, 'primary'
        ).pack(side='left', padx=5)

        self.components.create_gradient_button(
            ops_row2, "🔗 Generate URLs", self.generate_urls
        ).pack(side='left', padx=5)

        # Operation descriptions
        self.create_operation_descriptions(operations_section)

    def create_operation_descriptions(self, parent):
        """Create descriptions for CSV operations"""
        desc_frame = self.components.create_glass_frame(parent)
        desc_frame.pack(fill='x', padx=15, pady=(10, 15))

        desc_header = self.components.create_styled_label(
            desc_frame, "ℹ️ Operation Descriptions", 'subheader'
        )
        desc_header.pack(anchor='w', padx=10, pady=(10, 5))

        descriptions = [
            ("🔀 Merge CSVs", "Combines unique entries from source CSV into main CSV"),
            ("🔤 Sort Main CSV", "Sorts main CSV alphabetically by first column"),
            ("🧹 Remove Duplicates", "Removes duplicate entries based on name column"),
            ("💾 Export Cleaned", "Exports a cleaned and sorted version to new file"),
            ("🔗 Generate URLs", "Generates streaming URLs from image background sources")
        ]

        for title, desc in descriptions:
            row = tk.Frame(desc_frame, bg=AeroStyle.GLASS_BACKGROUND)
            row.pack(fill='x', padx=10, pady=2)
            
            self.components.create_styled_label(row, title, 'normal').pack(side='left')
            self.components.create_styled_label(row, f" - {desc}", 'secondary').pack(side='left')

    def create_video_tools_section(self):
        """Create video tools section"""
        video_section = self.components.create_glass_frame(self.scrollable_frame)
        video_section.pack(fill='x', padx=10, pady=10)

        # Section header
        video_header = self.components.create_styled_label(
            video_section,
            "🎬 Video Tools",
            'subheader'
        )
        video_header.pack(anchor='w', padx=15, pady=(15, 10))

        # Video operations
        video_buttons_frame = tk.Frame(video_section, bg=AeroStyle.GLASS_BACKGROUND)
        video_buttons_frame.pack(fill='x', padx=15, pady=10)

        self.components.create_gradient_button(
            video_buttons_frame, "🎞️ Merge MP4 Files", self.merge_videos, 'primary'
        ).pack(side='left', padx=5)

        # Video tools info
        info_frame = self.components.create_glass_frame(video_section)
        info_frame.pack(fill='x', padx=15, pady=(10, 15))

        info_text = self.components.create_styled_label(
            info_frame,
            "💡 Video merging requires FFmpeg to be installed and available in system PATH",
            'secondary'
        )
        info_text.pack(anchor='w', padx=10, pady=10)

        req_frame = tk.Frame(info_frame, bg=AeroStyle.GLASS_BACKGROUND)
        req_frame.pack(fill='x', padx=10, pady=(0, 10))
        
        self.components.create_styled_label(req_frame, "Requirements:", 'normal').pack(side='left')
        self.components.create_styled_label(req_frame, "FFmpeg installed", 'secondary').pack(side='left', padx=(10, 0))

    def create_status_section(self):
        """Create status display section"""
        self.status_frame = self.components.create_glass_frame(self.scrollable_frame)
        self.status_frame.pack(fill='x', padx=10, pady=10)

        status_header = self.components.create_styled_label(
            self.status_frame,
            "📊 Operation Status",
            'subheader'
        )
        status_header.pack(anchor='w', padx=15, pady=(15, 5))

        self.csv_status_label = self.components.create_styled_label(
            self.status_frame,
            "Ready for CSV/Video operations",
            'secondary'
        )
        self.csv_status_label.pack(anchor='w', padx=15, pady=(5, 15))

    # Event handlers
    def browse_main_file(self):
        """Browse for main CSV file"""
        file_path = filedialog.askopenfilename(
            title="Select Main CSV File",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if file_path:
            self.main_file_path.set(file_path)

    def browse_source_file(self):
        """Browse for source CSV file"""
        file_path = filedialog.askopenfilename(
            title="Select Source CSV File",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if file_path:
            self.source_file_path.set(file_path)

    def merge_csvs(self):
        """Merge CSV files using CSV tools"""
        try:
            main_file = self.main_file_path.get()
            source_file = self.source_file_path.get()
            columns = [col.strip() for col in self.columns_to_copy.get().split(',')]

            if not main_file or not source_file:
                messagebox.showerror("Error", "Please select both main and source CSV files")
                return

            result = self.csv_tools.merge_csvs(main_file, source_file, columns)
            messagebox.showinfo("Success", result)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to merge CSVs:\n{e}")

    def sort_main_csv(self):
        """Sort main CSV file"""
        try:
            main_file = self.main_file_path.get()
            columns = [col.strip() for col in self.columns_to_copy.get().split(',')]

            if not main_file:
                messagebox.showerror("Error", "Please select main CSV file")
                return

            result = self.csv_tools.sort_main_csv(main_file, columns)
            messagebox.showinfo("Success", result)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to sort CSV:\n{e}")

    def remove_duplicates(self):
        """Remove duplicates from main CSV"""
        try:
            main_file = self.main_file_path.get()
            columns = [col.strip() for col in self.columns_to_copy.get().split(',')]

            if not main_file:
                messagebox.showerror("Error", "Please select main CSV file")
                return

            result = self.csv_tools.remove_duplicates_by_name(main_file, columns)
            messagebox.showinfo("Success", result)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to remove duplicates:\n{e}")

    def export_cleaned_csv(self):
        """Export cleaned and sorted CSV"""
        try:
            main_file = self.main_file_path.get()
            columns = [col.strip() for col in self.columns_to_copy.get().split(',')]

            if not main_file:
                messagebox.showerror("Error", "Please select main CSV file")
                return

            save_path = filedialog.asksaveasfilename(
                title="Save Cleaned CSV",
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
            )

            if save_path:
                result = self.csv_tools.export_cleaned_sorted_csv(main_file, save_path, columns)
                messagebox.showinfo("Success", result)
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export CSV:\n{e}")

    def generate_urls(self):
        """Generate URLs from CSV using image links"""
        try:
            file_path = filedialog.askopenfilename(
                title="Select CSV with Image Links",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
            )

            if file_path:
                result_path = self.csv_tools.generate_urls_from_csv(file_path)
                messagebox.showinfo("Success", 
                    f"URLs generated successfully!\nSaved as: {os.path.basename(result_path)}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate URLs:\n{e}")

    def merge_videos(self):
        """Merge MP4 videos using video tools"""
        try:
            self.video_tools.merge_videos()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to merge videos:\n{e}")

    def update_csv_status(self, message):
        """Update CSV tools status label"""
        if hasattr(self, 'csv_status_label'):
            self.csv_status_label.config(text=message)

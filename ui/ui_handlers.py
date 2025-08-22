# ui/ui_handlers.py
"""
Event handlers for UI interactions
"""
from tkinter import messagebox, simpledialog
import os
import platform
import subprocess

class UIHandlers:
    def __init__(self, base_ui, downloader, logger):
        self.base_ui = base_ui
        self.downloader = downloader
        self.logger = logger

    def add_manual_link(self):
        """Add a manual stream link"""
        name = simpledialog.askstring("Add Stream", "Enter stream name:")
        if not name:
            return

        url = simpledialog.askstring("Add Stream", "Enter stream URL:")
        if not url:
            return

        self.base_ui.csv_data.append({'name': name, 'url': url})
        # Update CSV tree if it exists
        if hasattr(self.base_ui, 'csv_tree'):
            self.base_ui.csv_tree.insert('', 'end', text=name, values=(url,))
        
        self.logger.log_to_console(f"Added manual stream: {name}")

    def set_output_folder(self):
        """Set output folder for downloads"""
        from tkinter import filedialog
        
        folder = filedialog.askdirectory(
            title="Select output folder",
            initialdir=self.base_ui.output_folder
        )

        if folder:
            self.base_ui.output_folder = folder
            self.downloader.output_folder = folder
            if hasattr(self.base_ui, 'output_label'):
                self.base_ui.output_label.config(text=f"📁 Output: {folder}")
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

    def add_selected(self, tree_widget):
        """Add selected streams to download list"""
        selected = tree_widget.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select streams to add")
            return

        added_count = 0
        for item in selected:
            name = tree_widget.item(item)['text']
            url = tree_widget.item(item)['values'][0]
            delay = float(self.base_ui.default_delay.get())
            
            if self.downloader.add_stream(name, url, delay):
                # Update download tree if it exists
                if hasattr(self.base_ui, 'tree'):
                    self.base_ui.tree.insert('', 'end', text=name, 
                                           values=('Stopped', delay, '0'), 
                                           tags=('Stopped',))
                added_count += 1

        if added_count > 0:
            self.logger.log_to_console(f"Added {added_count} streams to download list")

    def start_stream(self, tree_widget=None):
        """Start selected streams"""
        if tree_widget is None and hasattr(self.base_ui, 'tree'):
            tree_widget = self.base_ui.tree
            
        selected = tree_widget.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select streams to start")
            return

        # Update quality setting
        self.downloader.selected_quality = self.base_ui.selected_quality.get()

        for item in selected:
            name = tree_widget.item(item)['text']
            if name in self.downloader.streams:
                self.downloader.start_stream(name)

    def stop_stream(self, tree_widget=None):
        """Stop selected streams"""
        if tree_widget is None and hasattr(self.base_ui, 'tree'):
            tree_widget = self.base_ui.tree
            
        selected = tree_widget.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select streams to stop")
            return

        for item in selected:
            name = tree_widget.item(item)['text']
            if name in self.downloader.streams:
                self.downloader.stop_stream(name)

    def remove_stream(self, tree_widget=None):
        """Remove selected streams from download list"""
        if tree_widget is None and hasattr(self.base_ui, 'tree'):
            tree_widget = self.base_ui.tree
            
        selected = tree_widget.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select streams to remove")
            return

        for item in selected:
            name = tree_widget.item(item)['text']
            if name in self.downloader.streams:
                self.downloader.stop_stream(name)
                del self.downloader.streams[name]
                tree_widget.delete(item)

        self.logger.log_to_console(f"Removed {len(selected)} streams")

    def restart_stream(self, tree_widget=None):
        """Restart selected streams"""
        if tree_widget is None and hasattr(self.base_ui, 'tree'):
            tree_widget = self.base_ui.tree
            
        selected = tree_widget.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select streams to restart")
            return

        for item in selected:
            name = tree_widget.item(item)['text']
            if name in self.downloader.streams:
                self.downloader.restart_stream(name)

    def set_delay(self, tree_widget=None):
        """Set delay for selected streams"""
        if tree_widget is None and hasattr(self.base_ui, 'tree'):
            tree_widget = self.base_ui.tree
            
        selected = tree_widget.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select streams to set delay")
            return

        delay = simpledialog.askfloat("Set Delay", "Enter delay in minutes:", minvalue=0)
        if delay is not None:
            for item in selected:
                name = tree_widget.item(item)['text']
                if name in self.downloader.streams:
                    self.downloader.set_delay(name, delay)

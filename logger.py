# logger.py
"""
Logger - Centralized logging for the Streamlink Downloader application.
Handles application logs, Streamlink logs, status bar updates, and exporting logs.
"""

import tkinter as tk
from datetime import datetime
from tkinter import filedialog, messagebox


class Logger:
    def __init__(self, status_updater=None, app_log_widget=None, streamlink_log_widget=None):
        """
        :param status_updater: Function to update status bar label
        :param app_log_widget: Tk Text widget for app logs
        :param streamlink_log_widget: Tk Text widget for streamlink logs
        """
        self.update_status = status_updater if status_updater else lambda msg: None
        self.app_log_text = app_log_widget
        self.streamlink_log_text = streamlink_log_widget

        self.app_logs = []
        self.streamlink_logs = []

    # ----------------- General Application Logging -----------------
    def log_to_console(self, message):
        """Log normal application messages with timestamp."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        self.app_logs.append(log_entry)

        # Console print
        print(log_entry)

        # Update status bar
        self.update_status(message)

        # Update app log text widget if available
        if self.app_log_text:
            self.app_log_text.config(state='normal')

            if "Error" in message:
                self._insert_colored(self.app_log_text, log_entry, "error", "red")
            elif "Starting" in message:
                self._insert_colored(self.app_log_text, log_entry, "success", "green")
            else:
                self.app_log_text.insert(tk.END, log_entry + '\n')

            self.app_log_text.see(tk.END)
            self.app_log_text.config(state='disabled')

    # ----------------- Streamlink Logging -----------------
    def log_streamlink(self, message):
        """Log streamlink output messages with timestamp."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        self.streamlink_logs.append(log_entry)

        # Update UI if available
        if self.streamlink_log_text:
            self.streamlink_log_text.config(state='normal')
            self.streamlink_log_text.insert(tk.END, log_entry + '\n')
            self.streamlink_log_text.see(tk.END)
            self.streamlink_log_text.config(state='disabled')

    # ----------------- Internal helper -----------------
    def _insert_colored(self, widget, text, tag, color):
        """Insert colored log message into a Text widget."""
        widget.insert(tk.END, text + '\n')
        line_start = widget.index("end-2c linestart")
        line_end = widget.index("end-2c lineend")
        widget.tag_add(tag, line_start, line_end)
        widget.tag_config(tag, foreground=color)

    # ----------------- Clear Logs -----------------
    def clear_logs(self, app_log=True, streamlink_log=True):
        """Clear logs from memory and UI."""
        if app_log:
            self.app_logs.clear()
            if self.app_log_text:
                self.app_log_text.config(state='normal')
                self.app_log_text.delete(1.0, tk.END)
                self.app_log_text.config(state='disabled')
            self.log_to_console("Application log cleared")

        if streamlink_log:
            self.streamlink_logs.clear()
            if self.streamlink_log_text:
                self.streamlink_log_text.config(state='normal')
                self.streamlink_log_text.delete(1.0, tk.END)
                self.streamlink_log_text.config(state='disabled')
            self.log_to_console("Streamlink log cleared")

    # ----------------- Export Logs -----------------
    def export_logs(self, app_log=True):
        """Export logs to a file."""
        file = filedialog.asksaveasfilename(
            defaultextension=".log",
            filetypes=[("Log files", "*.log")],
            initialfile="application.log" if app_log else "streamlink.log"
        )
        if file:
            try:
                with open(file, 'w', encoding='utf-8') as f:
                    if app_log:
                        f.write("=== Application Log ===\n")
                        f.write("\n".join(self.app_logs))
                    else:
                        f.write("=== Streamlink Log ===\n")
                        f.write("\n".join(self.streamlink_logs))
                self.log_to_console(f"Log exported to {file}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not export log:\n{e}")

# ui/ui_log_tab.py
"""
Log tab with dual logging system for application and streamlink logs
"""
import tkinter as tk
from tkinter import ttk
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from aero_style import AeroStyle
from ui.ui_components import AeroComponents

class LogTab:
    def __init__(self, parent, base_ui, logger):
        self.parent = parent
        self.base_ui = base_ui
        self.logger = logger
        self.components = AeroComponents()
        
        self.setup_log_tab()
        
        # Update logger with UI widgets after creation
        self.logger.app_log_text = self.log_text
        self.logger.streamlink_log_text = self.streamlink_text

    def setup_log_tab(self):
        """Setup the log tab UI with dual log display"""
        # Create notebook for different log types
        self.log_notebook = ttk.Notebook(self.parent, style='Aero.TNotebook')
        self.log_notebook.pack(fill='both', expand=True, padx=10, pady=5)

        # Create tab frames
        self.app_log_frame = self.components.create_glass_frame(self.log_notebook)
        self.streamlink_log_frame = self.components.create_glass_frame(self.log_notebook)

        # Add tabs to notebook
        self.log_notebook.add(self.app_log_frame, text='📋 Application Logs')
        self.log_notebook.add(self.streamlink_log_frame, text='📄 Streamlink Logs')

        # Setup individual log displays
        self.create_app_log_display()
        self.create_streamlink_log_display()
        self.create_log_controls()

    def create_app_log_display(self):
        """Create application log display"""
        # Header
        app_header = self.components.create_styled_label(
            self.app_log_frame,
            "📋 Application Activity",
            'subheader'
        )
        app_header.pack(anchor='w', padx=15, pady=(15, 10))

        # Log display frame
        log_frame = tk.Frame(self.app_log_frame, bg=AeroStyle.GLASS_BACKGROUND)
        log_frame.pack(fill='both', expand=True, padx=15, pady=(0, 15))

        # Text widget with enhanced styling
        self.log_text = tk.Text(log_frame,
                               state='disabled',
                               wrap='word',
                               bg='white',
                               fg=AeroStyle.TEXT_COLOR,
                               font=('Consolas', 9),
                               relief='solid',
                               bd=1,
                               selectbackground=AeroStyle.ACCENT_LIGHT_BLUE)

        # Scrollbar
        log_scrollbar = ttk.Scrollbar(log_frame, 
                                     orient='vertical', 
                                     command=self.log_text.yview)
        log_scrollbar.pack(side='right', fill='y')
        
        self.log_text.configure(yscrollcommand=log_scrollbar.set)
        self.log_text.pack(side='left', fill='both', expand=True)

        # Configure tags for colored logging
        self.log_text.tag_configure('error', foreground=AeroStyle.ERROR_COLOR, font=('Consolas', 9, 'bold'))
        self.log_text.tag_configure('success', foreground=AeroStyle.SUCCESS_COLOR, font=('Consolas', 9, 'bold'))
        self.log_text.tag_configure('warning', foreground=AeroStyle.WARNING_COLOR, font=('Consolas', 9, 'bold'))

    def create_streamlink_log_display(self):
        """Create streamlink log display"""
        # Header
        streamlink_header = self.components.create_styled_label(
            self.streamlink_log_frame,
            "📄 Streamlink Output",
            'subheader'
        )
        streamlink_header.pack(anchor='w', padx=15, pady=(15, 10))

        # Info panel
        info_frame = self.components.create_glass_frame(self.streamlink_log_frame)
        info_frame.pack(fill='x', padx=15, pady=(0, 10))

        info_text = self.components.create_styled_label(
            info_frame,
            "💡 This tab shows real-time output from Streamlink processes",
            'secondary'
        )
        info_text.pack(anchor='w', padx=10, pady=8)

        # Log display frame
        streamlink_frame = tk.Frame(self.streamlink_log_frame, bg=AeroStyle.GLASS_BACKGROUND)
        streamlink_frame.pack(fill='both', expand=True, padx=15, pady=(0, 15))

        # Text widget
        self.streamlink_text = tk.Text(streamlink_frame,
                                      state='disabled',
                                      wrap='word',
                                      bg='#1e1e1e',  # Dark background for console feel
                                      fg='#00ff00',   # Green text for console feel
                                      font=('Consolas', 8),
                                      relief='solid',
                                      bd=1,
                                      insertbackground='white')

        # Scrollbar
        streamlink_scrollbar = ttk.Scrollbar(streamlink_frame,
                                           orient='vertical',
                                           command=self.streamlink_text.yview)
        streamlink_scrollbar.pack(side='right', fill='y')
        
        self.streamlink_text.configure(yscrollcommand=streamlink_scrollbar.set)
        self.streamlink_text.pack(side='left', fill='both', expand=True)

        # Configure tags for different message types
        self.streamlink_text.tag_configure('process', foreground='#00ffff')  # Cyan for process info
        self.streamlink_text.tag_configure('error', foreground='#ff4444')   # Red for errors
        self.streamlink_text.tag_configure('info', foreground='#ffff00')    # Yellow for info

    def create_log_controls(self):
        """Create log control buttons"""
        controls_frame = self.components.create_glass_frame(self.parent)
        controls_frame.pack(fill='x', padx=15, pady=(0, 15))

        # Control buttons container
        buttons_container = tk.Frame(controls_frame, bg=AeroStyle.GLASS_BACKGROUND)
        buttons_container.pack(pady=15)

        # Left side buttons - Clear functions
        left_buttons = tk.Frame(buttons_container, bg=AeroStyle.GLASS_BACKGROUND)
        left_buttons.pack(side='left', padx=15)

        clear_app_btn = self.components.create_gradient_button(
            left_buttons, "🗑️ Clear App Log", self.clear_app_log
        )
        clear_app_btn.pack(side='left', padx=5)

        clear_streamlink_btn = self.components.create_gradient_button(
            left_buttons, "🗑️ Clear Streamlink Log", self.clear_streamlink_log
        )
        clear_streamlink_btn.pack(side='left', padx=5)

        clear_all_btn = self.components.create_gradient_button(
            left_buttons, "🧹 Clear All Logs", self.clear_all_logs, 'primary'
        )
        clear_all_btn.pack(side='left', padx=5)

        # Right side buttons - Export functions
        right_buttons = tk.Frame(buttons_container, bg=AeroStyle.GLASS_BACKGROUND)
        right_buttons.pack(side='right', padx=15)

        export_app_btn = self.components.create_gradient_button(
            right_buttons, "💾 Export App Log", self.export_app_log, 'primary'
        )
        export_app_btn.pack(side='left', padx=5)

        export_streamlink_btn = self.components.create_gradient_button(
            right_buttons, "💾 Export Streamlink Log", self.export_streamlink_log, 'primary'
        )
        export_streamlink_btn.pack(side='left', padx=5)

        # Auto-scroll controls
        auto_scroll_frame = tk.Frame(buttons_container, bg=AeroStyle.GLASS_BACKGROUND)
        auto_scroll_frame.pack(pady=(10, 0))

        self.auto_scroll_var = tk.BooleanVar(value=True)
        auto_scroll_check = tk.Checkbutton(auto_scroll_frame,
                                          text="📜 Auto-scroll logs",
                                          variable=self.auto_scroll_var,
                                          bg=AeroStyle.GLASS_BACKGROUND,
                                          fg=AeroStyle.TEXT_COLOR,
                                          selectcolor=AeroStyle.ACCENT_LIGHT_BLUE,
                                          font=('Segoe UI', 9))
        auto_scroll_check.pack()

    # Event handlers
    def clear_app_log(self):
        """Clear application log only"""
        self.logger.clear_logs(app_log=True, streamlink_log=False)

    def clear_streamlink_log(self):
        """Clear streamlink log only"""
        self.logger.clear_logs(app_log=False, streamlink_log=True)

    def clear_all_logs(self):
        """Clear both logs"""
        self.logger.clear_logs(app_log=True, streamlink_log=True)

    def export_app_log(self):
        """Export application log to file"""
        self.logger.export_logs(app_log=True)

    def export_streamlink_log(self):
        """Export streamlink log to file"""
        self.logger.export_logs(app_log=False)

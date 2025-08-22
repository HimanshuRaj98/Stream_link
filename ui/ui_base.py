# ui/ui_base.py
"""
Base UI class with window setup and styling
"""
import tkinter as tk
from tkinter import ttk
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from aero_style import AeroStyle
from ui.ui_components import AeroComponents

class BaseUI:
    def __init__(self):
        self.root = tk.Tk()
        self.components = AeroComponents()
        
        # Data initialization
        self.csv_data = []
        self.output_folder = os.path.join(os.path.expanduser("~"), "Documents", "YTS", "M3U8")
        os.makedirs(self.output_folder, exist_ok=True)
        
        # Variables
        self.selected_quality = tk.StringVar(value="best")
        self.default_delay = tk.StringVar(value="1")
        self.search_var = tk.StringVar()
        self.sort_column = None
        self.sort_reverse = False
        
        # Compression variables
        self.compression_enabled = tk.BooleanVar(value=False)
        self.compression_preset = tk.StringVar(value="medium")
        self.compression_crf = tk.IntVar(value=23)
        self.compression_audio_bitrate = tk.StringVar(value="128k")
        
        # CSV Tools variables
        self.main_file_path = tk.StringVar()
        self.source_file_path = tk.StringVar()
        self.columns_to_copy = tk.StringVar(value="name,url")

    def setup_window(self):
        """Configure main window"""
        self.root.title("Streamlink Downloader - Aero Edition")
        self.root.geometry("1200x850")
        self.root.configure(bg=AeroStyle.BACKGROUND)
        self.root.minsize(1000, 700)
        self.root.wm_attributes('-alpha', 0.98)
        
        self.center_window()
        self.add_window_effects()
        self.setup_styles()

    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def add_window_effects(self):
        """Add visual effects to simulate Aero glass"""
        self.root.configure(highlightthickness=1, highlightcolor=AeroStyle.ACCENT_BLUE)

    def setup_styles(self):
        """Configure Aero-style TTK themes"""
        style = ttk.Style()
        
        # Configure Notebook (tabs) with glass effect
        style.configure('Aero.TNotebook',
                       background=AeroStyle.GLASS_BACKGROUND,
                       borderwidth=1,
                       relief='solid')
        
        style.configure('Aero.TNotebook.Tab',
                       background=AeroStyle.BUTTON_GRADIENT_END,
                       foreground=AeroStyle.TEXT_COLOR,
                       padding=[20, 8],
                       borderwidth=1,
                       focuscolor='none')
        
        style.map('Aero.TNotebook.Tab',
                 background=[('selected', AeroStyle.ACCENT_LIGHT_BLUE),
                           ('active', AeroStyle.BUTTON_HOVER_END)])

        # Configure Treeview with glass effect
        style.configure('Aero.Treeview',
                       background='white',
                       foreground=AeroStyle.TEXT_COLOR,
                       fieldbackground='white',
                       borderwidth=1,
                       relief='solid')
        
        style.configure('Aero.Treeview.Heading',
                       background=AeroStyle.ACCENT_LIGHT_BLUE,
                       foreground=AeroStyle.TEXT_COLOR,
                       borderwidth=1,
                       relief='solid')

        # Configure Buttons with enhanced styling
        style.configure('Aero.TButton',
                       background=AeroStyle.BUTTON_GRADIENT_END,
                       foreground=AeroStyle.TEXT_COLOR,
                       borderwidth=1,
                       relief='solid',
                       padding=[12, 6],
                       font=('Segoe UI', 9))
        
        style.map('Aero.TButton',
                 background=[('active', AeroStyle.BUTTON_HOVER_END),
                           ('pressed', AeroStyle.ACCENT_LIGHT_BLUE)],
                 relief=[('pressed', 'sunken')])

        # Configure Combobox with glass effect
        style.configure('Aero.TCombobox',
                       fieldbackground='white',
                       background=AeroStyle.BUTTON_GRADIENT_END,
                       borderwidth=1,
                       relief='solid',
                       font=('Segoe UI', 9))

    def animate_startup(self):
        """Animate window appearance"""
        self.root.wm_attributes('-alpha', 0.0)
        self.root.after(50, self.fade_in)

    def fade_in(self, alpha=0.0):
        """Fade in animation"""
        alpha += 0.1
        self.root.wm_attributes('-alpha', alpha)
        if alpha < 0.98:
            self.root.after(30, lambda: self.fade_in(alpha))

    def create_status_bar(self):
        """Create status bar at the bottom of the window"""
        self.status_frame = self.components.create_glass_frame(self.root)
        self.status_frame.pack(side='bottom', fill='x', padx=10, pady=(0, 10))

        self.status_label = self.components.create_styled_label(
            self.status_frame,
            text="Ready",
            anchor='w'
        )
        self.status_label.pack(fill='x', padx=10, pady=5)

    def update_status(self, message):
        """Update main status bar"""
        if hasattr(self, 'status_label'):
            self.status_label.config(text=message)

# ui/ui_components.py
"""
Reusable UI components with Aero styling
"""
import tkinter as tk
from tkinter import ttk
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from aero_style import AeroStyle

class AeroComponents:
    @staticmethod
    def create_glass_frame(parent, **kwargs):
        """Create a frame with glass-like appearance"""
        frame = tk.Frame(parent,
                        bg=AeroStyle.GLASS_BACKGROUND,
                        relief='solid',
                        bd=1,
                        **kwargs)
        return frame

    @staticmethod
    def create_gradient_button(parent, text, command, style='primary'):
        """Create a button with gradient-like appearance"""
        if style == 'primary':
            bg_color = AeroStyle.ACCENT_BLUE
            fg_color = 'white'
            active_bg = '#106EBE'
        else:
            bg_color = AeroStyle.BUTTON_GRADIENT_END
            fg_color = AeroStyle.TEXT_COLOR
            active_bg = AeroStyle.BUTTON_HOVER_END

        button = tk.Button(parent,
                          text=text,
                          command=command,
                          bg=bg_color,
                          fg=fg_color,
                          activebackground=active_bg,
                          activeforeground=fg_color if style == 'primary' else AeroStyle.TEXT_COLOR,
                          border=0,
                          relief='flat',
                          font=('Segoe UI', 9),
                          cursor='hand2',
                          padx=15,
                          pady=6)

        # Add hover effects
        def on_enter(e):
            button.configure(bg=active_bg)
            if style == 'primary':
                button.configure(relief='raised')

        def on_leave(e):
            button.configure(bg=bg_color)
            button.configure(relief='flat')

        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
        return button

    @staticmethod
    def create_styled_entry(parent, textvariable=None, width=30, **kwargs):
        """Create a styled entry widget"""
        entry = tk.Entry(parent,
                        textvariable=textvariable,
                        width=width,
                        font=('Segoe UI', 9),
                        relief='solid',
                        bd=1,
                        **kwargs)
        return entry

    @staticmethod
    def create_styled_label(parent, text, style='normal', **kwargs):
        """Create a styled label"""
        styles = {
            'header': {'font': ('Segoe UI', 12, 'bold'), 'fg': AeroStyle.TEXT_COLOR},
            'subheader': {'font': ('Segoe UI', 10, 'bold'), 'fg': AeroStyle.TEXT_COLOR},
            'normal': {'font': ('Segoe UI', 9), 'fg': AeroStyle.TEXT_COLOR},
            'secondary': {'font': ('Segoe UI', 9), 'fg': AeroStyle.SECONDARY_TEXT}
        }
        
        style_config = styles.get(style, styles['normal'])
        
        label = tk.Label(parent,
                        text=text,
                        bg=AeroStyle.GLASS_BACKGROUND,
                        **style_config,
                        **kwargs)
        return label

    @staticmethod
    def create_styled_treeview(parent, columns=(), show='tree headings', **kwargs):
        """Create a styled treeview"""
        tree = ttk.Treeview(parent,
                           columns=columns,
                           show=show,
                           style='Aero.Treeview',
                           **kwargs)
        return tree

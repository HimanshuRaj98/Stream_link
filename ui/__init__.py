# ui/__init__.py
"""
Modular UI package for Streamlink Downloader
Complete module collection with all tabs
"""
from .ui_base import BaseUI
from .ui_components import AeroComponents  
from .ui_main_tab import MainTab
from .ui_log_tab import LogTab
from .ui_csv_tools_tab import CSVToolsTab
from .ui_settings_tab import SettingsTab
from .ui_handlers import UIHandlers

__all__ = [
    'BaseUI', 
    'AeroComponents', 
    'MainTab', 
    'LogTab', 
    'CSVToolsTab', 
    'SettingsTab', 
    'UIHandlers'
]

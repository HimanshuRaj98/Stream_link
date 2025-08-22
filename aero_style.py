# aero_style.py
"""
AeroStyle - Constants for Aero Glass-like styling configuration.
This file holds all color values and theme constants for consistent
styling across the application.
"""

class AeroStyle:
    """Aero Glass-like styling configuration"""

    # Light theme colors
    LIGHT_BACKGROUND = '#F0F0F0'
    LIGHT_GLASS_BACKGROUND = '#FAFAFA'
    LIGHT_ACCENT_BLUE = '#0078D4'
    LIGHT_ACCENT_LIGHT_BLUE = '#E3F2FD'
    LIGHT_ACCENT_DARK_BLUE = '#005A9E'
    LIGHT_BORDER_COLOR = '#D0D0D0'
    LIGHT_TEXT_COLOR = '#2D2D2D'
    LIGHT_SECONDARY_TEXT = '#666666'
    LIGHT_SUCCESS_COLOR = '#4CAF50'
    LIGHT_WARNING_COLOR = '#FF9800'
    LIGHT_ERROR_COLOR = '#F44336'
    LIGHT_HIGHLIGHT_COLOR = '#FFF3E0'

    # Dark theme colors
    DARK_BACKGROUND = '#1E1E1E'
    DARK_GLASS_BACKGROUND = '#2D2D2D'
    DARK_ACCENT_BLUE = '#0078D4'
    DARK_ACCENT_LIGHT_BLUE = '#1E3A5F'
    DARK_ACCENT_DARK_BLUE = '#005A9E'
    DARK_BORDER_COLOR = '#404040'
    DARK_TEXT_COLOR = '#FFFFFF'
    DARK_SECONDARY_TEXT = '#CCCCCC'
    DARK_SUCCESS_COLOR = '#4CAF50'
    DARK_WARNING_COLOR = '#FF9800'
    DARK_ERROR_COLOR = '#F44336'
    DARK_HIGHLIGHT_COLOR = '#3E3E3E'

    # Current theme (default to light)
    _current_theme = 'light'

    # Color scheme (default to light)
    BACKGROUND = LIGHT_BACKGROUND
    GLASS_BACKGROUND = LIGHT_GLASS_BACKGROUND
    ACCENT_BLUE = LIGHT_ACCENT_BLUE
    ACCENT_LIGHT_BLUE = LIGHT_ACCENT_LIGHT_BLUE
    ACCENT_DARK_BLUE = LIGHT_ACCENT_DARK_BLUE
    BORDER_COLOR = LIGHT_BORDER_COLOR
    TEXT_COLOR = LIGHT_TEXT_COLOR
    SECONDARY_TEXT = LIGHT_SECONDARY_TEXT
    SUCCESS_COLOR = LIGHT_SUCCESS_COLOR
    WARNING_COLOR = LIGHT_WARNING_COLOR
    ERROR_COLOR = LIGHT_ERROR_COLOR
    HIGHLIGHT_COLOR = LIGHT_HIGHLIGHT_COLOR

    # Gradient colors
    BUTTON_GRADIENT_START = '#FFFFFF'
    BUTTON_GRADIENT_END = '#E8E8E8'
    BUTTON_HOVER_START = '#F0F8FF'
    BUTTON_HOVER_END = '#D0E8FF'

    # Shadow and glow effects
    SHADOW_COLOR = '#00000015'
    GLOW_COLOR = '#0078D440'

    @classmethod
    def set_theme(cls, theme):
        """Set the current theme (light or dark)"""
        cls._current_theme = theme
        
        if theme == 'dark':
            cls.BACKGROUND = cls.DARK_BACKGROUND
            cls.GLASS_BACKGROUND = cls.DARK_GLASS_BACKGROUND
            cls.ACCENT_BLUE = cls.DARK_ACCENT_BLUE
            cls.ACCENT_LIGHT_BLUE = cls.DARK_ACCENT_LIGHT_BLUE
            cls.ACCENT_DARK_BLUE = cls.DARK_ACCENT_DARK_BLUE
            cls.BORDER_COLOR = cls.DARK_BORDER_COLOR
            cls.TEXT_COLOR = cls.DARK_TEXT_COLOR
            cls.SECONDARY_TEXT = cls.DARK_SECONDARY_TEXT
            cls.SUCCESS_COLOR = cls.DARK_SUCCESS_COLOR
            cls.WARNING_COLOR = cls.DARK_WARNING_COLOR
            cls.ERROR_COLOR = cls.DARK_ERROR_COLOR
            cls.HIGHLIGHT_COLOR = cls.DARK_HIGHLIGHT_COLOR
            
            # Dark theme gradients
            cls.BUTTON_GRADIENT_START = '#404040'
            cls.BUTTON_GRADIENT_END = '#2D2D2D'
            cls.BUTTON_HOVER_START = '#1E3A5F'
            cls.BUTTON_HOVER_END = '#0F2A4F'
        else:
            cls.BACKGROUND = cls.LIGHT_BACKGROUND
            cls.GLASS_BACKGROUND = cls.LIGHT_GLASS_BACKGROUND
            cls.ACCENT_BLUE = cls.LIGHT_ACCENT_BLUE
            cls.ACCENT_LIGHT_BLUE = cls.LIGHT_ACCENT_LIGHT_BLUE
            cls.ACCENT_DARK_BLUE = cls.LIGHT_ACCENT_DARK_BLUE
            cls.BORDER_COLOR = cls.LIGHT_BORDER_COLOR
            cls.TEXT_COLOR = cls.LIGHT_TEXT_COLOR
            cls.SECONDARY_TEXT = cls.LIGHT_SECONDARY_TEXT
            cls.SUCCESS_COLOR = cls.LIGHT_SUCCESS_COLOR
            cls.WARNING_COLOR = cls.LIGHT_WARNING_COLOR
            cls.ERROR_COLOR = cls.LIGHT_ERROR_COLOR
            cls.HIGHLIGHT_COLOR = cls.LIGHT_HIGHLIGHT_COLOR
            
            # Light theme gradients
            cls.BUTTON_GRADIENT_START = '#FFFFFF'
            cls.BUTTON_GRADIENT_END = '#E8E8E8'
            cls.BUTTON_HOVER_START = '#F0F8FF'
            cls.BUTTON_HOVER_END = '#D0E8FF'

    @classmethod
    def get_current_theme(cls):
        """Get the current theme name"""
        return cls._current_theme

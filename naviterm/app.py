"""Main application class for Naviterm."""

from textual.app import App
from .screens import LoginScreen


class NavitermApp(App):
    """A basic Textualize TUI application."""

    def on_mount(self) -> None:
        """Set up the initial screen when the app starts."""
        self.push_screen(LoginScreen())


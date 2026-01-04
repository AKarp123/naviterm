"""Main application class for Naviterm."""

from textual.app import App
from textual.logging import TextualHandler
from .screens import LoginScreen
import logging

logging.basicConfig(level=logging.DEBUG, handlers=[TextualHandler()])
logger = logging.getLogger(__name__)


class NavitermApp(App):
    """A basic Textualize TUI application."""

    def on_mount(self) -> None:
        """Set up the initial screen when the app starts."""
        logger.debug("Starting NavitermApp")
        self.push_screen(LoginScreen())

    def on_login_screen_ping_result(self, event: LoginScreen.PingResult) -> None:
        """Handle ping result from login screen."""
        logger.debug(f"Ping result: {event.result}")
        self.stop()
        self.exit()


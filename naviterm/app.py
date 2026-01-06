"""Main application class for Naviterm."""

from textual.app import App
from textual.logging import TextualHandler

from naviterm.config import load_config
from .screens import LoginScreen
import logging
from typing import Optional
from .musicapi.connection import subsonic_conection
from .screens.AllAlbumsView import AllAlbumsView
logging.basicConfig(level=logging.DEBUG, handlers=[TextualHandler()])
logger = logging.getLogger(__name__)


class NavitermApp(App):
    """A basic Textualize TUI application."""
    
    def __init__(self):
        super().__init__()
        self.connection : Optional[subsonic_conection] = None

    def on_mount(self) -> None:
        """Set up the initial screen when the app starts."""
        logger.debug("Starting NavitermApp")
        config = load_config()
        if config.get("username") and config.get("password") and config.get("server_url"):
            self.connection = subsonic_conection(config.get("server_url"), config.get("username"), config.get("password"))
            ping_result = self.connection.ping()
            if ping_result:
                self.push_screen(AllAlbumsView())
            else:
                self.push_screen(LoginScreen())
        else:
            self.push_screen(LoginScreen())

    def on_login_screen_ping_result(self, event: LoginScreen.PingResult) -> None:
        """Handle ping result from login screen."""
        logger.debug(f"Ping result: {event.result}")
        if event.result:
            logger.debug("Pushing AllAlbumsView")
            self.push_screen(AllAlbumsView())
        else:
            logger.error("Login failed, staying on login screen")


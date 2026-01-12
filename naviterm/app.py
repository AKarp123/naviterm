"""Main application class for Naviterm."""

from textual.app import App
from textual.logging import TextualHandler

from naviterm.config import load_config
from .screens import LoginScreen, AllAlbumsView, AlbumView
import logging
from typing import Optional
from libopensonic.connection import Connection

logging.basicConfig(level=logging.DEBUG, handlers=[TextualHandler()])
logger = logging.getLogger(__name__)


class NavitermApp(App):
    """A basic Textualize TUI application."""
    
  
    

    
    def __init__(self):
        super().__init__()
        self.connection : Optional[Connection] = None

    def on_mount(self) -> None:
        """Set up the initial screen when the app starts."""
        self.theme = "catppuccin-mocha"
        logger.debug("Starting NavitermApp")
        config = load_config()
        if config.get("username") and config.get("password") and config.get("server_url"):
            self.connection = Connection(base_url=config.get("server_url"), username=config.get("username"), password=config.get("password"), app_name="Naviterm", port=443)
            try:
                self.connection.ping()
                self.push_screen(AllAlbumsView())
            except Exception as e:
                logger.error(f"Error pinging server: {e}")
                self.push_screen(LoginScreen())
            
            


    


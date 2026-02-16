"""Main application class for Naviterm."""

from naviterm.screens.NowPlaying import NowPlaying
from naviterm.player import Player
from textual.app import App
from textual.logging import TextualHandler

from naviterm.config import load_config
from .screens import LoginScreen, Layout
import logging
from typing import Optional
from libopensonic.async_connection import AsyncConnection
from os import listdir, remove
from pathlib import Path
from platformdirs import user_cache_dir

logging.basicConfig(level=logging.DEBUG, handlers=[TextualHandler()])
logger = logging.getLogger(__name__)






class NavitermApp(App):
    """A basic Textualize TUI application."""
    
  
    BINDINGS = [
        ("n", "toggle_now_playing()", "Toggle Now Playing"),
    ]

    
    def __init__(self):
        super().__init__()
        self.connection : Optional[AsyncConnection] = None
        self.player : Optional[Player] = None

    async def on_mount(self) -> None:
        """Set up the initial screen when the app starts."""
        self.theme = "catppuccin-mocha"
        logger.debug("Starting NavitermApp")
        config = load_config()
        if config.get("username") and config.get("password") and config.get("server_url"):
            self.connection = AsyncConnection(base_url=config.get("server_url", ""), username=config.get("username", ""), password=config.get("password", ""), app_name="Naviterm", port=443)
            try:
                await self.connection.ping()
                self.player = Player(self.connection)
                self.push_screen(Layout())
            except Exception as e:
                logger.error(f"Error pinging server: {e}")
                res = self.push_screen(LoginScreen(), wait_for_dismiss=True)
                if not res:
                    self.exit()
                else:
                    logger.debug("Login successful, proceeding to main layout")
                    self.push_screen(Layout())


    def action_toggle_now_playing(self) -> None:
        """Toggle the Now Playing screen."""
        if self.screen_stack and self.screen_stack[-1].__class__.__name__ == "NowPlaying":
            self.pop_screen()
        else:
            self.push_screen(NowPlaying())
                
    def on_unmount(self) -> None:
        assert self.player is not None
        """Clean up on app exit."""
        self.player.save_config()
        for file in listdir("music"):
            
            remove(f"music/{file}")
                
    
            
            


    


from textual.widgets import Static
from textual.widget import Widget
from textual.app import ComposeResult
from textual.containers import Vertical, Container

from libopensonic.async_connection import AsyncConnection
from libopensonic.connection import AlbumID3
from typing import Optional
import logging
logger = logging.getLogger(__name__)  
class AlbumView(Widget):
    """Widget for viewing an album."""
    
    CSS = """
    #album-content {
        width: 100%;
        height: 100%;
        padding: 1;
        scrollbar-visibility: hidden;
    }
    
    #album-header {
        width: 100%;
        height: 3;
        content-align: center middle;
        text-style: bold;
        margin-bottom: 1;
    }
    """
    
    def __init__(self, album_id: str):
        super().__init__()
        self.album_id = album_id
        self.connection: AsyncConnection = self.app.connection
        self.album : Optional[AlbumID3] = None
        
        
        
    async def on_mount(self) -> None:
        self.album = await self.connection.get_album(album_id=self.album_id)
        if self.album is None:
            logger.error(f"Failed to get album with ID: {self.album_id}")
            return
        self.album_name = self.album.name
        
        container = self.query_one("#album-content", Container)
        await container.remove_children()
        await container.mount(Static(self.album.name, id="album-name"))
        
        
        
        
        
        
    def compose(self) -> ComposeResult:
        """Create child widgets for the album view widget."""
        with Vertical(id="album-view"):
            with Container(id="album-content"):
                yield Static("Loading...", id="album-loading")




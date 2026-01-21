from textual.widgets import Static
from textual.widget import Widget
from textual.app import ComposeResult
from textual.containers import Vertical

from libopensonic.connection import Connection


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
        self.connection: Connection = self.app.connection
        self.album = self.connection.get_album(album_id=self.album_id)
        
    def compose(self) -> ComposeResult:
        """Create child widgets for the album view widget."""
        with Vertical(id="album-content"):
            yield Static("", id="album-header")
            # TODO: Add album tracks/songs here




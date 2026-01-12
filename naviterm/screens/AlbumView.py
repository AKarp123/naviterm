from textual.screen import Screen
from libopensonic.media.media_types import Album
from textual.app import ComposeResult
from textual.widgets import Header, Footer
from naviterm.musicapi.connection import SubsonicConnection
class AlbumView(Screen):
    """Screen for viewing an album."""
    
    CSS = """
    #album-table {
        width: 100%;
        height: 100%;
    }
    """
    
    def __init__(self, album_id: str):
        super().__init__()
        self.album_id = album_id
        self.album = self.connection.get_album(album_id)
        self.connection : SubsonicConnection = self.app.connection
        
    
        
    def compose(self) -> ComposeResult:
        """Create child widgets for the album view screen."""
        yield Header()
        yield Footer()
    
    def on_mount(self) -> None:
        self.title = f"🎵 {self.album.artist} - {self.album.name}"
	
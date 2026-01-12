from textual.widgets import Static
from textual.widget import Widget
from textual.app import ComposeResult
from textual.containers import Vertical
from naviterm.musicapi.connection import SubsonicConnection
from naviterm.screens.Layout import Layout


class AlbumViewWidget(Widget):
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
        self.connection: SubsonicConnection = None
        self.album = None
        
    def on_mount(self) -> None:
        """Load album data when widget is mounted."""
        if not hasattr(self.app, 'connection') or self.app.connection is None:
            raise RuntimeError("Connection not available")
        self.connection = self.app.connection
        
        self.album = self.connection.get_album(self.album_id)
        if self.album:
            header = self.query_one("#album-header", Static)
            header.update(f"🎵 {self.album.artist} - {self.album.name}")
    
    def compose(self) -> ComposeResult:
        """Create child widgets for the album view widget."""
        with Vertical(id="album-content"):
            yield Static("", id="album-header")
            # TODO: Add album tracks/songs here


class AlbumView(Layout):
    """Screen wrapper for AlbumView widget with Layout."""
    
    def __init__(self, album_id: str):
        self.album_widget = AlbumViewWidget(album_id)
        super().__init__(content_widget=self.album_widget)

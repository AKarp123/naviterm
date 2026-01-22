from textual.widgets import Static, DataTable
from textual.widget import Widget
from textual.app import ComposeResult
from textual.containers import Vertical, Container

from libopensonic.async_connection import AsyncConnection
from libopensonic.media.media_types import AlbumID3, Child
from typing import Optional
import logging
logger = logging.getLogger(__name__)  

mime_types = {
    "audio/mpeg": "mp3",
    "audio/flac": "flac",
    "audio/wav": "wav",
    "audio/aac": "aac",
    "audio/ogg": "ogg",
}


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
        
        table = self.query_one("#album-tracks-table", DataTable)
        table.cursor_type = "row"
        table.add_column("Track", width=6)
        table.add_column("Title", width=50)
        table.add_column("Duration", width=10)
        table.add_column("Type", width=10)
        table.add_column("Bitrate", width=10)
        
        container = self.query_one("#album-content", Container)
        await container.remove_children()
        await container.mount(table)
        if self.album.song:
            self.add_tracks_to_table(table, self.album.song)
        
    def add_tracks_to_table(self, table: DataTable, tracks: list[Child]) -> None:
        for i, track in enumerate(tracks):
            table.add_row(i + 1, track.title, self.format_duration(track.duration or 0), mime_types.get(track.content_type or "", "unknown"), f"{track.bit_rate} kbps")
            
    def format_duration(self, seconds: int) -> str:
        minutes = seconds // 60
        remaining_seconds = seconds % 60
        return f"{minutes}:{remaining_seconds:02d}"
        
    def compose(self) -> ComposeResult:
        """Create child widgets for the album view widget."""
        with Vertical(id="album-view"):
            with Container(id="album-content"):
                yield Static("Loading...", id="album-loading")
                yield DataTable(id="album-tracks-table")




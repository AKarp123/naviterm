import asyncio
from functools import reduce
from textual.events import Key
from textual.widgets import Static, DataTable
from textual.widget import Widget
from textual.app import ComposeResult
from textual.containers import Vertical, Container

from libopensonic.async_connection import AsyncConnection
from libopensonic.media.media_types import AlbumID3, Child
from typing import Optional
import logging
logger = logging.getLogger(__name__)  
from textual import log
from just_playback import Playback

mime_types = {
    "audio/mpeg": "mp3",
    "audio/flac": "flac",
    "audio/wav": "wav",
    "audio/aac": "aac",
    "audio/ogg": "ogg",
}


class AlbumView(Widget):
    """Widget for viewing an album."""
    

    DEFAULT_CSS = """
    #album-content {
        border: solid round white;
        width: 100%;
        scrollbar-visibility: hidden;

    }
    
    
    #album-content > DataTable > Header {
        background: transparent;
    }
    
    
    
    #album-header {
        width: 100%;
        height: auto;
        text-style: bold;
        border: solid round white;
    }
    #album-header > * {
        margin-left: 1;
    }
    

    #album-content > DataTable > .datatable--header,
    #album-content > DataTable > .datatable--header-hover,
    #album-content > DataTable > .datatable--header-cursor {
        background: transparent !important;
        color: $text;
        text-style: bold;
    }
    #album-content > DataTable {
        background: transparent;
    }
    """
    
    def __init__(self, album_id: str):
        super().__init__()
        self.album_id = album_id
        self.connection: AsyncConnection = self.app.connection #type: ignore
        self.album : Optional[AlbumID3] = None
        self.player = Playback()
        
        
        
    async def on_mount(self) -> None:
        self.album = await self.connection.get_album(album_id=self.album_id)
        if self.album is None:
            logger.error(f"Failed to get album with ID: {self.album_id}")
            return

        self.update_header()
        self.update_border_titles()
        
        table = self.query_one("#album-tracks-table", DataTable)
        table.cursor_type = "row"
        table.add_column("Track", width=6)
        needs_artist = any(
            track.artist != (self.album.artist if self.album else None)
            for track in self.album.song or []
        )
        if needs_artist:
            table.add_column("Artist",key="Artist", width=30)
        table.add_column("Title", width=50)
        table.add_column("Duration", width=10)
        table.add_column("Type", width=10)
        table.add_column("Bitrate", width=10)
        
        container = self.query_one("#album-content", Container)
        container.border_title = "Tracks"
        await container.remove_children()
        await container.mount(table)
        table.focus()
        if self.album.song:
            self.add_tracks_to_table(table, self.album.song)
                 
    def update_header(self) -> None:
        header_container = self.query_one("#album-header", Container)
        header_container.remove_children()
        header_container.mount(Static(f"Album: {self.album.name if self.album else 'Loading...'}", id="album-title"))
        header_container.mount(Static(f"Album Artist: {self.album.artist if self.album else 'Loading...'}", id="album-artist"))
        header_container.mount(Static(f"Duration: {self.format_duration(self.album.duration or 0) if self.album else 'Loading...'}", id="album-duration"))
        header_container.mount(Static(f"Year: {self.album.year if self.album and self.album.year else 'Unknown'}", id="album-year"))

        if self.album and self.album.genres:
            genres_str = reduce(
            lambda acc, g: acc + ", " + g.name,
            self.album.genres,
            ""
            ).lstrip(", ")
            header_container.mount(Static(f"Genres: {genres_str}", id="album-genres"))
            
        
        
    def update_border_titles(self) -> None:
        header = self.query_one("#album-header", Container)
        header.border_title = 'Album Info'
        body = self.query_one("#album-content", Container)
        body.border_title = 'Tracks'
        
        
    def add_tracks_to_table(self, table: DataTable, tracks: list[Child]) -> None:
        has_artist = "Artist" in table.columns
        for i, track in enumerate(tracks):
            if has_artist:
                table.add_row(
                    i + 1,
                    track.artist or (self.album.artist if self.album else "Unknown Artist"),
                    track.title,
                    self.format_duration(track.duration or 0),
                    mime_types.get(track.content_type or "", "unknown"),
                    f"{track.bit_rate} kbps",
                )

            else:
                table.add_row(
                    i + 1,
                    track.title,
                    self.format_duration(track.duration or 0),
                    mime_types.get(track.content_type or "", "unknown"),
                    f"{track.bit_rate} kbps"
                )
                
    async def on_key(self, event: Key) -> None:
        if event.key == "enter":
            table = self.query_one("#album-tracks-table", DataTable)
        
                
                
    def format_duration(self, seconds: int) -> str:
        minutes = seconds // 60
        remaining_seconds = seconds % 60
        return f"{minutes}:{remaining_seconds:02d}"
        
    def compose(self) -> ComposeResult:
        """Create child widgets for the album view widget."""
        with Vertical(id="album-view"):
            with Container(id="album-header"):
                yield Static("Loading...")

            with Container(id="album-content"):
                yield Static("Loading...", id="album-loading")
                yield DataTable(id="album-tracks-table")




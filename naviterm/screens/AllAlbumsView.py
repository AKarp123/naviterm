from textual.events import Key
from textual.screen import Screen
from textual.widgets import Header, Footer, DataTable
from textual.app import ComposeResult

import logging

from naviterm.musicapi.connection import subsonic_conection
from libopensonic.media.media_types import Album
logger = logging.getLogger(__name__)

class AllAlbumsView(Screen):
    """Screen for viewing all albums."""
    
    CSS = """
    #albums-table {
        width: 100%;
        height: 100%;
    }
    """
    
    def __init__(self):
        super().__init__()
        self.connection : subsonic_conection = self.app.connection
        albums_result = self.connection.get_all_albums()
        self.albums : list[Album] = albums_result if albums_result else []
        self.albums_offset = 0


    def compose(self) -> ComposeResult:
        """Create child widgets for the album view screen."""
        yield Header()
        table = DataTable(id="albums-table")
        table.cursor_type = "row"
        # Set column widths: Artist gets more space, Album is smaller, Year is minimal
        table.add_column("Artist", width=27)
        table.add_column("Album", width=40)
        table.add_column("Year", width=8)
        table.add_column("Added", width=12)
        
        # Populate table with album data
        for album in self.albums:
            artist = album.artist or "Unknown"
            album_name = album.name or "Unknown"
            year = str(album.year) if album.year else "Unknown"
            created = album.created.split("T")[0] if album.created else "Unknown"
            table.add_row(artist, album_name, year, created)
        
        yield table
        yield Footer()
        
    def on_mount(self) -> None:
        self.title = "🎵 All Albums"
        
    def on_key(self, event: Key) -> None:
        """Handle key events."""
        table = self.query_one("#albums-table", DataTable)
        if event.key == "down":
            if table.cursor_row < table.row_count - 1:
                table.action_cursor_down()
            else:
                self.albums_offset += 50
                new_albums = self.connection.get_all_albums(self.albums_offset)
                if new_albums:
                    self.albums += new_albums
                    for album in new_albums:
                        artist = album.artist or "Unknown"
                        album_name = album.name or "Unknown"
                        year = str(album.year) if album.year else "Unknown"
                        created = album.created.split("T")[0] if album.created else "Unknown"
                        table.add_row(artist, album_name, year, created)
                self.compose()
            event.stop()
                
  
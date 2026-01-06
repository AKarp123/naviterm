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
        logger.debug(f"Albums: {self.albums}")

    def compose(self) -> ComposeResult:
        """Create child widgets for the album view screen."""
        yield Header()
        table = DataTable(id="albums-table")
        table.add_columns("Artist", "Album", "Year")
        
        logger.debug(f"Albums: {self.albums}")
        # Populate table with album data
        for album in self.albums:
            artist = album.artist or "Unknown"
            album_name = album.name or "Unknown"
            year = str(album.year) if album.year else "Unknown"
            table.add_row(artist, album_name, year)
        
        yield table
        yield Footer()
        
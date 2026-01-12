from textual.events import Key
from textual.widgets import DataTable
from textual.app import ComposeResult
from textual.widget import Widget
import logging

from naviterm.musicapi.connection import SubsonicConnection
from libopensonic.media.media_types import Album
from naviterm.screens.Layout import Layout
logger = logging.getLogger(__name__)

class AllAlbumsViewWidget(Widget):
    """Widget for viewing all albums."""
    
    CSS = """
    #albums-table {
        width: 100%;
        height: 100%;
        border: solid round white;
        scrollbar-visibility: hidden;
        
    }
    """
    
    def __init__(self):
        super().__init__()
        self.albums_offset = 0
        self.connection: SubsonicConnection = None
        
    def on_mount(self) -> None:
        if not hasattr(self.app, 'connection') or self.app.connection is None:
            raise RuntimeError("Connection not available")
        self.connection = self.app.connection
        
        table = self.query_one("#albums-table", DataTable)
        table.cursor_type = "row"
        # Set column widths: Artist gets more space, Album is smaller, Year is minimal
        table.add_column("Artist", width=27)
        table.add_column("Album", width=40)
        table.add_column("Year", width=8)
        table.add_column("Added", width=12)
        
        # Add albums to the table
        albums = self.get_albums(0)
        self.add_albums_to_table(table, albums)

    def get_albums(self, offset: int = 0) -> list[Album]:
        """Get all albums from the server."""
        albums = self.connection.get_all_albums(offset)
        if albums is False or albums is None:
            logger.error("Failed to get albums")
            return []
        return albums
    
    def add_albums_to_table(self, table: DataTable, albums: list[Album]) -> None:
        """Add albums to the table."""
        for album in albums:
            artist = album.artist or "Unknown"
            album_name = album.name or "Unknown"
            year = str(album.year) if album.year else "Unknown"
            created = album.created.split("T")[0] if album.created else "Unknown"
            table.add_row(artist, album_name, year, created, key=album.id)

    def view_album(self) -> None:
        """View an album."""
        table = self.query_one("#albums-table", DataTable)
        if table.cursor_row is None:
            logger.warning("No row selected")
            return
        
        album_id = table.get_row_key(table.cursor_row)
        if album_id is None:
            logger.error("Could not get album ID for selected row")
            return
        
        logger.debug(f"Viewing album with ID: {album_id}")
        from naviterm.screens.AlbumView import AlbumView
        self.app.push_screen(AlbumView(album_id))

    def compose(self) -> ComposeResult:
        """Create child widgets for the album view widget."""
        yield DataTable(id="albums-table")

    def load_more_albums(self) -> None:
        """Load more albums when reaching the end of the table."""
        table = self.query_one("#albums-table", DataTable)
        self.albums_offset += 50
        new_albums = self.get_albums(self.albums_offset)
        if new_albums:
            self.add_albums_to_table(table, new_albums)
            logger.debug(f"Loaded {len(new_albums)} more albums")
        
    def on_key(self, event: Key) -> None:
        """Handle key events."""
        if event.key == "down":
            table = self.query_one("#albums-table", DataTable)
            # Check if we're at the last row
            if table.cursor_row == table.row_count - 1:
                self.load_more_albums()
                # Only stop event if we actually loaded more albums
                if table.cursor_row < table.row_count - 1:
                    event.stop()
        elif event.key == "enter":
            self.view_album()
            event.stop()


class AllAlbumsView(Layout):
    """Screen wrapper for AllAlbumsView widget with Layout."""
    
    BINDINGS = [
        ("enter", "view_album", "View album"),
    ]
    
    def __init__(self):
        self.albums_widget = AllAlbumsViewWidget()
        super().__init__(content_widget=self.albums_widget)
    
    def action_view_album(self) -> None:
        """View an album."""
        self.albums_widget.view_album()
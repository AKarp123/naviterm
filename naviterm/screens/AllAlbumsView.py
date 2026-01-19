import asyncio
from textual.events import Key
from textual.widgets import DataTable
from textual.app import ComposeResult
from textual.widget import Widget
import logging
from naviterm.screens.AlbumView import AlbumView
from libopensonic.connection import Connection
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
        self.connection: Connection = self.app.connection
        self.loading_more_albums = False
        
    def on_mount(self) -> None:
        table = self.query_one("#albums-table", DataTable)
        table.cursor_type = "row"
        # Set column widths: Artist gets more space, Album is smaller, Year is minimal
        table.add_column("Artist", width=27)
        table.add_column("Album", width=40)
        table.add_column("Year", width=8)
        table.add_column("Added", width=12)
        
        # Add albums to the table
        
        albums = self.get_albums(count=self.app.size.height, offset=0)
        self.add_albums_to_table(table, albums)

    def get_albums(self, count: int = 50, offset: int = 0) -> list[Album]:
        """Get all albums from the server."""
        print(f"Getting albums with count: {count} and offset: {offset}")
        albums = self.connection.get_album_list(ltype="newest", size=count, offset=offset)
        if albums is False or albums is None:
            logger.error("Failed to get albums")
            return []
        
        return albums
    
    def add_albums_to_table(self, table: DataTable, albums: list[Album]) -> None:
        """Add albums to the table."""
        for album in albums:
            artist = album.artist.replace("\u200b", "") or "Unknown"
            album_name = album.name.replace("\u200b", "") or "Unknown"
            year = str(album.year) if album.year else "Unknown"
            created = album.created.split("T")[0] if album.created else "Unknown"
            
            table.add_row(artist, album_name, year, created, key=album.id)
        
        self.albums_offset += len(albums)
        print(f"Albums offset: {self.albums_offset}")
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

        self.app.push_screen(AlbumView(album_id))

    def compose(self) -> ComposeResult:
        """Create child widgets for the album view widget."""
        yield DataTable(id="albums-table")

    async def load_more_albums(self) -> None:
        """Load more albums when reaching the end of the table."""
        self.loading_more_albums = True
        table = self.query_one("#albums-table", DataTable)
        print(f"Loading more albums with offset: {self.albums_offset}")
        new_albums = await asyncio.to_thread(self.get_albums, offset=self.albums_offset, )
        if new_albums:
            self.add_albums_to_table(table, new_albums)
            logger.debug(f"Loaded {len(new_albums)} more albums")
        self.loading_more_albums = False
    def on_key(self, event: Key) -> None:
        """Handle key events."""
        if event.key == "down":
            table = self.query_one("#albums-table", DataTable)
            # Check if we're close to the bottom of the table
            if table.cursor_row >= table.row_count - 10 and not self.loading_more_albums:
                self.run_worker(self.load_more_albums)
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
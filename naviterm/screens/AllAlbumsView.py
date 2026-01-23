from textual.events import Key
from textual.widgets import DataTable
from textual.app import ComposeResult
from textual.widget import Widget
import logging
from libopensonic.async_connection import AsyncConnection
from libopensonic.media.media_types import Album
from textual.message import Message
logger = logging.getLogger(__name__)

class AllAlbumsView(Widget):
    """Widget for viewing all albums.
    
    TODO: Implement caching to prevent flash when hitting back button.
    
    """
    
    CSS = """
    #albums-table {
        width: 100%;
        height: 100%;
        border: solid round white;
        scrollbar-visibility: hidden;
        
    }
    """
    
    class Selected(Message):
        """Message emitted when an album is selected."""
        def __init__(self, album_id: str):
            super().__init__()
            self.album_id = album_id
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.albums_offset = 0
        self.connection: AsyncConnection = self.app.connection
        self.albums : list[Album] = []
        self.loading_more_albums = False
        self.table_row = 0
        
    async def on_mount(self) -> None:
        table = self.query_one("#albums-table", DataTable)
        table.focus()
        table.cursor_type = "row"
        # Set column widths: Artist gets more space, Album is smaller, Year is minimal
        table.add_column("Artist", width=27)
        table.add_column("Album", width=40)
        table.add_column("Year", width=8)
        table.add_column("Added", width=12)
        
        # Add albums to the table
        
        if( len(self.albums) == 0): #only refetch if we have no albums (first load)
            albums = await self.get_albums(count=self.app.size.height, offset=self.albums_offset)
            self.albums.extend(albums)
            self.albums_offset = len(self.albums)
        
        self.add_albums_to_table(table, self.albums)
        table.move_cursor(row=self.table_row)

        

    async def get_albums(self, count: int = 50, offset: int = 0) -> list[Album]:
        """Get all albums from the server."""
        print(f"Getting albums with count: {count} and offset: {offset}")
        albums = await self.connection.get_album_list(ltype="newest", size=count, offset=offset)
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
        
        print(f"Albums offset: {self.albums_offset}")
    def view_album(self) -> None:
        """View an album."""
        table = self.query_one("#albums-table", DataTable)
        if table.cursor_row is None:
            logger.warning("No row selected")
            return

        # Textual's DataTable doesn't expose get_row_key() in older versions.
        # We can map the visible row index to its RowKey via ordered_rows.
        try:
            album_id = table.ordered_rows[table.cursor_row].key.value
        except Exception:
            logger.error("Could not get album ID for selected row")
            return

        logger.debug("Viewing album with ID: %s", album_id)
        self.post_message(self.Selected(album_id))


    async def load_more_albums(self) -> None:
        """Load more albums when reaching the end of the table."""
        self.loading_more_albums = True
        table = self.query_one("#albums-table", DataTable)
        print(f"Loading more albums with offset: {self.albums_offset}")
        new_albums = await self.get_albums(offset=self.albums_offset)
        self.albums.extend(new_albums)
        self.albums_offset = len(self.albums)
        if new_albums:
            self.add_albums_to_table(table, new_albums)
            
            logger.debug(f"Loaded {len(new_albums)} more albums")
        self.loading_more_albums = False
        
    
    
    def on_data_table_row_highlighted(self, event: DataTable.RowHighlighted) -> None:
        """Handle row highlighted event to load more albums if needed."""
        table = self.query_one("#albums-table", DataTable)
        self.table_row = event.cursor_row
        if (
            table.row_count > 10 and
            event.cursor_row >= table.row_count - 3 and
            not self.loading_more_albums
        ):
            self.run_worker(self.load_more_albums)
        
    
    def on_key(self, event: Key) -> None:
        """Handle key events."""
        if event.key == "enter":
            self.view_album()
            event.stop()
    
    
    
            
    def compose(self) -> ComposeResult:
        """Create child widgets for the album view widget."""
        yield DataTable(id="albums-table")



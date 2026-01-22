from textual.app import ComposeResult
from textual.events import Key
from textual.message import Message
from textual.widget import Widget
from textual.widgets import DataTable

import logging
logger = logging.getLogger(__name__)


OPTIONS = [
    "Recently Added",
    "Songs",
    "Playlists",
    "Artists",
    
    
]


class Sidebar(Widget):
    """A sidebar widget."""

    def __init__(self):
        super().__init__()

    CSS = """
    Sidebar {
        width: 20%;
        height: 100%;
        border: solid round white;
        scrollbar-visibility: hidden;
    }
    
    #sidebar-table {
        scrollbar-visibility: hidden;
    }
    """

    def on_mount(self) -> None:
        table = self.query_one("#sidebar-table", DataTable)
        table.cursor_type = "row"
        table.add_column("Options", width=21)
        for option in OPTIONS:
            table.add_row(option, key=option)
            
    class SidebarOptionSelected(Message):
        """Message emitted when a sidebar option is selected."""

        def __init__(self, option: str):
            super().__init__()
            self.option = option

    def on_data_table_row_highlighted(self, event: DataTable.RowHighlighted) -> None:
        """Handle row highlighting."""
        logger.debug(f"Row highlighted: {event.row_key.value}")
        self.post_message(self.SidebarOptionSelected(event.row_key.value))
        

    def compose(self) -> ComposeResult:
        yield DataTable(id="sidebar-table")
from textual.app import ComposeResult
from textual.events import Key
from textual.message import Message
from textual.widget import Widget
from textual.widgets import DataTable


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

    def on_key(self, event: Key) -> None:
        """Handle key events."""
        if event.key in {"down", "up", "enter"}:
            table = self.query_one("#sidebar-table", DataTable)
            # Ensure a row is selected; default to first row
            if table.cursor_row is None:
                table.cursor_coordinate = (0, 0)
            cursor_row = table.cursor_row
            if cursor_row is not None and 0 <= cursor_row < len(OPTIONS):
                self.post_message(self.SidebarOptionSelected(OPTIONS[cursor_row]))
            event.stop()
        

    def compose(self) -> ComposeResult:
        yield DataTable(id="sidebar-table")
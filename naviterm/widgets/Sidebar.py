from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import DataTable


OPTIONS = [
    "Recently Added Albums",
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

    def compose(self) -> ComposeResult:
        yield DataTable(id="sidebar-table")
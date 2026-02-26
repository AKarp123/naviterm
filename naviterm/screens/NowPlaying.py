from textual.app import ComposeResult
from textual.screen import Screen
from textual.containers import Vertical
from textual.widgets import DataTable, Footer, Static
from naviterm.player.util import format_duration



class NowPlaying(Screen):
    """Screen to display the currently playing track."""
 
    CSS = """
    Screen {
        align: center middle;
    }
    
    #now-playing-container {
        height: auto;
        align: center middle;
        border: round white;
        padding: 2;
    }
 
    #queue-container {
        border: round white;
    }
    
    #title {
        width: 100%;
        height: 3;
        content-align: center middle;
        text-style: bold;
        margin-bottom: 2;
    }
    
    #queue-table {
        width: 100%;
        background: transparent;
        scrollbar-visibility: hidden;
    }
    
    #queue-table > .datatable--header,
    #queue-table > .datatable--header-hover,
    #queue-table > .datatable--header-cursor {
        background: transparent !important;
        color: $text;
        text-style: bold;
    }
    
 
 
    """
    
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
 
    def compose(self) -> ComposeResult:
        """Compose the Now Playing screen."""
        with Vertical(id="now-playing-container"):
            yield Static("Now Playing", id="title")
            # Additional now playing details would go here
        with Vertical(id="queue-container"):
            yield DataTable(id="queue-table")
            
        yield Footer()
        
    
   
   
    def on_mount(self) -> None:
       self.query_one("#now-playing-container").border_title = "Now Playing"
       self.query_one("#queue-container").border_title = "Up Next"
       queue_table = self.query_one("#queue-table", DataTable)
       queue_table.cursor_type = "row"
       queue_table.add_column("Title", width=30)
       queue_table.add_column("Artist", width=30)
       queue_table.add_column("Album", width=30)
       queue_table.add_column("Duration", width=10)
       
       for i, track in enumerate(self.app.player.tracks[self.app.player.current_index:]): #type: ignore
           queue_table.add_row(track.title, track.artist, track.album, format_duration(track.duration), label=str(i))
        
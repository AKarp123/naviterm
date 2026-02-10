from textual.app import ComposeResult
from textual.screen import Screen
from textual.containers import Vertical
from textual.widgets import Footer, Static



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
        padding: 1;
    }
    
    #title {
        width: 100%;
        height: 3;
        content-align: center middle;
        text-style: bold;
        margin-bottom: 2;
    }
 
 
    """
 
    def compose(self) -> ComposeResult:
        """Compose the Now Playing screen."""
        with Vertical(id="now-playing-container"):
            yield Static("Now Playing", id="title")
            # Additional now playing details would go here
        with Vertical(id="queue-container"):
            yield Static("Up Next:", id="up-next-title")
            # Queue details would go here
            
        yield Footer()
   
   
    def on_mount(self) -> None:
       self.query_one("#now-playing-container").border_title = "Now Playing"
       self.query_one("#queue-container").border_title = "Up Next"
from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Header, Footer, Input, Static


class NavitermApp(App):
    """A basic Textualize TUI application."""

    CSS = """
    Screen {
        align: center middle;
    }
    
    #form-container {
        width: 66%;
        max-width: 66%;
        height: auto;
        align: center middle;
    }
    
    #title {
        width: 100%;
        height: 3;
        content-align: center middle;
        text-style: bold;
        margin-bottom: 2;
    }
    
    Input {
        width: 100%;
        margin-bottom: 1;
    }
    
    .label {
        width: 100%;
        margin-bottom: 1;
    }
    """

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        with Container(id="form-container"):
            yield Static("Naviterm", id="title")
            yield Static("", classes="label")
            yield Static("Server URL:", classes="label")
            yield Input(placeholder="Enter server URL", id="server-url")
            yield Static("Username:", classes="label")
            yield Input(placeholder="Enter username", id="username")
            yield Static("Password:", classes="label")
            yield Input(placeholder="Enter password", id="password", password=True)
        yield Footer()





if __name__ == "__main__":
    app = NavitermApp()
    app.run()

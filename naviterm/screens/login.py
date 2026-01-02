"""Login screen for Naviterm."""

from textual.containers import Container, Vertical
from textual.screen import Screen
from textual.widgets import Header, Footer, Input, Static, Button
from textual.app import ComposeResult
from ..config import load_config, save_config


class LoginScreen(Screen):
    """Login screen for entering server credentials."""

    CSS = """
    Screen {
        align: center middle;
    }
    
    Vertical {
        align: center middle;
        width: 100%;
        height: 100%;
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

    def __init__(self):
        super().__init__()
        config = load_config()
        self.username = config.get("username", "")
        self.password = config.get("password", "")
        self.server_url = config.get("server_url", "")

    def compose(self) -> ComposeResult:
        """Create child widgets for the login screen."""
        yield Header()
        with Vertical():
            with Container(id="form-container"):
                yield Static("Naviterm Setup", id="title")
                yield Static("", classes="label")
                yield Input(placeholder="Enter server URL", id="server-url", value=self.server_url)
                yield Input(placeholder="Enter username", id="username", value=self.username)
                yield Input(placeholder="Enter password", id="password", password=True, value=self.password)
                yield Button("Login", id="login-button", variant="primary")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press events."""
        if event.button.id == "login-button":
            self.login()

    def login(self):
        """Handle login: save credentials and exit."""
        self.username = self.query_one("#username", Input).value
        self.password = self.query_one("#password", Input).value
        self.server_url = self.query_one("#server-url", Input).value
        save_config(self.username, self.password, self.server_url)
        self.app.exit()


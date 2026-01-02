from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Header, Footer, Input, Static, Button
from platformdirs import user_config_dir
import os
import json
config_dir = user_config_dir("naviterm", appauthor=False)
config_file = os.path.join(config_dir, "config.json")


    
def load_config() -> dict:
    config = {}
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
    if not os.path.exists(config_file):
        with open(config_file, "w") as f:
            json.dump({}, f)

    with open(config_file, "r") as f:
        config = json.load(f)
    return config

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
    
    def __init__(self):
        super().__init__()
        config = load_config()
        self.username = config.get("username", "")
        self.password = config.get("password", "")
        self.server_url = config.get("server_url", "")

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        with Container(id="form-container"):
            yield Static("Naviterm Setup", id="title")
            yield Static("", classes="label")
            yield Input(placeholder="Enter server URL", id="server-url", value=self.server_url)
            yield Input(placeholder="Enter username", id="username", value=self.username)
            yield Input(placeholder="Enter password", id="password", password=True, value=self.password)
            yield Button("Login", id="login-button", variant="primary")
        yield Footer()
        
    def save_config(self):
        with open(config_file, "w") as f:
            json.dump({"username": self.username, "password": self.password, "server_url": self.server_url}, f)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press events."""
        if event.button.id == "login-button":
            self.login()

    def login(self):
        self.username = self.query_one("#username", Input).value
        self.password = self.query_one("#password", Input).value
        self.server_url = self.query_one("#server-url", Input).value
        self.save_config()
        self.exit()


def main():
    app = NavitermApp()
    app.run()


if __name__ == "__main__":
    main()


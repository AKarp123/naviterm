from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Button, Static


class NavitermApp(App):
    """A basic Textualize TUI application."""

    CSS = """
    Screen {
        align: center middle;
    }
    
    #greeting {
        width: 50;
        height: 3;
        border: solid $primary;
        content-align: center middle;
    }
    """

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Static("Welcome to Naviterm!", id="greeting")
        yield Button("Click me!", id="click-button", variant="primary")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press events."""
        if event.button.id == "click-button":
            self.query_one("#greeting", Static).update("Button was clicked!")


def main():
    app = NavitermApp()
    app.run()


if __name__ == "__main__":
    main()

"""Layout screen that contains Sidebar and content area."""

from textual.screen import Screen
from textual.containers import Horizontal, Container
from textual.app import ComposeResult
from textual.widgets import Footer
from naviterm.widgets.Sidebar import Sidebar
from textual.widget import Widget


class Layout(Screen):
    """A layout screen with Sidebar and content area."""
    
    BINDINGS = [
        ("b", "go_back()", "Go back")
    ]
    
    CSS = """
    Layout {
        layout: horizontal;
        margin: 1;
    }
    
    #sidebar-container {
        width: 25;
        min-width: 15;
        max-width: 40;
        height: 100%;
        border: solid round white;
        margin-right: 1;
        scrollbar-visibility: hidden;
    }
    
    #content-container {
        width: 1fr;
        height: 100%;
        layout: vertical;
        border: solid round white;
        scrollbar-visibility: hidden;
    }
    
    #content-container > * {
        width: 100%;
    }
    
    #content-container > .content-widget {
        height: 1fr;
    }
    
    #content-container > Footer {
        height: auto;
    }
    
    DataTable {
        scrollbar-visibility: hidden;
    }
    """
    
    def __init__(self, content_widget=None):
        """Initialize the layout with optional content widget.
        
        Args:
            content_widget: Optional widget to display in the content area.
        """
        super().__init__()
        self.history: list[Widget] = []
        self.content_widget = content_widget
    
    def compose(self) -> ComposeResult:
        """Create child widgets for the layout screen."""
        with Horizontal():
            with Container(id="sidebar-container"):
                yield Sidebar()
            
            with Container(id="content-container"):
                if self.content_widget:
                    self.content_widget.add_class("content-widget")
                    yield self.content_widget
            yield Footer(id="layout-footer")
    
    def set_content(self, widget: Widget) -> None:
        """Set the content widget in the content area.
        
        Args:
            widget: Widget to display in the content area.
        """
        content_container = self.query_one("#content-container", Container)
        footer = self.query_one("#layout-footer", Footer)
        # Remove existing content (except footer)
        self.history.append(self.content_widget)
        content_container.remove_children()
        # Add class to widget and mount before footer
        widget.add_class("content-widget")
        content_container.mount(widget, before=footer)
    
    def on_mount(self) -> None:
        """Called when the screen is mounted."""
        pass
    
    def action_go_back(self) -> None:
        """Go back to the previous screen."""
        if len(self.history) > 0:
            self.content_widget = self.history.pop()
            self.set_content(self.content_widget)
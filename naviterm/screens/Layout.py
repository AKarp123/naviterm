"""Layout screen that contains Sidebar and content area."""

from textual.screen import Screen
from textual.containers import Horizontal, Container
from textual.app import ComposeResult
from textual.widgets import Footer
from naviterm.widgets.Sidebar import Sidebar


class Layout(Screen):
    """A layout screen with Sidebar and content area."""
    
    CSS = """
    Layout {
        layout: horizontal;
    }
    
    #sidebar-container {
        width: 25;
        min-width: 15;
        max-width: 40;
        height: 100%;
        border-right: solid $primary;
    }
    
    #content-container {
        width: 1fr;
        height: 100%;
        layout: vertical;
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
    """
    
    def __init__(self, content_widget=None):
        """Initialize the layout with optional content widget.
        
        Args:
            content_widget: Optional widget to display in the content area.
        """
        super().__init__()
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
    
    def set_content(self, widget) -> None:
        """Set the content widget in the content area.
        
        Args:
            widget: Widget to display in the content area.
        """
        content_container = self.query_one("#content-container", Container)
        footer = self.query_one("#layout-footer", Footer)
        # Remove existing content (except footer)
        for child in list(content_container.children):
            if child.id != "layout-footer":
                child.remove()
        # Add class to widget and mount before footer
        widget.add_class("content-widget")
        content_container.mount(widget, before=footer)
    
    def on_mount(self) -> None:
        """Called when the screen is mounted."""
        pass

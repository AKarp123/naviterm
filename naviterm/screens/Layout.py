"""Layout screen that contains Sidebar and content area."""

import logging
from textual.screen import Screen
from textual.containers import Horizontal, Container
from textual.app import ComposeResult
from textual.widgets import Footer
from naviterm.widgets.Sidebar import Sidebar
from naviterm.screens.AllAlbumsView import AllAlbumsView
from naviterm.screens.AlbumView import AlbumView
from textual.reactive import reactive
class Layout(Screen):
    """A layout screen with Sidebar and content area."""
    
    BINDINGS = [
        ("b", "go_back()", "Go back"),
        ("s", "toggle_sidebar()", "Toggle sidebar")
    ]
    
    logger = logging.getLogger(__name__)
    
    
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


    .hidden {
        display: none;
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
    CONTENT_WIDGETS = {
        "AllAlbumsView": AllAlbumsView,
        "AlbumView": AlbumView,
    }
    
    hide_sidebar = reactive(False)
    
    def __init__(self, content_widget=None):
        """Initialize the layout with optional content widget.
        
        Args:
            content_widget: Optional widget to display in the content area.
        """
        super().__init__()
        self.history: list[str] = []
        self.content_widget : str = "AllAlbumsView"
    
    def compose(self) -> ComposeResult:
        """Create child widgets for the layout screen."""
        with Horizontal():
            with Container(id="sidebar-container"):
                yield Sidebar()
            
            with Container(id="content-container"):
                yield self.CONTENT_WIDGETS[self.content_widget]()
            yield Footer(id="layout-footer")
    
    def set_content(self, widget_name: str) -> None:
        """Set the content widget in the content area.
        
        Args:
            widget: Widget to display in the content area.
        """
        content_container = self.query_one("#content-container", Container)
        footer = self.query_one("#layout-footer", Footer)
        # Remove existing content (except footer)
        self.history.append(widget_name)
        content_container.remove_children()
        # Add class to widget and mount before footer

        content_container.mount(self.CONTENT_WIDGETS[widget_name](), before=footer)
    
    
    def on_mount(self) -> None:
        """Called when the screen is mounted."""
        pass
    
    def action_go_back(self) -> None:
        """Go back to the previous screen."""
        if len(self.history) > 0:
            self.content_widget = self.history.pop()
            self.set_content(self.content_widget)

    def on_sidebar_option_selected(self, message: Sidebar.SidebarOptionSelected) -> None:
        """Handle sidebar navigation to switch screens/content."""
        option = message.option
        self.content_widget = option
        self.set_content(self.content_widget)
        
    def watch_hide_sidebar(self, value: bool) -> None:
        sidebar_container = self.query_one("#sidebar-container", Container)

        if value:
            sidebar_container.add_class("hidden")
        else:
            sidebar_container.remove_class("hidden")
    def action_toggle_sidebar(self) -> None:
        self.hide_sidebar = not self.hide_sidebar
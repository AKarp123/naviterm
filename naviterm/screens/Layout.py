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
from textual.widget import Widget
from typing import Any
logger = logging.getLogger(__name__)



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
    
    def __init__(self):
        """Initialize the layout with optional content widget.
        
        Args:
            content_widget: Optional widget to display in the content area.
        """
        super().__init__()
        all_album_view = AllAlbumsView()
        self.history: list[Widget] = [all_album_view]
        self.content_widget : Widget = all_album_view
        

    
    
    
    def on_mount(self) -> None:
        """Called when the screen is mounted."""
        print(self.history)
        pass
    
    async def push_widget(self, widget: Widget) -> None:
        """Push a widget to the content area."""
        self.content_widget = widget
        
        await self.remove_widget()
        await self.set_widget(widget)
        self.history.append(widget)
    
    async def pop_widget(self) -> None:
        """Pop a widget from the content area."""
        if len(self.history) > 1:
            self.history.pop()  # Remove current widget
            self.content_widget = self.history[-1]  # Get previous widget
            await self.remove_widget()
            content_container = self.query_one("#content-container", Container)
            await content_container.mount(self.content_widget)
            print(self.history)
            
    async def set_widget(self, widget: Widget) -> None:
        """Set the current widget."""
        content_container = self.query_one("#content-container", Container)
        await self.remove_widget()
        await content_container.mount(widget)
    
    
    async def remove_widget(self) -> None:
        """Remove the current widget."""
        content_container = self.query_one("#content-container", Container)
        await content_container.remove_children()
    
    async def action_go_back(self) -> None:
        """Go back to the previous screen."""
        await self.pop_widget()

    async def on_sidebar_option_selected(self, message: Sidebar.SidebarOptionSelected) -> None:
        """Handle sidebar navigation to switch screens/content."""
        option = message.option
        self.content_widget = self.CONTENT_WIDGETS.get(option, AllAlbumsView())()
        await self.set_widget(self.content_widget)

    
    async def on_all_albums_view_selected(self, message: AllAlbumsView.Selected) -> None:
        """Handle album selection."""
        logger.debug(f"Album selected: {message.album_id}")
        self.content_widget = AlbumView(message.album_id)
        await self.push_widget(self.content_widget)
        
    def watch_hide_sidebar(self, value: bool) -> None:
        try: # Skip before the screen is mounted
            sidebar_container = self.query_one("#sidebar-container", Container)
        except Exception:
            return

        if value:
            sidebar_container.add_class("hidden")
        else:
            sidebar_container.remove_class("hidden")
    def action_toggle_sidebar(self) -> None:
        self.hide_sidebar = not self.hide_sidebar
        
    def check_action(self, action_name: str, parameters: tuple[object, ...]) -> bool:
        """Check if an action is valid in the current context."""
        if action_name == "go_back":
            return len(self.history) > 1
        return True
        
    def compose(self) -> ComposeResult:
        """Create child widgets for the layout screen."""
        with Horizontal():
            with Container(id="sidebar-container")  :
                yield Sidebar()
            
            with Container(id="content-container"):
                yield AllAlbumsView(id="AllAlbumsView")
            yield Footer(id="layout-footer")
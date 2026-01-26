from textual.app import ComposeResult
from textual.message import Message
from textual.widget import Widget
from textual.widgets import OptionList
from textual.containers import Container

import logging
logger = logging.getLogger(__name__)


OPTIONS = [
    "Recently Added",
    "Songs",
    "Playlists",
    "Artists",
    
    
]


class Sidebar(Widget):
    """A sidebar widget."""

    def __init__(self):
        super().__init__()


    DEFAULT_CSS = """
    #sidebar-widget {
        scrollbar-visibility: hidden;
        background: transparent;
    }

    #sidebar-options {
        background: transparent;
        border: none;
        padding: 0 1;
        scrollbar-visibility: hidden;
    }

    #sidebar-options > .option-list--option-highlighted {
        background: $block-cursor-blurred-background;
        color: $block-cursor-blurred-foreground;
        text-style: $block-cursor-blurred-text-style;
    }

    #sidebar-options:focus > .option-list--option-highlighted {
        background: $block-cursor-background;
        color: $block-cursor-foreground;
        text-style: $block-cursor-text-style;
    }
    """
    def on_mount(self) -> None:
        option_list = self.query_one("#sidebar-options", OptionList)
        option_list.set_options(OPTIONS)
        if OPTIONS:
            option_list.highlighted = 0
            
    class SidebarOptionSelected(Message):
        """Message emitted when a sidebar option is selected."""

        def __init__(self, option: str):
            super().__init__()
            self.option = option

    def on_option_list_option_highlighted(
        self, event: OptionList.OptionHighlighted
    ) -> None:
        """Handle option highlighting."""
        option_label = str(event.option.prompt)
        logger.debug(f"Option highlighted: {option_label}")
        self.post_message(self.SidebarOptionSelected(option_label))
        

    def compose(self) -> ComposeResult:
        yield OptionList(id="sidebar-options")

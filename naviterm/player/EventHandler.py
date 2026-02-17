from typing import Callable
import logging
logger = logging.getLogger(__name__)

class EventHandler:
    """This class is responsible for handling events from the player and updating the UI accordingly."""
    
    
    
    def __init__(self) -> None:
        self.events : dict[str, list[Callable]] = {} # Dictionary to store event names and their corresponding listeners
        
        
    def on(self, event_name: str, func: Callable) -> None:
        """Register an event listener for a specific event."""
        if event_name not in self.events:
            self.events[event_name] = []
        self.events[event_name].append(func)
        
    
    def emit(self, event_name: str, *args, **kwargs) -> None:
        """Emit an event and call all registered listeners for that event."""
        if event_name in self.events:
            for listener in self.events[event_name]:
                try:
                    listener(*args, **kwargs)
                except Exception as e:
                    logger.error(f"Error in event listener for {event_name}: {e}")
        
        
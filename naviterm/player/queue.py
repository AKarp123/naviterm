from libopensonic.media.media_types import Child
from naviterm.config import load_playback_config
import random
from naviterm.config import save_playback_config

class Queue():
    """This class controls the queue of playable media
    
    
    
    """
    
    
    def __init__(self) -> None:
        
        
        self.tracks : list[Child] = []
        self.current_index : int = 0
        playback_config = load_playback_config()
        self.shuffling : bool = playback_config.get("shuffling", False)
        self.repeating : bool = playback_config.get("repeating", False)
        
        
        
    def save_config(self) -> None:
        """Save the playback configuration to file.
        """
        playback_config = {
            "shuffling": self.shuffling,
            "repeating": self.repeating,
        }
        save_playback_config(playback_config)
    
        

        
    def add_track(self, track: Child) -> None:
        
        """Add a track to the queue.
        """
        self.tracks.append(track)
        
    
    def get_current_track(self) -> Child | None:
        """Get the current track in the queue.
        """
        if 0 <= self.current_index < len(self.tracks):
            return self.tracks[self.current_index]
        return None
    
    def shuffle(self) -> None:
        """Shuffle the queue.
        """
        current_track = self.get_current_track()
        left = self.tracks[:self.current_index]
        right = self.tracks[self.current_index + 1 :]
        t_queue = left + right
        random.shuffle(t_queue)
        if current_track:
            self.tracks = [current_track] + t_queue
            self.current_index = 0
        else:
            self.tracks = t_queue
            self.current_index = -1
            
    def clear(self) -> None:
        """Clear the queue.
        """
        self.tracks = []
        self.current_index = 0
        
    
    
    pass
from libopensonic.media.media_types import Child
from asyncio import create_task

from platformdirs import user_cache_dir
from naviterm.config import load_playback_config
import random
from naviterm.config import save_playback_config
from just_playback import Playback
from libopensonic.async_connection import AsyncConnection
from aiofiles import open as aio_open, os as aio_os


from pathlib import Path
import logging
mime_types = {
"audio/mpeg": "mp3",
"audio/flac": "flac",
"audio/wav": "wav",
"audio/aac": "aac",
"audio/ogg": "ogg",
}

logger = logging.getLogger(__name__)
cache_dir = Path(user_cache_dir("Naviterm", "Naviterm"))
music_cache_dir = cache_dir / "music"  

class Player():
    """This class manages the playback of the music player
    
    
    
    """
    
    
    def __init__(self, connection: AsyncConnection) -> None:
        self.is_playing = False
        self.connection = connection
        self.tracks : list[Child] = []
        self.current_index : int = 0 # -1 so no track playing
        self.del_index = -1 # Left ptr to delete tracks that have been played from cache
        self.cache_index = self.current_index # Right ptr to cache tracks to be played next in the queue
        playback_config = load_playback_config()
        self.shuffling : bool = playback_config.get("shuffling", False)
        self.repeating : bool = playback_config.get("repeating", False)
        self.audio_player = Playback()

        
        
        
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
    
    
    def get_queue(self) -> list[Child]:
        """Get the current queue of tracks.
        """
        return self.tracks
    
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
        self.del_index = -1
        self.enqueue_index = 0 
        
        
    def add_to_queue(self, tracks: Child | list[Child]) -> None:
        """Add a track or list of tracks to the end of the queue.
        """
        if isinstance(tracks, Child):
            self.tracks.append(tracks)
        else:
            self.tracks.extend(tracks)
        
    
    
    async def start(self):
        """Start playback of queue"""
        if len(self.tracks) == 0:
            print("No tracks in queue")
            return
        
        
        cur = self.get_current_track()
        if not cur:
            print("No current track to play")
            return
        assert cur.content_type is not None, "Track content type is None"
        
        if not await self.file_exists(cur.id, cur.content_type): 
            await self.cache_track(cur)
            self.cache_index += 1
            create_task(self.play_track(cur.id, cur.content_type))
        else:
            create_task(self.play_track(cur.id, cur.content_type))
            
        while(self.cache_index < len(self.tracks) and self.cache_index <= self.current_index + 3):
            track = self.tracks[self.cache_index]
            if track.content_type is not None and not await self.file_exists(track.id, track.content_type):
                await self.cache_track(track)
            self.cache_index += 1
        
    
    
    async def next(self):
        pass
        
        
        

    
    
    async def cache_track(self, track: Child) -> None:
        
        data = await self.connection.stream(track.id)
        async with aio_open(f"{music_cache_dir}/{track.id}.{mime_types[data.content_type]}", "wb") as f:
            await f.write(await data.read())
            logger.info(f"Cached track: {track.id if track.id else 'Unknown'}")
            
    async def remove_from_cache(self) -> None:
        if self.del_index < 0 or self.del_index >= len(self.tracks):
            return
        track = self.tracks[self.del_index]
        if track.content_type is not None:
            path = Path(f"{music_cache_dir}/{track.id}.{mime_types[track.content_type]}")
            if self.file_exists(track.id, track.content_type):
                await aio_os.remove(path)
                
        self.del_index += 1

    async def play_track(self, track_id: str, content_type: str) -> None:
        """Play a track."""
        current_track = self.get_current_track()
        if not current_track:
            return
        
        self.audio_player.load_file(f"{music_cache_dir}/{track_id}.{mime_types[content_type]}")
        self.is_playing = True
        self.audio_player.play()
        logger.info(f"Streaming track: {track_id if track_id else 'Unknown'}")
        
    async def file_exists(self, track_id: str, content_type: str) -> bool:
        return Path(f"{music_cache_dir}/{track_id}.{mime_types[content_type]}").exists()

    async def wait_for_current_track_end(self, duration: int) -> None:
        pass
    
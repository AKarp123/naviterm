from libopensonic import Connection, errors
import logging

from libopensonic.media.media_types import Album


logger = logging.getLogger(__name__)

class subsonic_conection:
    def __init__(self, server_url: str, username: str, password: str):
        self.connection = Connection(base_url=server_url, username=username, password=password, app_name="Naviterm", port=443)
        
    def ping(self):
        try:
            res = self.connection.ping()
            logger.debug(f"Ping result: {res}")
            return res
        except Exception as e:

            logger.error(f"Error pinging server: {e}")
            return False
        
    def get_all_albums(self, offset: int = 0) -> list[Album]:
        try:
            res = self.connection.get_album_list(ltype="newest", size=50, offset=offset)
            return res
        except Exception as e:
            logger.error(f"Error getting all albums: {e}")
            return False
        
        


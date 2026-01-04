from libopensonic import Connection
import logging

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
        
        


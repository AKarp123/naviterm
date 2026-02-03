from textual.app import ComposeResult
from textual.screen import Screen
from textual.containers import Vertical
from textual.widgets import Static



class NowPlaying(Screen):
	"""Screen to display the currently playing track."""
 
	CSS = """
	Screen {
		align: center middle;
	}
	
	#now-playing-container {
		width: 80%;
		height: auto;
		align: center middle;
		border: round $accent;
		padding: 2;
	}
	
	#title {
		width: 100%;
		height: 3;
		content-align: center middle;
		text-style: bold;
		margin-bottom: 2;
	}
	"""
 
	def compose(self) -> ComposeResult:
		"""Compose the Now Playing screen."""
		with Vertical(id="now-playing-container"):
			yield Static("Now Playing", id="title")
			# Additional now playing details would go here
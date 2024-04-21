import os
import time
from pathlib import Path
import tornado.ioloop
import tornado.websocket
import tornado.httpserver
# import mtvplayer as MTVP
import mpv

import glob

class MTVPlayer:
    def __init__(self):
        self.player = mpv.MPV()
        self.player.fullscreen = True
    
    def play(self, path):
        self.player.play(path)
        print("play function invoked")

    def stop(self):
        self.player.stop()

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

class VideoHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        self.write_message("Connection established")

    def on_message(self, message):
        # mtvplayer = MTVP.MTVPlayer()
        mtvplayer = MTVPlayer()
        
        mtvcommand, path = message.split(":")
        print(path)
        if mtvcommand == "TIME":
            txt = f"Current time: {time.ctime()}"
            self.write_message(txt)
        elif mtvcommand == "PLAY":
            mtvplayer.play(path)
            self.write_message("Video playing")
        elif mtvcommand == "STOP":
            mtvplayer.stop()
            self.write_message("Video paused")
        elif mtvcommand == "glob":
            search_path = Path(path)
            search_pattern =  "**/*.mp4"
            files = search_path.glob(search_pattern, follow_symlinks=True)
            self.write_message(str(files))
        else:
            self.write_message("Invalid command")

    def on_close(self):
        print("Connection closed")

def make_app():
    settings = {
        "template_path": os.path.join(os.path.dirname(__file__), "templates"),
        "static_path": os.path.join(os.path.dirname(__file__), "static")
    }
    
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/mtvws", VideoHandler),
    ], **settings)

if __name__ == "__main__":
    app = make_app()
    app.listen(5000)
    print("Server started on port 5000")
    tornado.ioloop.IOLoop.current().start()

# import subprocess
# import asyncio
# import websockets
# import mpv  # Assuming you're using python-mpv



# async def handle_message(websocket, message):
#     # Parse the message (e.g., play, pause, volume)
#     command, path = message.split(":")
    
#     # Use mpv object to control playback
#     player = mpv.MPV(input_ipc_server="/tmp/mpv-socket", idle=True)  # Define the "player" object
    
#     if command == "play":
#         player.play(path)
#     elif command == "pause":
#         player.pause()
#     # Add logic for other commands (volume, seek, etc.)
    
#     # Respond with confirmation (optional)
#     await websocket.send("Command received!")

# async def main():
#     async with websockets.serve(handle_message, "localhost", 8765):
#         print("WebSocket server started on port 8765!")
#         await asyncio.Future()  # Run server indefinitely

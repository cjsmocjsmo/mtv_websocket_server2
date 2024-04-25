# import os
# import time
# from pathlib import Path
# import tornado.ioloop
# import tornado.websocket
# import tornado.httpserver
# # import mtvplayer as MTVP
# import mpv

# import glob

# class MTVPlayer:
#     def __init__(self):
#         self.player = mpv.MPV()
#         self.player.fullscreen = True
    
#     def play(self, path):
#         self.player.play(path)
#         print("play function invoked")

#     def stop(self):
#         self.player.stop()

# class MainHandler(tornado.web.RequestHandler):
#     def get(self):
#         self.render("index.html")

# class VideoHandler(tornado.websocket.WebSocketHandler):
#     def open(self):
#         self.write_message("Connection established")

#     def on_message(self, message):
#         # mtvplayer = MTVP.MTVPlayer()
#         mtvplayer = MTVPlayer()
        
#         mtvcommand, path = message.split(":")
#         print(path)
#         if mtvcommand == "TIME":
#             txt = f"Current time: {time.ctime()}"
#             self.write_message(txt)
#         elif mtvcommand == "PLAY":
#             mtvplayer.play(path)
#             self.write_message("Video playing")
#         elif mtvcommand == "STOP":
#             mtvplayer.stop()
#             self.write_message("Video paused")
#         elif mtvcommand == "glob":
#             search_path = Path(path)
#             search_pattern =  "/*.mp4"
#             files = search_path.glob(search_pattern)
#             f = None
#             for file in files:
#                 print(file)

            
#             self.write_message(str(f))
#         else:
#             self.write_message("Invalid command")

#     def on_close(self):
#         print("Connection closed")

# def make_app():
#     settings = {
#         "template_path": os.path.join(os.path.dirname(__file__), "templates"),
#         "static_path": os.path.join(os.path.dirname(__file__), "static")
#     }
    
#     return tornado.web.Application([
#         (r"/", MainHandler),
#         (r"/mtvws", VideoHandler),
#     ], **settings)

# if __name__ == "__main__":
#     app = make_app()
#     app.listen(5000)
#     print("Server started on port 5000")
#     tornado.ioloop.IOLoop.current().start()

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







import json
from gevent import monkey
from gevent.server import StreamServer

# Import mpv library
import mpv

monkey.patch_all()  # Patch standard library for asynchronous behavior


class MpvController:
    def init(self):
        self.player = mpv.MPV()
        return self.player

    def load(self, filename):
        self.player.loadfile(filename)
        self.player.fullscreen = True
        return "Loaded file: {}".format(filename)

    def play(self):
        self.player.play()
        return "Playing"

    def stop(self):
        self.player.pause()
        return "Stopped"


def handle_request(socket, address):
    # Receive data from client
    data = socket.recv(1024).decode()

    # Parse data (assuming simple JSON format)
    try:
        request = json.loads(data)
        method = request["method"]
        params = request.get("params", [])
    except json.JSONDecodeError:
        response = {"error": "Invalid JSON format"}
    else:
        # Call corresponding method from MpvController
        if method == "load":
            response = {"result": controller.load(params[0])}
        elif method == "play":
            response = {"result": controller.play()}
        elif method == "stop":
            response = {"result": controller.stop()}
        else:
            response = {"error": "Unknown method"}

    # Send response back to client
    socket.sendall(json.dumps(response).encode())
    socket.close()


if __name__ == "__main__":
    print("starting controller")
    controller = MpvController().init()
    print("controller started")
    server = StreamServer(("192.168.0.97", 8000), handle_request)
    print("Mpv RPC server listening on port 8000")
    server.serve_forever()
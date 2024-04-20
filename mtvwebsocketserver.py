import os
import time
import subprocess
import tornado.ioloop
import tornado.websocket
import tornado.httpserver
# import mtvplayer as MTVP
from mpv import MPVError, Context

# class MTVPlayer:
#     def __init__(self):
#         try:
#             self.mpv_context = Context()
#             self.mpv_context.set_option('input-default-bindings')
#             self.mpv_context.set_option('osc')
#             self.mpv_context.set_option('input-vo-keyboard')
#             self.mpv_context.set_option("fs", True)
#             self.mpv_context.set_option("idle", "yes")
#             self.mpv_context.initialize()
#             print("Video Player Ready")
#         except MPVError as e:
#             print(f"Failed to create MPV context: {e}")
#             self.close()
    
#     def play(self, path):
#         self.mpv_context.command('loadfile', path)

#     def stop(self):
#         self.mpv_context.command("stop")

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

class VideoHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        self.write_message("Connection established")

    def on_message(self, message):
        # mtvplayer = MTVP.MTVPlayer()
        # mtvplayer = MTVPlayer()
        
        mtvcommand, path = message.split(":")
        print(path)
        if mtvcommand == "TIME":
            txt = f"Current time: {time.ctime()}"
            self.write_message(txt)
        elif mtvcommand == "PLAY":
            command = ["python3", "mtvplayer.py", "--play", path]
            subprocess.run(command)
            self.write_message("Video playing")
        elif mtvcommand == "STOP":
            command = ["python3", "mtvplayer.py", "--stop"]
            subprocess.run(command)
            self.write_message("Video paused")
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


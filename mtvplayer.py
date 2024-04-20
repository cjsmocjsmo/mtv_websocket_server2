import mpv

class MTVPlayer:
    def __init__(self):
        self.player = mpv.MPV()
        self.player.fullscreen = True
    
    def play(self, path):
        self.player.play(path)
        print("play function invoked")

    def stop(self):
        self.player.stop()
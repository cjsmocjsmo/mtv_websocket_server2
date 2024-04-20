# from mpv import MPVError, Context

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
    
import mpv

class MTVPlayer:
    def __init__(self, path):
        self.player = mpv.MPV()
        self.player.fullscreen
    
    def play(self, path):
        self.player.play(path)
        print("play function invoked")

    def stop(self):
        self.player.stop

# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description='MTVPlayer CLI')
#     parser.add_argument('--play', metavar='path', type=str, help='the path to the video file to play')
#     parser.add_argument('--stop', action='store_true', help='stop the currently playing video')

#     args = parser.parse_args()

#     player = MTVPlayer(args.play)

    
#     if args.stop:
#         player.stop()
import os
import subprocess
import sys

os.environ['DISPLAY'] = ':0'

if len(sys.argv) > 1:
    video_file = sys.argv[1]
else:
    raise ValueError("No video file specified.")

def play_video_loop(video_file_path):
    # mpvでループ再生
    subprocess.run(['mpv', '--loop', '--fullscreen', '--no-border', video_file_path])

def main():
    if not os.path.isfile(video_file):
        raise FileNotFoundError(f"{video_file} not found.")

    play_video_loop(video_file)

if __name__ == "__main__":
    main()

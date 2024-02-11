import os
import subprocess
import sys
import random
from datetime import datetime

os.environ['DISPLAY'] = ':0'

if len(sys.argv) > 1:
    try:
        pi_idx = int(sys.argv[1]) 
    except ValueError:
        raise ValueError("pi_idx should be int。")
else:
    raise ValueError("no pi_idx specified")

def get_newest_file(path):
    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    files.sort(key=lambda x: os.path.getmtime(os.path.join(path, x)), reverse=True)
    for file in files:
        if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            return os.path.join(path, file)
    return None

def is_gif_file(file_path):
    return file_path.lower().endswith('.gif')

def display_image(file_path):
    if is_gif_file(file_path):
        # GIFアニメーションの場合は mpv または mplayer を使用
        subprocess.run(['mpv', '--loop=inf', '--fullscreen', file_path])
    else:
        # PNG/JPG の場合は feh を使用
        subprocess.run(['feh', '--fullscreen', file_path])

def kill_previous_instances():
    try:
        current_pid = str(os.getpid())
        pids = subprocess.check_output(["pgrep", "-f", "sync_text_levi.py"]).decode().split()

        for pid in pids:
            if pid != current_pid:
                os.kill(int(pid), signal.SIGTERM)
    except subprocess.CalledProcessError:
        pass

def main():
    subprocess.run(['rclone', 'sync', f'googledrive:/HATRA24SS/21M/AX01/{str(pi_idx).zfill(2)}/', f'/home/pi/sync/'])
    newest_file = get_newest_file(f'/home/pi/sync/')

    if newest_file:
        display_image(newest_file)

    kill_previous_instances()
    sys.exit(0)

if __name__ == "__main__":
    main()

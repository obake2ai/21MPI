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
        # GIFアニメーションの場合、mpvで黒背景を設定して再生
        subprocess.run(['mpv', '--loop=inf', '--fs', '--no-keepaspect-window', '--background=#000000', file_path])
    else:
        # PNG/JPGの場合はfehを使用
        subprocess.run(['feh', '--fullscreen', file_path])
        
def kill_previous_mpv_instances():
    try:
        subprocess.run(["pkill", "-f", "mpv"])
    except subprocess.CalledProcessError:
        pass

def main():
    kill_previous_mpv_instances() 
    subprocess.run(['rclone', 'sync', f'googledrive:/HATRA24SS/21M/AX01/{str(pi_idx).zfill(2)}/', f'/home/pi/sync/'])
    newest_file = get_newest_file(f'/home/pi/sync/')

    if newest_file:
        display_image(newest_file)

    kill_previous_instances()
    sys.exit(0)

if __name__ == "__main__":
    main()

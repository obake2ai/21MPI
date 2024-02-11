import os
import subprocess
import sys
import random
from datetime import datetime

os.environ['DISPLAY'] = ':0'
DEFAULT_GIF = "/home/pi/21MPI/3dlogo_typ_bg.gif"
if len(sys.argv) > 1:
    try:
        pi_idx = int(sys.argv[1])
    except ValueError:
        raise ValueError("pi_idx should be an integer.")
else:
    raise ValueError("No pi_idx specified.")

def get_newest_file(path):
    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    files.sort(key=lambda x: os.path.getmtime(os.path.join(path, x)), reverse=True)
    for file in files:
        if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            return os.path.join(path, file), os.path.getmtime(os.path.join(path, file))
    return None, None

def is_gif_file(file_path):
    return file_path.lower().endswith('.gif')

def display_image(file_path):
    if is_gif_file(file_path):
        subprocess.run(['mpv', '--loop=inf', '--fs', '--no-keepaspect-window', '--background=#000000', file_path])
    else:
        subprocess.run(['feh', '--fullscreen', file_path])

def kill_previous_mpv_instances():
    try:
        subprocess.run(["pkill", "-f", "mpv"])
    except subprocess.CalledProcessError:
        pass

def main():
    last_update_time = None
    while True:
        kill_previous_mpv_instances() 
        subprocess.run(['rclone', 'sync', f'googledrive:/HATRA24SS/21M/AX01/{str(pi_idx).zfill(2)}/', f'/home/pi/sync/'])
        newest_file, file_time = get_newest_file(f'/home/pi/sync/')

        if newest_file and (last_update_time is None or file_time > last_update_time):
            last_update_time = file_time
            display_image(newest_file)
        elif last_update_time is None:
            display_image(DEFAULT_GIF)

        time.sleep(10)

if __name__ == "__main__":
    main()

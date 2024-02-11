import os
import subprocess
import sys
import time

os.environ['DISPLAY'] = ':0'

if len(sys.argv) > 1:
    try:
        pi_idx = int(sys.argv[1])
    except ValueError:
        raise ValueError("pi_idx should be an integer.")
else:
    raise ValueError("No pi_idx specified.")

def get_newest_file(path):
    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    if not files:
        return None, None
    newest_file = max(files, key=lambda x: os.path.getmtime(os.path.join(path, x)))
    return os.path.join(path, newest_file), os.path.getmtime(os.path.join(path, newest_file))

def display_image(file_path):
    subprocess.run(['feh', '--fullscreen', file_path])

def kill_previous_feh_instances():
    try:
        subprocess.run(["pkill", "-f", "feh"])
    except subprocess.CalledProcessError:
        pass

def main():
    last_update_time = None
    while True:
        kill_previous_feh_instances()
        subprocess.run(['rclone', 'sync', f'googledrive:/HATRA24SS/21M/AX01/{str(pi_idx).zfill(2)}/', f'/home/pi/sync/'])
        newest_file, file_time = get_newest_file(f'/home/pi/sync/')

        if newest_file and (last_update_time is None or file_time > last_update_time):
            last_update_time = file_time
            display_image(newest_file)

        time.sleep(10)

if __name__ == "__main__":
    main()

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
    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and f.lower().endswith(('.png', '.jpg', '.jpeg')) and not f.endswith('_rotated.jpg')]
    if not files:
        return None, None
    newest_file = max(files, key=lambda x: os.path.getmtime(os.path.join(path, x)))
    return os.path.join(path, newest_file), os.path.getmtime(os.path.join(path, newest_file))

def rotate_and_display_image(file_path):
    rotated_file_path = file_path + "_rotated.jpg"
    # 画像を90度回転
    subprocess.run(['convert', file_path, '-rotate', '90', rotated_file_path])
    # 回転した画像を表示
    subprocess.run(['feh', '--fullscreen', '--zoom', 'fill', rotated_file_path])

def main():
    last_update_time = None
    while True:
        subprocess.run(['rclone', 'sync', f'googledrive:/HATRA24SS/21M/AX01/{str(pi_idx).zfill(2)}/', f'/home/antix01/sync/'])
        newest_file, file_time = get_newest_file(f'/home/antix01/sync/')

        if newest_file and (last_update_time is None or file_time > last_update_time):
            last_update_time = file_time
            rotate_and_display_image(newest_file)
        time.sleep(10)

if __name__ == "__main__":
    main()

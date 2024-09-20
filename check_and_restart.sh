#!/bin/bash

# プログラム名または一意な識別子
PROCESS_NAME="play_loop_video.py"

# プロセスが動作しているか確認
if pgrep -f "$PROCESS_NAME" > /dev/null
then
    echo "$PROCESS_NAME is running"
else
    echo "$PROCESS_NAME is not running, starting it again..."
    /usr/bin/python3 /home/pi/21MPI/play_loop_video.py /home/pi/21MPI/assets/STT_square.mp4 &
fi

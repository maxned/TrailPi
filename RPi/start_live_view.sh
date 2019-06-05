
TRAILPI_PID=$(ps -aef | grep 'trailpi.py' | grep -v 'grep' | awk '{ print $2 }')

if [[ -n "$TRAILPI_PID" ]]; then
    echo "Stopping TrailPi"
    kill -s SIGINT $TRAILPI_PID

    # Allow trailpi.py to kill all of the other scripts
    sleep 3
fi

if [[ $1 == "-s" ]]; then
    echo "Stopping live camera view"
    ~/RPi_Cam_Web_Interface/stop.sh
else
    echo "Starting live camera view"
    ~/RPi_Cam_Web_Interface/start.sh

    echo "Live view started. Don't forget to restart TrailPi again!"
fi

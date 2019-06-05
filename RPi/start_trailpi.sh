echo "Stopping live camera view"
~/RPi_Cam_Web_Interface/stop.sh

TRAILPI_PID=$(ps -aef | grep 'trailpi.py' | grep -v 'grep' | awk '{ print $2 }')
if [[ -n "$TRAILPI_PID" ]]; then
    echo "Stopping TrailPi"
    kill -s SIGINT $TRAILPI_PID

    # Allow trailpi.py to kill all of the other scripts
    sleep 3
fi

if [[ $1 != "-s" ]]; then
    echo "Starting TrailPi"
    ~/TrailPi/trailpi_launcher.sh
fi

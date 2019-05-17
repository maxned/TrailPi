
EXECUTION_PID=$(ps -aef | grep 'execution.py' | grep -v 'grep' | awk '{ print $2 }')

if [[ -n "$EXECUTION_PID" ]]; then
    echo "Stopping TrailPi"
    kill -s SIGINT $EXECUTION_PID

    # Allow execution to kill all of the scripts
    sleep 3
fi

echo "Starting live camera view"
~/RPi_Cam_Web_Interface/start.sh

echo "Live view started. Don't forget to restart TrailPi again!"

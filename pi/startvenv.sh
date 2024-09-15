#!/bin/bash

# Kill the tmux session if it already exists
tmux kill-session -t virtualenv_session 2>/dev/null

# Start a new tmux session and run the commands in an infinite loop
tmux new-session -d -s virtualenv_session "
    export USER="jeremy"
    export HOME=/home/jeremy
    rm -rf ~/.atsign/storage

    # Navigate to the directory
    cd ~/GitHub/at_server/tools/virtualenv/ &&

    # Bring down and up Docker Compose services
    sudo docker-compose down --volumes &&
    sudo docker-compose up -d &&

    # Sleep for 20 seconds to allow containers to initialize
    sleep 30 &&

    # Run the PKAM keys installation
    sudo docker exec virtualenv /usr/local/bin/install_PKAM_Keys;
"

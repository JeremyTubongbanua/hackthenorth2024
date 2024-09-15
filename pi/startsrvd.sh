#!/bin/bash

# Kill the tmux session if it already exists
tmux kill-session -t srvd_session 2>/dev/null

# Start a new tmux session for srvd and run the command in an infinite loop
tmux new-session -d -s srvd_session "
export USER="jeremy"
export HOME=/home/jeremy
while true; do
    rm -rf ~/.atsign/storage
    ~/.local/bin/srvd -a @alice🛠 -i 192.168.8.220 -v --root-domain vip.ve.atsign.zone;
    sleep 5;  # Delay before restarting if failure occurs
done
"
#!/bin/bash

# Kill the tmux session if it already exists
tmux kill-session -t sshnpd_session 2>/dev/null

# Start a new tmux session for sshnpd and run the command in an infinite loop
tmux new-session -d -s sshnpd_session "
while true; do
    export USER="jeremy"
    export HOME=/home/jeremy
    rm -rf ~/.atsign/storage
    ~/.local/bin/sshnpd -m @barbara🛠 -a @colin🛠  -s -v --root-domain vip.ve.atsign.zone -d jetson_v --po \"127.0.0.1:22,127.0.0.1:3389,localhost:3389,localhost:22\"; 
    sleep 5;  # Delay before restarting if failure occurs
done
"
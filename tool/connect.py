#!/usr/bin/env python3
import os
import time
import subprocess
import requests
import sys
import argparse
import configparser

# Check if we are connected to the Internet. Based on that, we can decide if we should either 1. connect through Internet rendezvous or 2. connect locally (and assume that we are on the same network as the Jetson Nano).


def check_internet():
    try:
        requests.get("https://www.google.com", timeout=5)
        return True
    except (requests.ConnectionError, requests.Timeout):
        return False


def load_config(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)
    return config


def run_command(config, use_cli):
    parser = argparse.ArgumentParser(
        description="Run NPT commands with Internet/local connection options.")
    parser.add_argument(
        '-p', type=str, help='Port number for the remote machine (default: 22)')
    parser.add_argument(
        '-l', type=str, help='Local port number (default: 12332)')
    parser.add_argument(
        '--rh', type=str, help='Remote host value for --rh flag (optional)')
    parser.add_argument('--override-with-internet', action='store_true',
                        help='Override to force using Internet method')
    parser.add_argument('--override-with-no-internet', action='store_true',
                        help='Override to force using local method')
    parser.add_argument('--cli', action='store_true',
                        help='Use CLI input instead of config file')

    args = parser.parse_args()

    if use_cli:
        # handle the possiblilty of the user using it like `./connect.py --cli -p 22` -> in this scenario, the user is providing the remote port but not the local port, and maybe we could still ask
        # something like `./connect.py --cli -p 22 -l 12332 --rh localhost would be the same as `./connect.py -p 22 -l 12332 --rh localhost`, which is an interesting case to handle, but is intended
        port = args.p
        if not port:
            port = input(
                "Enter the port number for the -p flag (Press Enter for default 22): ") or "22"
        local_port = args.l
        if not local_port:
            local_port = input(
                "Enter the local port number for the -l flag (Press Enter for default 12332): ") or "12332"
        rh_flag = args.rh
        if not rh_flag:
            rh_flag = input(
                "Enter the value for --rh flag (Press Enter for default \"localhost\"): ") or "localhost"
    else:
        # default to config.ini values
        port = args.p or config.get('Internet', 'internet_remote_port')
        local_port = args.l or config.get('Internet', 'internet_local_port')
        rh_flag = args.rh or config.get('Internet', 'internet_remote_host')

    if args.override_with_internet:
        # in this 1st scenario, the user is forcing the internet method
        print("Override detected: Forcing Internet method.")
        run_internet_command(config, port, local_port, rh_flag)
    elif args.override_with_no_internet:
        # in this 2nd scenario, the user is forcing the local method, we shall assume that the user is on the same network as the Jetson Nano
        print("Override detected: Forcing local method.")
        run_local_command(config, port, local_port, rh_flag)
    else:
        # in this 3rd scenario, we shall check if they are connected to the Internet ourselves
        if check_internet():
            print("Internet connection detected. Using Internet method.")
            run_internet_command(config, port, local_port, rh_flag)
        else:
            print("No Internet connection detected. Using local method.")
            run_local_command(config, port, local_port, rh_flag)


def run_internet_command(config, port, local_port, rh_flag):
    print("Connecting via Internet...")

    internet_from = config.get('Internet', 'internet_from')
    internet_to = config.get('Internet', 'internet_to')
    internet_rvd = config.get('Internet', 'internet_rvd')
    internet_device = config.get('Internet', 'internet_device')

    command = f"~/.local/bin/npt -f {internet_from} -t {internet_to} -r {
        internet_rvd} -d {internet_device} -K -T 0 -p {port} -l {local_port}"
    if rh_flag:
        command += f" --rh {rh_flag}"
    subprocess.run(command, shell=True)
    print("Monitoring Internet connection...")

    while True:
        if not check_internet():
            print("Disconnected from the Internet. Switching to local connection.")
            run_local_command(config, port, local_port, rh_flag)
            break
        time.sleep(5)


def run_local_command(config, port, local_port, rh_flag):
    print("Running local connection...")

    air_gapped_from = config.get('AirGapped', 'air_gapped_from')
    air_gapped_to = config.get('AirGapped', 'air_gapped_to')
    air_gapped_rvd = config.get('AirGapped', 'air_gapped_rvd')
    air_gapped_device = config.get('AirGapped', 'air_gapped_device')
    air_gapped_root_domain = config.get('AirGapped', 'air_gapped_root_domain')

    command = f"~/.local/bin/npt -f {air_gapped_from} -t {air_gapped_to} -r {air_gapped_rvd} -d {
        air_gapped_device} --root-domain {air_gapped_root_domain} -K -T 0 -p {port} -l {local_port}"
    if rh_flag:
        command += f" --rh {rh_flag}"
    subprocess.run(command, shell=True)


if __name__ == "__main__":
    config_file = "config.ini"
    config = load_config(config_file)

    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('--cli', action='store_true',
                        help='Use CLI input instead of config file')
    initial_args, _ = parser.parse_known_args()

    run_command(config, use_cli=initial_args.cli)

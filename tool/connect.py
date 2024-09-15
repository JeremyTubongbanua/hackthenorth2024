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


def get_custom_flags(args, config):
    port = args.p if args.p else input(f"Enter the port number for the -p flag (default {config.get(
        'Internet', 'internet_remote_port')}): ") or config.get('Internet', 'internet_remote_port')
    local_port = args.l if args.l else input(f"Enter the local port number for the -l flag (default {
                                             config.get('Internet', 'internet_local_port')}): ") or config.get('Internet', 'internet_local_port')
    rh_flag = args.rh if args.rh else input(
        f"Enter the value for --rh flag (optional, default \"localhost\"): ") or "localhost"

    return port, local_port, rh_flag


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
        port, local_port, rh_flag = get_custom_flags(args, config)
    else:
        port, local_port, rh_flag = args.p or config.get('Internet', 'internet_remote_port'), \
            args.l or config.get('Internet', 'internet_local_port'), \
            args.rh or "localhost"

    if args.override_with_internet:
        print("Override detected: Forcing Internet method.")
        run_internet_command(config, port, local_port, rh_flag)
    elif args.override_with_no_internet:
        print("Override detected: Forcing local method.")
        run_local_command(config, port, local_port, rh_flag)
    else:
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
        internet_rvd} -d {internet_device} -K -T 0 -p {port} -l {local_port} -v"
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
        air_gapped_device} --root-domain {air_gapped_root_domain} -K -T 0 -p {port} -l {local_port} -v"
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

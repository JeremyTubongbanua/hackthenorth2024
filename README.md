# hackthenorth2024

This is the repository for my Hack The North 2024 submission.

# Table of Contents

1. [HackTheNorth2024](#hackthenorth2024)
2. [Demo](#demo)
3. [Authors](#authors)
4. [Summary](#summary)
5. [How It Works](#how-it-works)
6. [Features](#features)
   - Recovery and Compatible in Air Gapped Environment
   - Sensitive Device is Literally Unhackable
   - Zero Trust
   - Secure
   - Smart CLI Tool
   - Utility
   - Jump Box
7. [Tool](#tool)
   - [Description](#description)
   - [-h Command](#-h-command)
   - [--cli Command](#--cli-command)
   - [--override-with-no-internet Command](#--override-with-no-internet-command)
   - [--override-with-internet Command](#--override-with-internet-command)
   - [-p Command](#-p-command)
   - [-l Command](#-l-command)
   - [--rh Command](#--rh-command)
   - [-v Command](#-v-command)
8. [Jetson Nano](#jetson-nano)
   - [startsshnpd.sh](#startsshnpdsh)
   - [Closing Ports](#closing-ports)
     - [SSH 22](#ssh-22)
     - [RDP 3389](#rdp-3389)
   - [Sample Logs](#sample-logs)
   - [Overall Crontab](#overall-crontab)
9. [Pi](#pi)
   - [1. venv](#1-venv)
   - [2. srvd](#2-srvd)
   - [Sample Logs](#sample-logs-1)
   - [Tunnel Tear Down Example](#tunnel-tear-down-example)
   - [Overall Crontab](#overall-crontab-1)

## Demo

4 minute video of the tool in action - [https://youtu.be/lrKfHAbEC_E](https://youtu.be/lrKfHAbEC_E)

## Authors

- [Emily Lai](https://github.com/emilyirenelai)
- [Jeremy Tubongbanua](https://github.com/JeremyTubongbanua)

## Summary

Our project is "Secure Remote Access into a Jetson Nano in an air gapped environment without exposing ports." In this hack, we offer features ranging from allowing you to recover from a loss of Internet connection whilst remaining a remote access connection to your device without that device having any open ports (at the level of a 192.168 address).

## How It Works

Our hack involves a Python tool that utilizes Atsign's NoPorts as a core dependency for secure remote access into devices without having to expose any ports. Atsign's NoPorts is a great solution because it is fully open source and allows for things like pulling their docker image so that we can locally run our very own NoPorts relay point, fully enabling us to utilize thier tech even in an air gapped setting.

Atsign is also great because all encryption keys are generated at the edge and all traffic is encrypted with them. So no central server can see any of the very top secret things that a person may be doing while remote accessing another machine.

![internet diagram](./Frame%207.png)

![local diagram](./Frame%206.png)

## Features

- **Recovery and Compatible in Air Gapped Environment** - if the user happens to both 1. be connected to the Internet and 2. be on the same network as the Jetson Nano and relay point, then if the Internet connection is lost, we can fall back to using the local method of remote access via the local raspberry pi relay point that is within the same network as both your own device and the Jetson Nano.
- **Sensitive Device is Literally Unhackable** - the Jetson Nano, in this case, is completely unhackable because it has no open ports, even at the level of a 192.168 address. This means that if a malicious person were to try to attack the Jetson Nano through the Internet, they can't because there are no exposed ports. Also, if a person were to come in-person to a secure facility and tried to access that device through the local network, they would also be unable to because the device has no open ports at the level of a 192.168 address.
- **Zero Trust** - nor the client nor the server have to trust the central server with any secrets or keys. This hack follows a zero trust architecture because the encryption keys are at the device level. We chose to go with a Raspberry Pi, Jetson Nano, and a MacBook for our demo devices because they are all devices that are highly capable of encryption. In a typical setting, there would be some sort of central body or institution that could see all of your data and have access to it. But in this hack, the tunnel in its establishment and during its entire session is fully peer-to-peer.
- **Secure** - the NoPorts relay point is a secure way to remote access devices because it is encrypted with keys that are on the device. This means that even if a malicious person were to try to attack the relay point, they would not be able to decrypt the traffic because the keys are on the device.
- **Smart CLI Tool** - the Python tool that we have created is a smart CLI tool that allows for the user to easily remote access their device. We provide 1. a config file that allows users of the tool to provide the atSigns that they own. 2. We provide an easy to use interface such that all scenarios are covered and possible to be ran in 1 command with the flags that you can pick and choose. For example, `./connect.py --cli` offers a fully interactive experience and `./connect.py --override-with-no-internet -p 3389 -l 12332` allows for the user to override default settings and skip the CLI steps and do everything in one quick succession.
- **Utility** - we believe our tool offers a lot of utility for those in IT or people who are constantly attending things like sensitive government machines. You can use our tool to remote access your device while still using the same remote access tool that you are familiar with. Just run the tool in the background and then you can go back to using something like Microsoft RDP. You can have the joy of doing things the way that you are comfortable with while also having the luxury of knowing that your device is secure and that you don't have to trust anyone in order to do it.
- **Jump Box** - you can use this tool as a jump box with the `--rh` flag where you can specify the remote host that you want to connect to. Typically, this is set to localhost by default because you probably want to connect to the Jetson Nano's services. But you can also use this as a jump box to connect to other devices that are on the same network as the Jetson Nano, like the pi for example.

## tool

### Description

This is the tool downloaded on the client side of things where the tunnel is initiated. The tool is a Python script that uses Atsign's NoPorts' [NPT binary](https://github.com/atsign-foundation/noports/releases) to establish a tunnel between the client and the server through a relay point. In our use case, the relay point is either 1. `@rv_am` which is hosted on the cloud by Atsign,  if Internet is available, or 2. `@alice` which is hosted on a Raspberry Pi and available on the local network, if Internet is not available.

`~/.local/bin/npt` is where most of the heavy encryption and tunnel establishing technology happens and that can be found [here](https://github.com/atsign-foundation/noports/releases).

### -h command

This is the help command that shows you all of the options you have when using the tool.

```bash
./connect.py -h
usage: connect.py [-h] [-p P] [-l L] [--rh RH] [--override-with-internet]
                  [--override-with-no-internet] [--cli] [-v]

Run NPT commands with Internet/local connection options.

options:
  -h, --help            show this help message and exit
  -p P                  Port number for the remote machine (default: 22)
  -l L                  Local port number (default: 12332)
  --rh RH               Remote host value for --rh flag (optional)
  --override-with-internet
                        Override to force using Internet method
  --override-with-no-internet
                        Override to force using local method
  --cli                 Use CLI input instead of config file
  -v, --verbose         Enable verbose output for the npt command
```

### --cli command

The CLI (command-line interface) command allows for a rich user experience when first establishing a tunnel. There are so many settings that it may be daunting at first, but the CLI allows for the user to easily input the settings that they want.

```bash
./connect.py --cli
Enter the port number for the -p flag (Press Enter for default 22): 22
Enter the local port number for the -l flag (Press Enter for default 12332): 33101
Enter the value for --rh flag (Press Enter for default "localhost"): localhost
Internet connection detected. Using Internet method.
Connecting via Internet...
Connecting ... Connected
2024-09-15 02:44:16.627594 : Requested "never" timeout: set to 365 days
2024-09-15 02:44:16.628169 : Sending daemon feature check request
2024-09-15 02:44:16.628216 : Fetching host and port from srvd
```

### --override-with-no-internet command

By default, the tool will actually check *for you* if the Internet is available. If it is, then it is assuming that you prefer to connect via Internet. But in some scenarios, if you are both connected to the Internet and connected locally, it would be faster to connect locally. The `--override-with-no-internet` command allows for the user to force the tool to use the local method of establishing a tunnel.

### --override-with-internet command

The `--override-with-internet` command allows for the user to force the tool to use the Internet method of establishing a tunnel. This is useful when the user is on the same network as the Jetson Nano and the Raspberry Pi, but they want to use the Internet method of establishing a tunnel.

### -p command

Specify the remote port that you want to connect to on the Jetson Nano. The default is 22 because you probably want to establish a tunnel using SSH.

### -l command

Specify the local port that you want to connect to on the Raspberry Pi. The default is 12332 because it is a random port that we chose. This is typically an ephemeral port that is used to establish the tunnel.

### --rh command

Specify the remote host that you want to connect to on the Jetson Nano. The default is localhost because you probably want to connect to the Jetson Nano's services. But you can also use this as a jump box.

### -v command

Enable verbose output for the npt command. This is useful for debugging purposes.

## jetson_nano

The Jetson Nano in our hack is the device that we will be remote accessing to (either with SSH on port 22 or RDP on port 3389)

### startsshnpd.sh

The [startsshnpd.sh](./jetson_nano/startsshnpd.sh) script is a simple script that will start the daemon process and run it again in case it crashes. The daemon processs will be listening . The daemon process binary can be found on Atsign's NoPorts [releases](https://github.com/atsign-foundation/noports/releases/tag/v5.6.1) (the daemon process was not written by us).

The daemon encryption keys would be located at `~/.atsign/keys/`

### Closing Ports

#### SSH 22

`sudo nano /etc/ssh/sshd_config`

```

ListenAddress localhost

```

`sudo service ssh restart`

#### RDP 3389

`sudo nano /etc/xrdp/xrdp.ini`

```

port=3389
address=127.0.0.1

```

`sudo systemctl daemon-reload`
`sudo systemctl restart xrdp`

### Sample Logs

Example of the daemon process starting up, listening for requests, then setting up a tunnel session.

```bash
INFO|2024-09-15 02:12:11.622303| sshnpd |Starting heartbeat
INFO|2024-09-15 02:12:11.622625| sshnpd |Subscribing to jetson_v\.sshnp@
INFO|2024-09-15 02:12:11.623158| sshnpd |Sharing device info for jetson_v with @barbara🛠
INFO|2024-09-15 02:12:11.718845| sshnpd |Done
INFO|2024-09-15 02:12:11.718971|Monitor (@colin🛠)|monitor started for @colin🛠 with last notification time: null
INFO|2024-09-15 02:12:17.166250| sshnpd |Received: ping
INFO|2024-09-15 02:12:17.166331| sshnpd |ping received from @barbara🛠 ( ping )
INFO|2024-09-15 02:12:17.166362| sshnpd |ping received from @barbara🛠 notification id : 4e3b1503-12b9-4159-869b-2ac9a61903cf
INFO|2024-09-15 02:12:17.889686| sshnpd |Received: npt_request
INFO|2024-09-15 02:12:17.889763| sshnpd |npt_request received from @barbara🛠 ( {"payload":{"sessionId":"794cc855-7434-4dad-9ec5-5887bfe9fe83","rvdHost":"192.168.8.220","rvdPort":38741,"requestedPort":22,"requestedHost":"localhost","authenticateToRvd":true,"clientNonce":"2024-09-15T02:12:16.589238","rvdNonce":"2024-09-15T02:12:17.276051","encryptRvdTraffic":true,"clientEphemeralPK":"MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAgH/leE1EPKojDkxU/Uv6FJ+1npuwqYZVIPg+2qkIjaS7bs5I5OnLB7nGzBQmbQZ2w9cAHEazeV7vgoh3J9syczbVwcK51BG7j1YIoxgD8vdAmR9EqVx7Tn5rwK9Bf7vni5Vc6eXVQ3Z8zDswzaRE7nhlwHS24Xs1pMbua53L8EdUTc2T5eCHlXcB08TPwL9L4kOcVnlhmNi+mXwzGCThE+27YUoB9dLdbx3GD57oVcscatcBChHCx6iLu/eSFD3L1EJlP067EvGdWCm91yYbZDnFEijhkOMZwARuhMwvSEtAwBIzQX9qMj3nUxKZ65QwroMomIB9ridHbVT6TbAFfwIDAQAB","clientEphemeralPKType":"rsa2048","timeout":31536000000},"signature":"hcG2vmySMSLaSPX5WOi0N3X+n2O570fLE60iceCaZdHRri/p1yaOo7uFqwvW294M3hxIBVcNlZ4gIHiEjCjJ3dZ4lrgEQLanesZZ1o/KTk5C/u366tgo/POXaUMmP/KuNvDaVwLB620ergdhdoa1SaUv90cSSXqGaCDDZAdrxNTYWvsfqob83k1xMCQ/tlObBaaZ59PRq4Pxinxl6v6z0lYG/jVzb2gb1j4s39JXhmehNQy2erHVG0mjxx8nTulpJ5Mpfc4GKj7C6F76KF8gkk05ZjdwTLnFjEUiT/vosm/f377BH1xv6MFnuTuel7atIRLmy2n7/eTpkWQps0CzWg==","hashingAlgo":"sha256","signingAlgo":"rsa2048"} )
INFO|2024-09-15 02:12:17.904535| sshnpd |Signing Verification Result: ResultType: bool, Result: true, SigningMetadata: {HashingAlgo: sha256, SigningAlgo: rsa2048, SignatureTimestamp: 2024-09-15 06:12:17.903258Z}
INFO|2024-09-15 02:12:17.904612| sshnpd |svr.result is a bool
INFO|2024-09-15 02:12:17.904638| sshnpd |svr.result is true
INFO|2024-09-15 02:12:17.904734| sshnpd |Setting up ports for tunnel session using openssh (openssh) from: @barbara🛠 session:
794cc855-7434-4dad-9ec5-5887bfe9fe83
INFO|2024-09-15 02:12:17.922607|SrvImplExec|SrvImplExec.run(): executing /usr/local/bin/srv -h 192.168.8.220 -p 38741 --local-port 22 --local-host localhost --timeout 31536000 --multi --rv-auth --rv-e2ee
INFO|2024-09-15 02:12:17.939118|SrvImplExec|rv stderr | INFO|2024-09-15 02:12:17.938468| SrvImplDart |New SrvImplDart - localPort 22
INFO|2024-09-15 02:12:17.941393|SrvImplExec|rv stderr | INFO|2024-09-15 02:12:17.941088| SrvImplDart |_runDaemonSideMulti authenticating control socket connection to rvd
INFO|2024-09-15 02:12:17.941683|SrvImplExec|rv stderr | rv started successfully
INFO|2024-09-15 02:12:18.043184| sshnpd |Started rv - pid is 7652
```

### Overall crontab

Hopefully this is what the overall crontab on the Jetson Nano looks like, so that you can get a better idea of what these scripts are doing exactly.

```bash
jeremy@jeremy-desktop:~$ crontab -l
@reboot /bin/bash /home/jeremy/startsshnpd.sh
```

## pi

The pi set up consists of two parts:

1. venv
2. srvd

The keys for the srvd to use would be located at `~/.atsign/keys/`

### 1. venv

This is a virtual environment that we use to run several things like: 3 atServers (alice, colin, and barbara) and an atDirectory (also known as the root server) that acts as a DNS server for these tinier atServers.

This docker hub image was fully provided by Atsign and can be found [here](https://hub.docker.com/r/atsigncompany/virtualenv).

We simply pulled the image and ran it. We also had to run `pkamLoad` to load each atServer with the appropriate PKAM public keys so that they could be authenticated to.

But in our case, we are using [docker-compose.yaml](./docker-compose.yaml) to spin up the image and manage the image/container.

The [startvenv.sh](./pi/startvenv.sh) script is used to start the venv @reboot via crontab.

### 2. srvd

This is a simple socket connector server that Atsign provides as part of their [releases](https://github.com/atsign-foundation/noports/releases/tag/v5.6.1). Essentially, when a NPT request is made by our client, the SRVD process will bind to two ports and simply relay the encrypted traffic between the two ports. Since it is encrypted with keys that are on the device, it is unable to decrypt the traffic. You can kind of think about it as passing on "garbage" that it can't do anything useful with. This is important because it means that although the raspberry pi is an attackable device, there would be nothing useful on it that a malicious person could do with it.

For this hack, we are using v5.6.1 of the SRVD binary that can be found in their [releases](https://github.com/atsign-foundation/noports/releases/tag/v5.6.1).

Below are some sample logs of a successful NPT tunnel being created. You can see by this line "`2024-09-15 01:57:41.030420 | serverToServer | Bound ports A: 42283, B: 45235`" that two ephemeral ports are bound to the two sides of the tunnel. The client will then use these ports to connect to the tunnel.

The [startsrvd.sh](./pi/startsrvd.sh) script is used to start the srvd @reboot via crontab.

### Sample Logs

```bash
QJRqqPpm6FBnhfEGFELzBCsXJAn6eP+jKkpAobqviUD7HdxSYlhCROT+CuVXqbtu53YBXB/puvMNcQIDAQAB","rvdNonce":"2024-09-15T01:57:40.862784","clientNonce":"2024-09-15T01:57:39.969997"}, false, true) 
INFO|2024-09-15 01:57:41.029967| srvd / socket_connector |Starting socket connector session for {sessionId: 91e14d7b-e7b2-4f3c-9881-d9c95e3537d5, atSignA: @barbara🛠, atSignB: @colin🛠, authenticateSocketA: true, authenticateSocketB: true, publicKeyA: MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAyvS3xLWgKuekekE9+D5+MIZ6Xx5Cjn8Xnm9D00xhUNu8/9C5wTgbMPX8XUfMGyOA85ymt9dkDl0BmrN8Rz8MPKpxNB94nRQuMO+0af1Tu2csxdAUZyn14usd0WYaahBhyUw36VKhuyhHoFOEmt2GHCiRiKr4pE3WPX8aod8JiJjzyzvREkQcn8NhxLi9k7ISPDwwp46NkBex10SV+oJ0YEDL1VGJHBdNTKm1q3e3mWorK391oK4gKmJv2zA/pFBdG0NXaPS9DYHRT3486nw6x3jVLybriCQBhfYAZrtUyfsc0tqCDD+YCFcWqhotSz2cA6Oj/Uu4TTHgnaSPc3BNNQIDAQAB, publicKeyB: MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEApLQ+CrLLF4Ndp7PKgZ+oRfzL8zJkiu4VXT7z8e5nsM7cUWOZ1f0Az2ct4FyF981NtN1pkf/4Vk3X5OMF2vmEKWzhxuocTYx+X19lbLnZkvYD+SEwKhf6BRfH0vREeKtijmPF/jCB0bKZ0Vffld4kz5F+PBmc93C6XeIm/T+n1ojKrQpDIwgIoPVa1OiP4Xx1prLsr9W2UbrH/h5F2+lsK5HwM35o64h4BXX3IdATYL8TQPCM47Tt1FiP1eMUim/81wO+18SeQJRqqPpm6FBnhfEGFELzBCsXJAn6eP+jKkpAobqviUD7HdxSYlhCROT+CuVXqbtu53YBXB/puvMNcQIDAQAB, rvdNonce: 2024-09-15T01:57:40.862784, clientNonce: 2024-09-15T01:57:39.969997} 
2024-09-15 01:57:41.030420 | serverToServer | Bound ports A: 42283, B: 45235
INFO|2024-09-15 01:57:41.030631| srvd / socket_connector |Assigned ports [42283, 45235] for session 91e14d7b-e7b2-4f3c-9881-d9c95e3537d5 
INFO|2024-09-15 01:57:41.030708| srvd / socket_connector |Waiting for connector to close 
INFO|2024-09-15 01:57:41.030775| srvd |Received ports (42283, 45235) in main isolate for session 91e14d7b-e7b2-4f3c-9881-d9c95e3537d5 
SHOUT|2024-09-15 01:57:41.030831| srvd |Starting session 91e14d7b-e7b2-4f3c-9881-d9c95e3537d5 for @barbara🛠 to @colin🛠 using ports (42283, 45235) 
SHOUT|2024-09-15 01:57:41.030863| srvd |Sending response data for requested session 91e14d7b-e7b2-4f3c-9881-d9c95e3537d5 : [192.168.8.220,42283,45235,2024-09-15T01:57:40.862784] 
INFO|2024-09-15 01:57:41.061504|AbstractAtKeyEncryption (@alice🛠)|Encrypted shared symmetric key for @alice🛠 not found in local storage 
INFO|2024-09-15 01:57:41.061645|AbstractAtKeyEncryption (@alice🛠)|Deleting @barbara🛠:shared_key@alice🛠 from LocalSecondary INFO|2024-09-15 01:57:41.062368|AbstractAtKeyEncryption (@alice🛠)|Fetching shared symmetric key for @alice🛠 from atServer 
INFO|2024-09-15 01:57:41.073878|AbstractAtKeyEncryption (@alice🛠)|Creating new shared symmetric key as @alice🛠 for @barbara🛠 
INFO|2024-09-15 01:57:41.076252|AbstractAtKeyEncryption (@alice🛠)|encryptedSharedKeyMyCopy from atChops: YouhPZ/kFt4qGmzl8/p6bz8RYa6gEda+u0mwfOSnC0sKEX4mLr54xt7WZSecLMp9qZiDy1OKVd6HFx6vzQlC2PXMhzg+YVL/ArjmOWRUw2M8X8Lo2svEA4cD7zm8ruhX4HK4CVd9wbrum7JrhQ6CPVdo6q46ZShQ92aa5f4iKdqeAej46O8P+ATlFsPPiKvXk8/hvZaxqwrhAaT1w/bd+3NKfhV1jIeWwM2EaFF+p3NVHdtLdiE1L8evXL8QKy0FRs2+D9qqm6f3spDtP6ODUGFGOZMA7YX7JuMKItakfya+/pfJiFAp2tGC1eW9STlyWHIX3Puq6G7o2k6GAPY1Tw== 
INFO|2024-09-15 01:57:41.076455|AbstractAtKeyEncryption (@alice🛠)|Deleting @barbara🛠:shared_key@alice🛠 from RemoteSecondary 
INFO|2024-09-15 01:57:41.109696|AbstractAtKeyEncryption (@alice🛠)|Storing new shared symmetric key to atServer 
INFO|2024-09-15 01:57:41.131753|AbstractAtKeyEncryption (@alice🛠)|Storing new shared symmetric key to local storage 
INFO|2024-09-15 01:57:41.133822|AbstractAtKeyEncryption (@alice🛠)|'Their' copy of shared symmetric key for @barbara🛠 not found in local storage - will check atServer 
INFO|2024-09-15 01:57:41.167645|AbstractAtKeyEncryption (@alice🛠)|Saving 'their' copy of shared symmetric key for @barbara🛠 to atServer 
INFO|2024-09-15 01:57:41.178659|AbstractAtKeyEncryption (@alice🛠)|Saving 'their' copy of shared symmetric key for @barbara🛠 to local storage 
2024-09-15 01:57:41.649064 | serverToServer | Connection on serverSocketB: 45235
INFO|2024-09-15 01:57:41.649199| SignatureAuthVerifier |SignatureAuthVerifier for @colin🛠: starting listen 
INFO|2024-09-15 01:57:41.651795| SignatureAuthVerifier |SignatureAuthVerifier @colin🛠 : verification SUCCESS : true 
2024-09-15 01:57:41.652019 | SocketConnector | Authentication succeeded on side B
2024-09-15 01:57:41.978674 | serverToServer | Connection on serverSocketA: 42283
INFO|2024-09-15 01:57:41.978794| SignatureAuthVerifier |SignatureAuthVerifier for @barbara🛠: starting listen 
INFO|2024-09-15 01:57:41.988446| SignatureAuthVerifier |SignatureAuthVerifier @barbara🛠 : verification SUCCESS : true 
2024-09-15 01:57:41.988599 | SocketConnector | Authentication succeeded on side A
2024-09-15 01:57:49.861843 | serverToServer | Connection on serverSocketA: 42283
INFO|2024-09-15 01:57:49.861939| SignatureAuthVerifier |SignatureAuthVerifier for @barbara🛠: starting listen 
INFO|2024-09-15 01:57:49.865962| SignatureAuthVerifier |SignatureAuthVerifier @barbara🛠 : verification SUCCESS : true 
2024-09-15 01:57:49.866291 | SocketConnector | Authentication succeeded on side A
2024-09-15 01:57:49.881424 | serverToServer | Connection on serverSocketB: 45235
INFO|2024-09-15 01:57:49.881492| SignatureAuthVerifier |SignatureAuthVerifier for @colin🛠: starting listen 
INFO|2024-09-15 01:57:49.885408| SignatureAuthVerifier |SignatureAuthVerifier @colin🛠 : verification SUCCESS : true 
2024-09-15 01:57:49.885638 | SocketConnector | Authentication succeeded on side B
```

Tunnel tear down example

```bash
2024-09-15 01:57:49.885638 | SocketConnector | Authentication succeeded on side B2244e B
2024-09-15 02:00:56.000031 | SocketConnector | stream.onDone on side A        -24
2024-09-15 02:00:56.000367 | SocketConnector | Destroying socket on side A
2024-09-15 02:00:56.000483 | SocketConnector | Destroying socket on far side (B)
2024-09-15 02:00:56.000584 | SocketConnector | Will remove established connection
2024-09-15 02:00:56.000665 | SocketConnector | Removed connection
2024-09-15 02:00:56.000740 | SocketConnector | stream.onDone on side B
2024-09-15 02:00:56.000814 | SocketConnector | Destroying socket on side B
2024-09-15 02:00:56.000888 | SocketConnector | Destroying socket on far side (A)
```

### Overall crontab

This is what the overall crontab on the raspberry pi looks like, so that you can get a better idea of what these scripts are doing exactly.

```bash
jeremy@raspberrypi8:~ $ crontab -l
@reboot /bin/bash /home/jeremy/startsrvd.sh
@reboot /bin/bash /home/jeremy/startvenv.sh
```

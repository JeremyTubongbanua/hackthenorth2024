# pi

The pi set up consists of two parts:

1. venv
2. srvd

The keys for the srvd to use would be located at `~/.atsign/keys/`

## 1. venv

This is a virtual environment that we use to run several things like: 3 atServers (alice, colin, and barbara) and an atDirectory (also known as the root server) that acts as a DNS server for these tinier atServers.

This docker hub image was fully provided by Atsign and can be found [here](https://hub.docker.com/r/atsigncompany/virtualenv).

We simply pulled the image and ran it. We also had to run `pkamLoad` to load each atServer with the appropriate PKAM public keys so that they could be authenticated to.

But in our case, we are using [docker-compose.yaml](./docker-compose.yaml) to spin up the image and manage the image/container.

The [startvenv.sh](./startvenv.sh) script is used to start the venv @reboot via crontab.

## 2. srvd

This is a simple socket connector server that Atsign provides as part of their [releases](https://github.com/atsign-foundation/noports/releases/tag/v5.6.1). Essentially, when a NPT request is made by our client, the SRVD process will bind to two ports and simply relay the encrypted traffic between the two ports. Since it is encrypted with keys that are on the device, it is unable to decrypt the traffic. You can kind of think about it as passing on "garbage" that it can't do anything useful with. This is important because it means that although the raspberry pi is an attackable device, there would be nothing useful on it that a malicious person could do with it.

For this hack, we are using v5.6.1 of the SRVD binary that can be found in their [releases](https://github.com/atsign-foundation/noports/releases/tag/v5.6.1).

Below are some sample logs of a successful NPT tunnel being created. You can see by this line "`2024-09-15 01:57:41.030420 | serverToServer | Bound ports A: 42283, B: 45235`" that two ephemeral ports are bound to the two sides of the tunnel. The client will then use these ports to connect to the tunnel.

The [startsrvd.sh](./startsrvd.sh) script is used to start the srvd @reboot via crontab.

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

# overall crontab

This is what the overall crontab on the raspberry pi looks like, so that you can get a better idea of what these scripts are doing exactly.

```bash
jeremy@raspberrypi8:~ $ crontab -l
@reboot /bin/bash /home/jeremy/startsrvd.sh
@reboot /bin/bash /home/jeremy/startvenv.sh
```

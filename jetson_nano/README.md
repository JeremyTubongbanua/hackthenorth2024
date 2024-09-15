# jetson_nano

The Jetson Nano in our hack is the device that we will be remote accessing to (either with SSH on port 22 or RDP on port 3389)

## startsshnpd.sh

The [startsshnpd.sh](./startsshnpd.sh) script is a simple script that will start the daemon process and run it again in case it crashes. The daemon processs will be listening . The daemon process binary can be found on Atsign's NoPorts [releases](https://github.com/atsign-foundation/noports/releases/tag/v5.6.1) (the daemon process was not written by us).

The daemon encryption keys would be located at `~/.atsign/keys/`

## Closing Ports

### SSH 22

`sudo nano /etc/ssh/sshd_config`

```
ListenAddress localhost
```

`sudo service ssh restart`

### RDP 3389

`sudo nano /etc/xrdp/xrdp.ini`

```
port=3389
address=127.0.0.1
```

`sudo systemctl daemon-reload`
`sudo systemctl restart xrdp`

## Sample Logs

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

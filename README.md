# hackthenorth2024

This is the repository for my Hack The North 2024 submission.

- [Emily Lai](https://github.com/emilyirenelai)
- [Jeremy Tubongbanua](https://github.com/JeremyTubongbanua)

## Summary

Our project is "Secure Remote Access into a Jetson Nano in an air gapped environment without exposing ports." In this hack, we offer features ranging from allowing you to recover from a loss of Internet connection whilst remaining a remote access connection to your device without that device having any open ports (at the level of a 192.168 address).

## How It Works

Our hack involves a Python tool that utilizes Atsign's NoPorts as a core dependency for secure remote access into devices without having to expose any ports. Atsign's NoPorts is a great solution because it is fully open source and allows for things like pulling their docker image so that we can locally run our very own NoPorts relay point, fully enabling us to utilize thier tech even in an air gapped setting.

Atsign is also great because all encryption keys are generated at the edge and all traffic is encrypted with them. So no central server can see any of the very top secret things that a person may be doing while remote accessing another machine.

## Features

- **Recovery and Compatible in Air Gapped Environment** - if the user happens to both 1. be connected to the Internet and 2. be on the same network as the Jetson Nano and relay point, then if the Internet connection is lost, we can fall back to using the local method of remote access via the local raspberry pi relay point that is within the same network as both your own device and the Jetson Nano.
- **Sensitive Device in Literally Unhackable** - the Jetson Nano, in this case, is completely unhackable because it has no open ports, even at the level of a 192.168 address. This means that if a malicious person were to try to attack the Jetson Nano through the Internet, they can't because there are no exposed ports. Also, if a person were to come in-person to a secure facility and tried to access that device through the local network, they would also be unable to because the device has no open ports at the level of a 192.168 address.
- **Zero Trust** - nor the client nor the server have to trust the central server with any secrets or keys. This hack follows a zero trust architecture because the encryption keys are at the device level. We chose to go with a Raspberry Pi, Jetson Nano, and a MacBook for our demo devices because they are all devices that are highly capable of encryption. In a typical setting, there would be some sort of central body or institution that could see all of your data and have access to it. But in this hack, the tunnel in its establishment and during its entire session is fully peer-to-peer.
- **Secure** - the NoPorts relay point is a secure way to remote access devices because it is encrypted with keys that are on the device. This means that even if a malicious person were to try to attack the relay point, they would not be able to decrypt the traffic because the keys are on the device.
- **Smart CLI Tool** - the Python tool that we have created is a smart CLI tool that allows for the user to easily remote access their device. We provide 1. a config file that allows users of the tool to provide the atSigns that they own. 2. We provide an easy to use interface such that all scenarios are covered and possible to be ran in 1 command with the flags that you can pick and choose. For example, `./connect.py --cli` offers a fully interactive experience and `./connect.py --override-with-no-internet -p 3389 -l 12332` allows for the user to override default settings and skip the CLI steps and do everything in one quick succession.
- **Utility** - we believe our tool offers a lot of utility for those in IT or people who are constantly attending things like sensitive government machines. You can use our tool to remote access your device while still using the same remote access tool that you are familiar with. Just run the tool in the background and then you can go back to using something like Microsoft RDP. You can have the joy of doing things the way that you are comfortable with while also having the luxury of knowing that your device is secure and that you don't have to trust anyone in order to do it.

## Demo

4 minute video of the tool in action - [https://youtu.be/lrKfHAbEC_E](https://youtu.be/lrKfHAbEC_E)

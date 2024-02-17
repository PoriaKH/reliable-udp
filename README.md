# reliable-udp
reliable-udp is a client-server project. in this project i optimized the [User Datagram Protocol (UDP)](https://en.wikipedia.org/wiki/User_Datagram_Protocol) and made it reliable by using [Selective Repeat ARQ](https://en.wikipedia.org/wiki/Selective_Repeat_ARQ).<br/>
In reliable-udp we took care of out of order and lost packets.<br/>
### How It Works
User will send bunch of packets to our client, our client will transfer the packets to [Lossy Link](https://github.com/HirbodBehnam/lossy_link) which will reorder and loose some of our packets randomly and we're gonna make sure that our server recieves packets in the right order and 0% loss rate.
<img width="799" alt="image" src="https://github.com/PoriaKH/reliable-udp/assets/94684621/c75fd798-4e0e-4a0f-bae0-dc34c755eedd">
### Usage
```
./lossy_link 127.0.0.1:12345 127.0.0.1:54321
```
With this command Lossy Link will transfer all the packets from the port 12345 to port 54321.<br/>
<br/>
User must send UDP packets to the client, it can use `ncat` as bellow:
```
ncat --recv-only -u -l 54321
```
### Build
Use `make` to build the project. The executable file will be in the `./dist` directory. <br/>
`make clean` to clean the artifacts. <br/>

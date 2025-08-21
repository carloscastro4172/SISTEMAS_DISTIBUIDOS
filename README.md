# Socket Programming Workshop

This repository contains the code developed during the **Distributed Systems workshop**.  
The main goal was to implement client-server communication using **sockets**, first in Python and then in C, also exploring **multithreading** and random message generation.

---

## Contents

### Python
- **`server_multithread.py`**  
  Multithreaded TCP server in Python. It handles multiple concurrent clients, each in its own thread.

- **`client_multithreading.py`**  
  Multithreaded client that sends a predefined set of messages to the server in parallel using multiple threads.

- **`client_random_multithread.py`**  
  Enhanced client that sends a **random number of messages** (between 1 and 20 per thread), generated from a word dictionary.  
  It simulates a more realistic load to the server.

### C
- **`server.c`**  
  Simple TCP server in C that receives client messages and responds with an echo of the message received.

- **`client.c`**  
  TCP client in C that sends messages to the server, receives the response, and allows the user to continue or end the session. Compatible with both **Linux** and **Windows (WinSock)**.

---

## Requirements

- **Python 3.8+**
- **Linux Fedora** or **Windows 11** (tested on both systems)
- C compiler:
  - `gcc` on Linux  
  - `MinGW` or similar on Windows  

---

## Running in Python

1. Start the server:

   ```bash
   python3 server_multithread.py
   ```

2. In another terminal, run a client:

   ```bash
   python3 client_multithreading.py
   ```

   or:

   ```bash
   python3 client_random_multithread.py
   ```

---

## Running in C

1. Compile the programs:

   ```bash
   gcc server.c -o server
   gcc client.c -o client
   ```

2. Start the server:

   ```bash
   ./server
   ```

3. Run the client:

   ```bash
   ./client
   ```

---

## Experiments performed

1. **Single machine test (localhost).**  
   Both client and server run on the same machine (Linux Fedora).  

2. **Different host test.**  
   Client and server run on separate machines, one with **Linux Fedora** and the other with **Windows 11**, connected in the same network.  

3. **Multithreading in Python.**  
   Multiple clients sending messages simultaneously to the server.  

4. **Random clients.**  
   Each client generates and sends a variable number of random messages.  

5. **C version.**  
   The client-server programs were reimplemented in C to repeat the tests and validate communication.  

---

## Repository structure

```
.
├── client_multithreading.py
├── client_random_multithread.py
├── server_multithread.py
├── server.c
└── client.c
```

---

## Authors

This workshop was carried out in the context of the **Distributed Systems course**, using two computers:  
- One with **Linux Fedora** (using `ifconfig` to obtain the IP).  
- Another with **Windows 11**.  
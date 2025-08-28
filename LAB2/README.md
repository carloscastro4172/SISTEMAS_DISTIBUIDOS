# Distributed Systems Lab – XML-RPC & ZeroMQ

This repository contains the implementation of different exercises for the Distributed Systems course.  
It includes two main parts:

1. **XML-RPC Array Manager** – A server and client to perform remote operations on numeric arrays.  
2. **ZeroMQ Publisher/Subscriber** – Examples with single and multiple publishers/subscribers.

---

## 📂 Project Structure

```
.
├── arreglo_server.py        # XML-RPC server exposing array operations
├── arreglo_client.py        # XML-RPC client with menu for array operations
├── publisher.py             # Basic ZeroMQ publisher (TIME messages)
├── subscriber.py            # Basic ZeroMQ subscriber
├── subscriber2.py           # Second subscriber (fan-out test)
├── subscriber3.py           # Third subscriber (fan-out test)
├── publisher_news.py        # Publisher sending NEWS messages
├── publisher_alert.py       # Publisher sending ALERT messages
├── subscriber_news.py       # Subscriber to NEWS only
├── subscriber_multi.py      # Subscriber to NEWS + ALERT
```

---

## ⚙️ Requirements

- Python 3.8+  
- [pyzmq](https://pypi.org/project/pyzmq/)  
- No extra dependencies for XML-RPC (standard library)

Install dependencies:
```bash
pip install pyzmq
```

---

## 🖥️ Part 1: XML-RPC Array Manager

### Server – `arreglo_server.py`
Runs an XML-RPC server on a given host/port. Implements:
- Element-wise sum
- Element-wise subtraction
- Dot product
- Element-wise maximum
- Element-wise minimum

Run the server:
```bash
python3 arreglo_server.py
```
(Default: binds to `172.23.199.4:12000`)

### Client – `arreglo_client.py`
Interactive terminal client. Allows user to:
1. Enter two arrays
2. Select an operation (sum, sub, dotprod, max, min)
3. Display result
4. Exit with option 6

Run the client:
```bash
python3 arreglo_client.py
```
Enter the server IP/port when prompted.

---

## 🖥️ Part 2: ZeroMQ Publisher/Subscriber

### Basic Example
- `publisher.py` → Publishes `TIME` messages every 5 seconds on `localhost:15000`.
- `subscriber.py` → Connects to the publisher and receives 5 messages.

Run in two terminals:
```bash
# Terminal 1
python3 publisher.py

# Terminal 2
python3 subscriber.py
```

### Multiple Subscribers
Tested with `subscriber.py`, `subscriber2.py`, `subscriber3.py` all connected to the same publisher.  
Each receives the same stream of `TIME` messages → demonstrates **fan-out**.

### Multiple Publishers
- `publisher_news.py` → Publishes NEWS messages (`tcp://0.0.0.0:15000`)
- `publisher_alert.py` → Publishes ALERT messages (`tcp://0.0.0.0:16000`)
- `subscriber_news.py` → Subscribes only to NEWS
- `subscriber_multi.py` → Subscribes to both NEWS and ALERT (even across hosts)

Run in four terminals:
```bash
# Terminal 1 (NEWS Publisher)
python3 publisher_news.py

# Terminal 2 (ALERT Publisher)
python3 publisher_alert.py

# Terminal 3 (NEWS Subscriber)
python3 subscriber_news.py

# Terminal 4 (Multi Subscriber)
python3 subscriber_multi.py
```

---

## 📊 Tests Performed

1. **Same Machine**  
   - Publisher and subscriber on `localhost`.  
   - Subscriber receives periodic TIME messages.

2. **Different Hosts**  
   - Publisher on Fedora, subscriber on Debian, and vice versa.  
   - Needed to bind publisher to `0.0.0.0` and change port to `4444` to bypass firewall restrictions.

3. **Multiple Subscribers**  
   - Three subscribers connected simultaneously to one publisher.  
   - All received identical messages (fan-out confirmed).

4. **Multiple Publishers / Multiple Subscribers**  
   - NEWS and ALERT publishers sending on different ports.  
   - Subscriber to NEWS only and multi-subscriber (NEWS+ALERT).  
   - Verified correct reception and interleaving of messages.

---

## 📝 Notes & Troubleshooting

- At first, subscribers received no messages until the publisher bind was changed to `0.0.0.0` instead of `localhost`.  
- In cross-host tests, port `15000` was blocked. Changing to `4444` solved the issue.  
- ZeroMQ PUB/SUB requires a small “warm-up” delay: subscribers must start after the publisher to avoid missing the first messages.  
- On Debian, it was necessary to activate the Python virtual environment and install `pyzmq`.  

---

## 👨‍💻 Authors

Developed for the **Distributed Systems Lab** by Carlos Castro and Freddy Valenzuela.

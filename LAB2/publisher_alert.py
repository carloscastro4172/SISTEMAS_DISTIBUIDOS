#!/usr/bin/env python3
import zmq
import time
import signal
import sys

def main():
    ctx = zmq.Context.instance()
    pub = ctx.socket(zmq.PUB)
    pub.bind("tcp://0.0.0.0:16000")
    print("[PUB ALERT] Bound on tcp://0.0.0.0:16000 (topic=ALERT)")

    # Breve warm-up para que los SUB se conecten
    time.sleep(0.5)

    try:
        i = 1
        while True:
            msg = f"ALERT High CPU usage! #{i}"
            pub.send(msg.encode())
            print("[PUB ALERT] ->", msg)
            i += 1
            time.sleep(3)
    except KeyboardInterrupt:
        print("\n[PUB ALERT] Stopping...")
    finally:
        pub.close(0)
        ctx.term()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main()

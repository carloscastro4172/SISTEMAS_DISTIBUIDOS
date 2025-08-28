#!/usr/bin/env python3
import zmq
import time
import signal
import sys

def main():
    ctx = zmq.Context.instance()
    pub = ctx.socket(zmq.PUB)
    pub.bind("tcp://0.0.0.0:15000")
    print("[PUB NEWS] Bound on tcp://0.0.0.0:15000 (topic=NEWS)")

    # Breve warm-up para que los SUB se conecten
    time.sleep(0.5)

    try:
        i = 1
        while True:
            msg = f"NEWS Breaking update #{i}"
            pub.send(msg.encode())
            print("[PUB NEWS] ->", msg)
            i += 1
            time.sleep(2)
    except KeyboardInterrupt:
        print("\n[PUB NEWS] Stopping...")
    finally:
        pub.close(0)
        ctx.term()

if __name__ == "__main__":
    # Manejo de Ctrl+C en Windows/Linux/Mac
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main()

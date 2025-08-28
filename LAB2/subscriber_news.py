#!/usr/bin/env python3
import zmq
import signal

def main():
    ctx = zmq.Context.instance()
    sub = ctx.socket(zmq.SUB)

    # Conéctate al publisher NEWS local (tu IP: 127.0.0.1)
    sub.connect("tcp://127.0.0.1:15000")
    sub.setsockopt_string(zmq.SUBSCRIBE, "NEWS")
    print("[SUB NEWS] Connected to tcp://127.0.0.1:15000 (topic=NEWS)")

    try:
        while True:
            msg = sub.recv().decode()
            print("[SUB NEWS] <-", msg)
    except KeyboardInterrupt:
        print("\n[SUB NEWS] Stopping...")
    finally:
        sub.close(0)
        ctx.term()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main()

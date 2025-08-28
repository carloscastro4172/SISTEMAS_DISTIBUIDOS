#!/usr/bin/env python3
import zmq
import signal

def main():
    ctx = zmq.Context.instance()
    sub = ctx.socket(zmq.SUB)

    # NEWS desde tu máquina local
    sub.connect("tcp://127.0.0.1:15000")

    # ALERT desde la máquina de tu compañero (172.23.199.4)
    sub.connect("tcp://172.23.199.4:16000")

    # Suscríbete a ambos tópicos
    sub.setsockopt_string(zmq.SUBSCRIBE, "NEWS")
    sub.setsockopt_string(zmq.SUBSCRIBE, "ALERT")

    print("[SUB MULTI] Connected to NEWS (127.0.0.1:15000) and ALERT (172.23.199.4:16000)")
    print("[SUB MULTI] Waiting for NEWS/ALERT...")

    try:
        while True:
            msg = sub.recv().decode()
            print("[SUB MULTI] <-", msg)
    except KeyboardInterrupt:
        print("\n[SUB MULTI] Stopping...")
    finally:
        sub.close(0)
        ctx.term()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main()

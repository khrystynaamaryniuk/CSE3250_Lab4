import os, time
from collections import OrderedDict
import paho.mqtt.client as mqtt

BROKER = os.getenv("BROKER_HOST", "broker0")
ROUNDS = int(os.getenv("ROUNDS", "5"))
TIMEOUT = float(os.getenv("TIMEOUT", "20.0"))

round_no = 0
winners = OrderedDict()

def log(msg):
    print(f"[tracker] {msg}", flush=True)

def on_connect(client, userdata, flags, rc):
    log(f"Connected to {BROKER} rc={rc}")
    client.subscribe("result", qos=1)

def on_message(client, userdata, msg):
    global round_no
    payload = msg.payload.decode("utf-8").strip()
    if round_no in winners:
        return
    if "wins" in payload or "won" in payload:
        winners[round_no] = "CC1" if "CC1" in payload else ("CC2" if "CC2" in payload else "UNKNOWN")
        log(f"Round {round_no} winner: {winners[round_no]} ({payload})")
        client.publish("blockData", "stop", qos=1)

def summary():
    print("\n========== SUMMARY ==========")
    print("Round | Winner")
    print("------+--------")
    for r, w in winners.items():
        print(f"{r:>5} | {w}")
    print("=============================\n")

def main():
    global round_no
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(BROKER, 1883, 60)
    client.loop_start()

    for i in range(1, ROUNDS + 1):
        round_no = i
        log(f"===== Starting round {round_no} =====")
        client.publish("mine", "start", qos=1)
        t0 = time.time()
        while (time.time() - t0) < TIMEOUT and round_no not in winners:
            time.sleep(0.1)
        if round_no not in winners:
            winners[round_no] = "TIMEOUT"
            log(f"Round {round_no} timed out.")
            client.publish("blockData", "stop", qos=1)
        time.sleep(1)

    summary()
    log("Done. Ctrl+C to stop.")
    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()

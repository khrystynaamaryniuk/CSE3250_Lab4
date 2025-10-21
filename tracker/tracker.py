import json
import time
from collections import defaultdict
import paho.mqtt.client as mqtt

wins_by_block = defaultdict(str)
block_no = 0

def on_message(client, userdata, message):
    global block_no
    payload = message.payload.decode('utf-8').strip()
    # Very simple parsing: look for 'CC1' or 'CC2' in the win message
    if "wins" in payload or "won" in payload:
        block_no += 1
        winner = "CC1" if "CC1" in payload else ("CC2" if "CC2" in payload else "UNKNOWN")
        wins_by_block[block_no] = winner
        print(f"[tracker] Block {block_no} winner: {winner} (msg='{payload}')")

def run_tracker():
    client = mqtt.Client()
    client.connect("broker0", 1883)
    client.subscribe("mine", qos=1)
    client.on_message = on_message
    print("[tracker] Listening on topic 'mine'...")
    client.loop_forever()

if __name__ == "__main__":
    run_tracker()


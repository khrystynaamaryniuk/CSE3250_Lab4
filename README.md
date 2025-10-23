## Clockchain MQTT Lab
This project simulates a simple blockchain (“Clockchain”) using MQTT and Docker.  
Two clients mine blocks, a Mosquitto broker handles messaging, and a tracker records the winner of each round.

Based on https://github.com/wonder-phil/ChainsThatBindUs.git
## How to Run

docker network create kmm
docker compose up --build

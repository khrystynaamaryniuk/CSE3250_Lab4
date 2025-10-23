 How to Run
  Create Docker network
  docker network create kmm
Build and start everything
  docker compose up --build
This automatically builds and runs:
  broker0 (Mosquitto broker)
  client1 (Miner 1)
  client2 (Miner 2)
  tracker (Round manager)

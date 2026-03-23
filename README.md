# Clockchain: Distributed Blockchain Mining with MQTT

A containerized distributed blockchain mining simulation that demonstrates concurrent mining clients competing to solve proof-of-work challenges using MQTT for inter-process communication.

## Overview

This project showcases a simplified blockchain ("Clockchain") where two competitive mining clients (`CC1` and `CC2`) attempt to mine blocks by finding hashes that meet a difficulty threshold. A central tracker orchestrates multiple mining rounds, determines winners, and logs results. Communication between all components happens asynchronously via MQTT, illustrating real-world pub/sub messaging patterns in distributed systems.

**Key Concepts Demonstrated:**
- Distributed systems communication via MQTT (Message Queuing Telemetry Transport)
- Proof-of-work blockchain mining simulation
- Container orchestration with Docker Compose
- Concurrent process competition and synchronization
- Resource-constrained environments (CPU limits per container)

## Project Structure

```
.
├── broker/                  # MQTT Broker (Mosquitto)
│   ├── Dockerfile
│   └── mosquitto.conf      # MQTT configuration with persistence
├── client1/                 # Mining Client 1 (CC1)
│   ├── CC1.py
│   ├── Dockerfile
│   └── requirements.txt
├── client2/                 # Mining Client 2 (CC2)
│   ├── CC2.py
│   ├── Dockerfile
│   └── requirements.txt
├── tracker/                 # Round Coordinator & Results Tracker
│   ├── tracker.py
│   ├── Dockerfile
│   └── requirements.txt
└── docker-compose.yml      # Multi-container orchestration
```

## Components

### Broker (`broker/`)
- **Mosquitto MQTT Broker**: Enables publish/subscribe communication between all components
- **Configuration**: Supports MQTT (port 1883) and WebSocket (port 9001) protocols
- **Features**: Message persistence, anonymous client access

### Mining Clients (`client1/` & `client2/`)
- **CC1**: Increments nonce by 1 per iteration (standard stride)
- **CC2**: Increments nonce by 3 per iteration (faster non-overlapping stride)
- **Common Logic**:
  - Subscribes to `mine` topic to receive start signals
  - Performs proof-of-work by computing SHA-256 hashes until finding one with N leading zeros
  - Publishes victory message to `result` topic when successful
  - Listens to `blockData` topic for stop signals

### Tracker (`tracker/`)
- **Responsibilities**: 
  - Orchestrates mining rounds (configurable count)
  - Sets timeout windows for each round
  - Identifies and logs round winners
  - Publishes final summary statistics
- **Configuration** (via environment variables):
  - `BROKER_HOST`: MQTT broker address
  - `ROUNDS`: Number of mining rounds to execute (default: 5)
  - `TIMEOUT`: Maximum seconds per round (default: 20)

## System Architecture

```
┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│  CC1 Client │         │  MQTT Broker │         │  CC2 Client │
│  (Mining)   │◄───────►│  (Mosquitto) │◄───────►│  (Mining)   │
└──────┬──────┘         └──────┬───────┘         └──────┬──────┘
       │                       │                        │
       │ publishes result      │ publishes mine         │
       └───────────────────────┼────────────────────────┘
                               │
                        ┌──────▼──────┐
                        │  Tracker    │
                        │  (Scoreboard)│
                        └─────────────┘
```

**Message Flow:**
1. **Tracker** publishes `"start"` on `mine` topic
2. **CC1 & CC2** wake up and begin mining (incrementing nonce, computing hashes)
3. **First client** to find valid hash publishes victory on `result` topic
4. **Tracker** records winner and publishes `"stop"` on `blockData` topic
5. **Losing client** stops mining and waits for next round
6. **Repeat** for configured number of rounds

## Getting Started

### Prerequisites
- Docker & Docker Compose
- macOS/Linux/Windows with Docker Desktop

### Installation & Execution

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Clockchain
   ```

2. **Create the Docker network** (if not already present)
   ```bash
   docker network create kmm
   ```

3. **Build and run all services**
   ```bash
   docker compose up --build
   ```

   This command will:
   - Build Docker images for all four services
   - Create containers with resource limits (0.25 CPU cores each)
   - Launch the broker, clients, and tracker
   - Display logs from all containers

4. **View results**
   - Watch tracker output in the console
   - Final summary shows round winners and any timeouts

5. **Stop all services**
   ```bash
   docker compose down
   ```

### Custom Configuration

Modify `docker-compose.yml` to adjust:
- **Number of rounds**: Change `ROUNDS` environment variable in tracker service
- **Round timeout**: Change `TIMEOUT` environment variable (seconds)
- **Port mappings**: Edit `ports` section in broker service
- **CPU limits**: Adjust `deploy.resources.limits.cpus` for each service

Example: Run 10 rounds with 30-second timeout
```yaml
environment:
  - BROKER_HOST=broker0
  - ROUNDS=10
  - TIMEOUT=30
```

## Technical Details

### Blockchain Mining Implementation
- **Difficulty**: Fixed at 5 leading zeros in SHA-256 hash
- **Nonce space exploration**:
  - **CC1**: Linear search (nonce += 1)
  - **CC2**: Faster stride (nonce += 3) to demonstrate computational advantage
- **Hash composition**: `SHA256(previous_hash + data + timestamp + nonce)`

### MQTT Messaging
| Topic | Publisher | Subscriber | Purpose |
|-------|-----------|------------|---------|
| `mine` | Tracker | CC1, CC2 | Start signal for mining round |
| `result` | CC1/CC2 | Tracker | Victory announcement |
| `blockData` | Tracker | CC1, CC2 | Stop signal to halt mining |


## Attribution

Based on the original concept from [Chains That Bind Us](https://github.com/wonder-phil/ChainsThatBindUs) by Phillip G. Bradford, adapted with MQTT integration for distributed messaging.

## License

Educational project - use for learning purposes.hain MQTT Lab
This project simulates a simple blockchain (“Clockchain”) using MQTT and Docker.  
Two clients mine blocks, a Mosquitto broker handles messaging, and a tracker records the winner of each round.

Based on https://github.com/wonder-phil/ChainsThatBindUs.git
## How to Run

docker network create kmm
docker compose up --build

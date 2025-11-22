# APT Simulation Framework

⚠️ **FOR AUTHORIZED PENETRATION TESTING ONLY**

This is an educational APT (Advanced Persistent Threat) simulation framework for authorized security testing and research.

## Features

### C2 Server
- Encrypted communications (Fernet encryption)
- Agent registration and management
- Command queuing and dispatch
- Interactive console for operators
- Multi-agent support

### Stealth Agent
- Encrypted C2 communication
- Beacon jitter for evasion
- User-agent randomization
- System information collection
- Remote command execution
- Persistence mechanisms (Linux)

### Security Features
- End-to-end encryption
- Password-based key derivation
- Obfuscation capabilities
- Stealth communication patterns

## Installation

```bash
cd apt-framework
pip install -r requirements.txt
```

## Usage

### Start C2 Server

```bash
python server/c2_server.py --host 127.0.0.1 --port 8443 --password YourPassword
```

### Start Agent

```bash
python agent/implant.py --c2 http://127.0.0.1:8443 --password YourPassword --interval 5
```

### C2 Console Commands

- `list` / `agents` - List all connected agents
- `use <agent_id>` - Select an agent to interact with
- `shell <command>` - Execute shell command on selected agent
- `sysinfo` - Get system information from agent
- `exit` - Exit console

## Architecture

```
apt-framework/
├── common/
│   ├── crypto.py      # Encryption and obfuscation
│   └── protocol.py    # Communication protocol
├── server/
│   └── c2_server.py   # Command & Control server
├── agent/
│   └── implant.py     # Stealth agent/implant
└── requirements.txt
```

## Legal Notice

This tool is intended for:
- Authorized penetration testing
- Security research in controlled environments
- Educational purposes
- CTF competitions

**UNAUTHORIZED USE IS ILLEGAL**

Always obtain written permission before testing any systems you do not own.

## Supported Commands

- `shell` - Execute shell commands
- `sysinfo` - Collect system information
- `sleep` - Modify beacon interval
- `kill` - Terminate agent

## Communication Protocol

1. Agent registers with C2 (encrypted)
2. Agent sends periodic beacons (heartbeat)
3. C2 queues commands for agents
4. Agent receives and executes commands
5. Agent returns results to C2

All communications are encrypted with Fernet (AES-128).

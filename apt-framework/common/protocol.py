"""
APT Framework - Communication Protocol
⚠️ FOR AUTHORIZED PENETRATION TESTING ONLY
"""

import json
import uuid
from datetime import datetime
from enum import Enum
from typing import Any, Dict


class MessageType(Enum):
    """Message types for C2 communication"""
    REGISTER = "register"
    HEARTBEAT = "heartbeat"
    COMMAND = "command"
    RESULT = "result"
    ERROR = "error"
    FILE_UPLOAD = "file_upload"
    FILE_DOWNLOAD = "file_download"


class Message:
    """Protocol message structure"""

    def __init__(
        self,
        msg_type: MessageType,
        agent_id: str = None,
        data: Any = None,
        command_id: str = None
    ):
        self.msg_id = str(uuid.uuid4())
        self.msg_type = msg_type.value
        self.agent_id = agent_id
        self.timestamp = datetime.utcnow().isoformat()
        self.data = data
        self.command_id = command_id

    def to_json(self) -> str:
        """Serialize to JSON"""
        return json.dumps({
            "msg_id": self.msg_id,
            "msg_type": self.msg_type,
            "agent_id": self.agent_id,
            "timestamp": self.timestamp,
            "data": self.data,
            "command_id": self.command_id
        })

    def to_bytes(self) -> bytes:
        """Serialize to bytes"""
        return self.to_json().encode('utf-8')

    @classmethod
    def from_json(cls, json_str: str) -> 'Message':
        """Deserialize from JSON"""
        data = json.loads(json_str)
        msg = cls(
            msg_type=MessageType(data["msg_type"]),
            agent_id=data.get("agent_id"),
            data=data.get("data"),
            command_id=data.get("command_id")
        )
        msg.msg_id = data["msg_id"]
        msg.timestamp = data["timestamp"]
        return msg

    @classmethod
    def from_bytes(cls, data: bytes) -> 'Message':
        """Deserialize from bytes"""
        return cls.from_json(data.decode('utf-8'))


class Command:
    """Command structure for agent execution"""

    def __init__(self, cmd_type: str, params: Dict[str, Any] = None):
        self.cmd_id = str(uuid.uuid4())
        self.cmd_type = cmd_type
        self.params = params or {}
        self.timestamp = datetime.utcnow().isoformat()

    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            "cmd_id": self.cmd_id,
            "cmd_type": self.cmd_type,
            "params": self.params,
            "timestamp": self.timestamp
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Command':
        """Create from dictionary"""
        cmd = cls(data["cmd_type"], data.get("params"))
        cmd.cmd_id = data["cmd_id"]
        cmd.timestamp = data["timestamp"]
        return cmd


# Supported command types
class CommandType:
    SHELL = "shell"  # Execute shell command
    DOWNLOAD = "download"  # Download file from agent
    UPLOAD = "upload"  # Upload file to agent
    SCREENSHOT = "screenshot"  # Take screenshot
    KEYLOG = "keylog"  # Start/stop keylogger
    PERSIST = "persist"  # Install persistence
    ELEVATE = "elevate"  # Attempt privilege escalation
    EXFILTRATE = "exfiltrate"  # Exfiltrate data
    SLEEP = "sleep"  # Change beacon interval
    KILL = "kill"  # Terminate agent
    SYSINFO = "sysinfo"  # Get system information

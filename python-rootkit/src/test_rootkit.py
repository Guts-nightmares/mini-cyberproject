"""
Test script for educational rootkit
⚠️ FOR EDUCATIONAL PURPOSES ONLY
"""

import os
import subprocess
import time
from pathlib import Path


def create_test_files():
    """Create test files for hiding"""
    test_dir = Path("/tmp/rootkit_test")
    test_dir.mkdir(exist_ok=True)

    # Create visible file
    visible_file = test_dir / "visible.txt"
    visible_file.write_text("This file is visible\n")

    # Create hidden file (with HIDE_ prefix)
    hidden_file = test_dir / "HIDE_secret.txt"
    hidden_file.write_text("This file should be hidden\n")

    print("✅ Test files created in /tmp/rootkit_test/")
    print(f"   - visible.txt (visible)")
    print(f"   - HIDE_secret.txt (should be hidden)")
    return test_dir


def test_file_hiding(test_dir: Path):
    """Test file hiding functionality"""
    print("\n" + "=" * 60)
    print("TEST: File Hiding")
    print("=" * 60)

    print("\n📂 Files in test directory (without rootkit):")
    subprocess.run(["ls", "-la", str(test_dir)])

    print("\n⚠️  Now activate the rootkit and run:")
    print(f"   ls -la {test_dir}")
    print("\nThe file HIDE_secret.txt should disappear!\n")


def test_process_hiding():
    """Test process hiding functionality"""
    print("\n" + "=" * 60)
    print("TEST: Process Hiding")
    print("=" * 60)

    print("\n🔍 To test process hiding:")
    print("1. Activate rootkit with hidden process:")
    print("   python rootkit_manager.py --hide-process sleep --activate")
    print("\n2. In the spawned shell, start a background process:")
    print("   sleep 1000 &")
    print("\n3. Check if it's hidden:")
    print("   ps aux | grep sleep")
    print("   ls /proc/ | grep [pid]")
    print("\nThe process should be hidden from ps and /proc listing!\n")


def demo_activation():
    """Show activation demo"""
    print("\n" + "=" * 60)
    print("DEMO: Rootkit Activation")
    print("=" * 60)

    print("\n🚀 Step-by-step activation:\n")
    print("1. Compile the rootkit:")
    print("   python rootkit_manager.py --compile")
    print()
    print("2. Activate with hidden items:")
    print("   python rootkit_manager.py --hide-file HIDE_secret.txt --activate")
    print()
    print("3. In the spawned shell, test hiding:")
    print("   ls /tmp/rootkit_test/")
    print("   cat /tmp/rootkit_test/HIDE_secret.txt  # Should fail")
    print()
    print("4. Exit the shell to deactivate:")
    print("   exit")
    print()


def main():
    """Main test function"""
    print("=" * 60)
    print("⚠️  EDUCATIONAL ROOTKIT - TEST SUITE")
    print("=" * 60)
    print()

    # Create test files
    test_dir = create_test_files()

    # Show tests
    test_file_hiding(test_dir)
    test_process_hiding()
    demo_activation()

    print("=" * 60)
    print("📚 For more information, see README.md")
    print("=" * 60)
    print()


if __name__ == "__main__":
    main()

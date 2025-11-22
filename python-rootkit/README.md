# Python LD_PRELOAD Rootkit

⚠️ **FOR EDUCATIONAL PURPOSES ONLY**

This is an educational demonstration of Linux rootkit techniques using LD_PRELOAD hooking. It shows how system calls can be intercepted to hide files, processes, and activities.

## ⚠️ WARNING

**NEVER use this tool on systems you don't own or without explicit written authorization.**

This tool is intended ONLY for:
- Educational purposes in controlled environments
- Security research in isolated Linux VMs
- Understanding rootkit techniques for defensive purposes
- Authorized penetration testing with written permission

## What is LD_PRELOAD?

LD_PRELOAD is a Linux environment variable that allows loading shared libraries before other libraries. This can be used to override standard library functions, enabling:
- Function hooking
- System call interception
- Behavior modification

## Features

### File Hiding
- Hide files/directories with magic prefix (`HIDE_`)
- Hide configured file patterns
- Intercepts: `readdir`, `readdir64`, `stat`, `lstat`, `fopen`

### Process Hiding
- Hide processes by name or pattern
- Hides from `/proc` filesystem
- Intercepts directory listing in `/proc`

### Configuration
- JSON-based configuration file
- Dynamic process/file hiding
- Pattern matching support

### Activation Modes
1. **User-specific**: Launch shell or command with LD_PRELOAD
2. **System-wide**: Install to `/etc/ld.so.preload` (requires root)

## How It Works

### Architecture

```
┌─────────────────────┐
│  Application (ls)   │
└──────────┬──────────┘
           │ calls readdir()
           ▼
┌─────────────────────┐
│  librootkit.so      │  ← Hooked functions
│  (LD_PRELOAD)       │     - Filter results
└──────────┬──────────┘     - Hide items
           │
           ▼
┌─────────────────────┐
│  libc.so            │  ← Original functions
│  (System Library)   │
└─────────────────────┘
```

### Hooking Mechanism

1. **LD_PRELOAD** loads our library first
2. Our library intercepts common functions:
   - `readdir()` / `readdir64()` - Directory listing
   - `stat()` / `lstat()` - File information
   - `fopen()` - File opening
3. Before returning to caller, we filter results
4. Hidden items are skipped/removed from output

## Installation & Setup

### Prerequisites

```bash
# Linux VM required
# Install gcc for compilation
sudo apt-get install gcc  # Debian/Ubuntu
sudo yum install gcc      # RHEL/CentOS
```

### Compilation

```bash
cd python-rootkit
python src/rootkit_manager.py --compile
```

This compiles `lib/rootkit.c` to `lib/librootkit.so`.

## Usage

### Basic File Hiding

```bash
# Hide files starting with HIDE_
python src/rootkit_manager.py --hide-file "HIDE_" --activate

# In the spawned shell:
touch /tmp/HIDE_secret.txt
ls /tmp/  # HIDE_secret.txt won't appear
```

### Process Hiding

```bash
# Hide processes containing "python3"
python src/rootkit_manager.py --hide-process "python3" --activate

# In the spawned shell:
python3 -c "import time; time.sleep(1000)" &
ps aux | grep python3  # Process hidden!
```

### Running Commands

```bash
# Run specific command with rootkit
python src/rootkit_manager.py --hide-file "secret" --activate -- ls -la /tmp
```

### Configuration Management

```bash
# Show current configuration
python src/rootkit_manager.py --show

# Load existing configuration
python src/rootkit_manager.py --load-config --activate
```

### System-Wide Installation (⚠️ Dangerous)

```bash
# Install for all processes (requires root)
sudo python src/rootkit_manager.py --install

# Uninstall
sudo python src/rootkit_manager.py --uninstall
```

## Testing

```bash
# Run test suite
python src/test_rootkit.py
```

This creates test files and provides step-by-step testing instructions.

## File Structure

```
python-rootkit/
├── lib/
│   ├── rootkit.c           # C library with hooked functions
│   └── librootkit.so       # Compiled shared library (after build)
├── src/
│   ├── rootkit_manager.py  # Python management tool
│   └── test_rootkit.py     # Test suite
└── README.md
```

## Technical Details

### Hooked Functions

| Function | Purpose | Hiding Technique |
|----------|---------|------------------|
| `readdir()` | Directory listing | Skip hidden entries |
| `readdir64()` | 64-bit directory listing | Skip hidden entries |
| `stat()` | File status | Return ENOENT |
| `lstat()` | Symbolic link status | Return ENOENT |
| `fopen()` | File opening | Return NULL |

### Configuration File

Location: `/tmp/.rootkit.conf`

Format:
```
PROCESS:python3
PROCESS:suspicious
FILE:HIDE_
FILE:secret
```

### Magic Prefix

Files/directories starting with `HIDE_` are automatically hidden.

## Detection & Defense

### How to Detect This Rootkit

1. **Check LD_PRELOAD**:
   ```bash
   echo $LD_PRELOAD
   cat /etc/ld.so.preload
   ```

2. **Compare with clean system**:
   ```bash
   # Run without LD_PRELOAD
   env -u LD_PRELOAD ls /proc
   ```

3. **Use static binaries**:
   ```bash
   # Static binaries ignore LD_PRELOAD
   /path/to/static/ls
   ```

4. **Check loaded libraries**:
   ```bash
   lsof | grep librootkit
   ```

### Defense Mechanisms

1. **Disable LD_PRELOAD** for privileged processes
2. **Monitor** `/etc/ld.so.preload` changes
3. **Use static binaries** for critical operations
4. **File integrity monitoring** (AIDE, Tripwire)
5. **Kernel-level** security (SELinux, AppArmor)

## Limitations

This educational rootkit:
- ✅ Hides from userland tools (ls, ps, etc.)
- ❌ Does NOT hide from kernel-level inspection
- ❌ Does NOT persist across reboots (unless installed)
- ❌ Can be detected by static binaries
- ❌ Doesn't work on SUID binaries

## Advanced Rootkit Techniques (Not Implemented)

For educational reference, advanced rootkits may use:
- **Kernel modules** (LKM rootkits)
- **Syscall table hooking**
- **/dev/kmem manipulation**
- **Bootkit techniques**
- **Hypervisor-level rootkits**

This implementation is intentionally limited to LD_PRELOAD for safety.

## Cleanup

```bash
# Remove configuration
rm /tmp/.rootkit.conf

# Uninstall system-wide (if installed)
sudo python src/rootkit_manager.py --uninstall

# Remove test files
rm -rf /tmp/rootkit_test
```

## Legal Notice

**UNAUTHORIZED USE IS ILLEGAL**

Using rootkits on systems you don't own or without authorization is illegal in most jurisdictions. This tool is for educational purposes only.

## Learning Objectives

This project demonstrates:
- LD_PRELOAD hooking mechanism
- Function interception techniques
- Library preloading on Linux
- System call manipulation
- Stealth techniques used by malware
- Defensive detection methods

## References

- `man ld.so` - Dynamic linker documentation
- `man dlsym` - Dynamic linking API
- Linux rootkit detection techniques
- Offensive security research papers

## Platform Support

- **Linux**: ✅ Fully supported
- **macOS**: ❌ Not supported (DYLD_INSERT_LIBRARIES has restrictions)
- **Windows**: ❌ Not supported (different hooking mechanisms)

This is specifically designed for Linux systems due to LD_PRELOAD availability.

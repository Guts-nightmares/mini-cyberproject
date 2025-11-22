"""
Automated Privilege Escalation Scanner
⚠️ FOR EDUCATIONAL PURPOSES ONLY

This tool scans for common privilege escalation vectors on Linux systems.
NEVER use this on systems you don't own or without authorization.
"""

import os
import pwd
import grp
import stat
import subprocess
import re
from pathlib import Path
from typing import List, Dict, Tuple
from dataclasses import dataclass
from enum import Enum


class Severity(Enum):
    """Finding severity levels"""
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    INFO = "INFO"


@dataclass
class Finding:
    """Represents a security finding"""
    title: str
    severity: Severity
    description: str
    evidence: str
    exploit_available: bool = False
    remediation: str = ""


class PrivilegeEscalationScanner:
    """Automated privilege escalation scanner"""

    def __init__(self):
        self.findings: List[Finding] = []
        self.current_user = os.getenv("USER")
        self.current_uid = os.getuid()
        self.current_gid = os.getgid()

        print("=" * 60)
        print("⚠️  PRIVILEGE ESCALATION SCANNER")
        print("⚠️  FOR AUTHORIZED TESTING ONLY")
        print("=" * 60)
        print(f"\n🔍 Scanning as: {self.current_user} (UID: {self.current_uid})")
        print()

    def run_command(self, cmd: str) -> Tuple[str, int]:
        """Run shell command and return output"""
        try:
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.stdout + result.stderr, result.returncode
        except:
            return "", -1

    def add_finding(self, finding: Finding):
        """Add a finding to the list"""
        self.findings.append(finding)

    def check_sudo_permissions(self):
        """Check sudo permissions"""
        print("[*] Checking sudo permissions...")

        output, returncode = self.run_command("sudo -l 2>&1")

        if "may run the following" in output.lower():
            # Parse sudo permissions
            lines = output.split('\n')
            sudo_cmds = []
            for line in lines:
                if line.strip().startswith('('):
                    sudo_cmds.append(line.strip())

            if sudo_cmds:
                self.add_finding(Finding(
                    title="Sudo Permissions Found",
                    severity=Severity.HIGH,
                    description=f"User {self.current_user} has sudo permissions",
                    evidence="\n".join(sudo_cmds),
                    exploit_available=True,
                    remediation="Review sudo permissions and apply principle of least privilege"
                ))

        # Check for NOPASSWD entries
        if "NOPASSWD" in output:
            self.add_finding(Finding(
                title="Sudo NOPASSWD Configuration",
                severity=Severity.CRITICAL,
                description="Sudo allows commands without password",
                evidence=output,
                exploit_available=True,
                remediation="Remove NOPASSWD entries from sudoers"
            ))

    def check_suid_binaries(self):
        """Check for SUID/SGID binaries"""
        print("[*] Checking SUID/SGID binaries...")

        # Common dangerous SUID binaries
        dangerous_suid = [
            'nmap', 'vim', 'nano', 'find', 'bash', 'sh',
            'more', 'less', 'perl', 'python', 'ruby',
            'cp', 'mv', 'awk', 'sed', 'lua', 'php'
        ]

        # Find SUID binaries
        output, _ = self.run_command("find / -type f -perm -4000 2>/dev/null")

        suid_bins = output.strip().split('\n')
        dangerous_found = []

        for binary in suid_bins:
            if not binary:
                continue

            basename = os.path.basename(binary)
            if any(dangerous in basename for dangerous in dangerous_suid):
                dangerous_found.append(binary)

        if dangerous_found:
            self.add_finding(Finding(
                title="Dangerous SUID Binaries Found",
                severity=Severity.CRITICAL,
                description="Found SUID binaries that can be exploited for privilege escalation",
                evidence="\n".join(dangerous_found),
                exploit_available=True,
                remediation="Remove SUID bit from unnecessary binaries"
            ))

        # Report all SUID binaries
        if suid_bins and suid_bins[0]:
            self.add_finding(Finding(
                title=f"SUID Binaries Found ({len(suid_bins)})",
                severity=Severity.INFO,
                description="List of all SUID binaries on system",
                evidence="\n".join(suid_bins[:20]) + ("\n... (truncated)" if len(suid_bins) > 20 else ""),
                remediation="Audit SUID binaries regularly"
            ))

    def check_writable_paths(self):
        """Check for writable sensitive paths"""
        print("[*] Checking writable sensitive paths...")

        sensitive_paths = [
            "/etc/passwd",
            "/etc/shadow",
            "/etc/sudoers",
            "/etc/crontab",
            "/root/.ssh",
            "/etc/ssh/sshd_config"
        ]

        writable = []
        for path in sensitive_paths:
            if os.path.exists(path):
                if os.access(path, os.W_OK):
                    writable.append(path)

        if writable:
            self.add_finding(Finding(
                title="Writable Sensitive Files",
                severity=Severity.CRITICAL,
                description="Current user can write to sensitive system files",
                evidence="\n".join(writable),
                exploit_available=True,
                remediation="Fix file permissions on sensitive files"
            ))

    def check_cron_jobs(self):
        """Check cron jobs for exploitation"""
        print("[*] Checking cron jobs...")

        # Check user crontab
        output, _ = self.run_command("crontab -l 2>/dev/null")
        if output and "no crontab" not in output.lower():
            self.add_finding(Finding(
                title="User Cron Jobs Found",
                severity=Severity.INFO,
                description=f"Cron jobs for {self.current_user}",
                evidence=output,
                remediation="Review cron jobs for potential exploitation"
            ))

        # Check system cron
        cron_dirs = ["/etc/cron.d", "/etc/cron.daily", "/etc/cron.hourly"]
        for cron_dir in cron_dirs:
            if os.path.exists(cron_dir):
                for file in os.listdir(cron_dir):
                    file_path = os.path.join(cron_dir, file)
                    if os.access(file_path, os.W_OK):
                        self.add_finding(Finding(
                            title="Writable Cron File",
                            severity=Severity.HIGH,
                            description="Writable cron file found",
                            evidence=file_path,
                            exploit_available=True,
                            remediation="Fix permissions on cron files"
                        ))

    def check_capabilities(self):
        """Check for dangerous Linux capabilities"""
        print("[*] Checking Linux capabilities...")

        output, _ = self.run_command("getcap -r / 2>/dev/null")

        dangerous_caps = ['cap_setuid', 'cap_setgid', 'cap_dac_override', 'cap_sys_admin']

        if output:
            lines = output.strip().split('\n')
            for line in lines:
                if any(cap in line.lower() for cap in dangerous_caps):
                    self.add_finding(Finding(
                        title="Dangerous Capability Found",
                        severity=Severity.HIGH,
                        description="Binary with dangerous capabilities",
                        evidence=line,
                        exploit_available=True,
                        remediation="Remove unnecessary capabilities"
                    ))

    def check_world_writable_dirs(self):
        """Check for world-writable directories in PATH"""
        print("[*] Checking world-writable directories...")

        path_var = os.getenv("PATH", "")
        paths = path_var.split(":")

        writable_paths = []
        for path in paths:
            if os.path.exists(path):
                st = os.stat(path)
                if st.st_mode & stat.S_IWOTH:  # World writable
                    writable_paths.append(path)

        if writable_paths:
            self.add_finding(Finding(
                title="World-Writable Directories in PATH",
                severity=Severity.HIGH,
                description="World-writable directories found in PATH",
                evidence="\n".join(writable_paths),
                exploit_available=True,
                remediation="Remove world-writable directories from PATH or fix permissions"
            ))

    def check_kernel_exploits(self):
        """Check kernel version for known exploits"""
        print("[*] Checking kernel version...")

        output, _ = self.run_command("uname -r")
        kernel_version = output.strip()

        # Known vulnerable kernel versions (examples)
        vulnerable_kernels = {
            "4.4.0": "DirtyCOW (CVE-2016-5195)",
            "3.13.0": "OverlayFS (CVE-2015-1328)",
            "2.6.37": "Full Nelson (CVE-2010-4258)"
        }

        for vuln_version, exploit in vulnerable_kernels.items():
            if kernel_version.startswith(vuln_version):
                self.add_finding(Finding(
                    title="Vulnerable Kernel Version",
                    severity=Severity.CRITICAL,
                    description=f"Kernel version {kernel_version} is vulnerable",
                    evidence=f"Exploit: {exploit}",
                    exploit_available=True,
                    remediation="Update kernel to latest version"
                ))

        self.add_finding(Finding(
            title="Kernel Version",
            severity=Severity.INFO,
            description="Current kernel version",
            evidence=kernel_version,
            remediation="Keep kernel updated"
        ))

    def check_docker_access(self):
        """Check Docker socket access"""
        print("[*] Checking Docker access...")

        if os.path.exists("/var/run/docker.sock"):
            if os.access("/var/run/docker.sock", os.W_OK):
                self.add_finding(Finding(
                    title="Docker Socket Writable",
                    severity=Severity.CRITICAL,
                    description="User has write access to Docker socket",
                    evidence="/var/run/docker.sock is writable",
                    exploit_available=True,
                    remediation="Restrict access to Docker socket"
                ))

        # Check docker group membership
        output, _ = self.run_command("groups")
        if "docker" in output:
            self.add_finding(Finding(
                title="Docker Group Membership",
                severity=Severity.HIGH,
                description="User is member of docker group",
                evidence=output,
                exploit_available=True,
                remediation="Remove user from docker group if not needed"
            ))

    def check_environment_variables(self):
        """Check for dangerous environment variables"""
        print("[*] Checking environment variables...")

        dangerous_vars = ["LD_PRELOAD", "LD_LIBRARY_PATH", "PYTHONPATH"]
        found = []

        for var in dangerous_vars:
            value = os.getenv(var)
            if value:
                found.append(f"{var}={value}")

        if found:
            self.add_finding(Finding(
                title="Dangerous Environment Variables",
                severity=Severity.MEDIUM,
                description="Environment variables that could be exploited",
                evidence="\n".join(found),
                exploit_available=True,
                remediation="Clear unnecessary environment variables"
            ))

    def check_nfs_exports(self):
        """Check NFS exports"""
        print("[*] Checking NFS exports...")

        if os.path.exists("/etc/exports"):
            try:
                with open("/etc/exports", "r") as f:
                    content = f.read()
                    if "no_root_squash" in content:
                        self.add_finding(Finding(
                            title="NFS no_root_squash Found",
                            severity=Severity.CRITICAL,
                            description="NFS export with no_root_squash option",
                            evidence=content,
                            exploit_available=True,
                            remediation="Remove no_root_squash from NFS exports"
                        ))
            except:
                pass

    def scan(self):
        """Run all checks"""
        print("\n🔍 Starting privilege escalation scan...\n")

        checks = [
            self.check_sudo_permissions,
            self.check_suid_binaries,
            self.check_writable_paths,
            self.check_cron_jobs,
            self.check_capabilities,
            self.check_world_writable_dirs,
            self.check_kernel_exploits,
            self.check_docker_access,
            self.check_environment_variables,
            self.check_nfs_exports
        ]

        for check in checks:
            try:
                check()
            except Exception as e:
                print(f"[!] Error in {check.__name__}: {e}")

        print("\n✅ Scan complete!\n")

    def generate_report(self):
        """Generate findings report"""
        print("=" * 60)
        print("PRIVILEGE ESCALATION SCAN REPORT")
        print("=" * 60)
        print()

        # Group by severity
        by_severity = {
            Severity.CRITICAL: [],
            Severity.HIGH: [],
            Severity.MEDIUM: [],
            Severity.LOW: [],
            Severity.INFO: []
        }

        for finding in self.findings:
            by_severity[finding.severity].append(finding)

        # Print summary
        print("📊 SUMMARY")
        print("-" * 60)
        for severity in [Severity.CRITICAL, Severity.HIGH, Severity.MEDIUM, Severity.LOW, Severity.INFO]:
            count = len(by_severity[severity])
            if count > 0:
                print(f"  {severity.value}: {count}")
        print()

        # Print findings by severity
        for severity in [Severity.CRITICAL, Severity.HIGH, Severity.MEDIUM, Severity.LOW, Severity.INFO]:
            findings = by_severity[severity]
            if not findings:
                continue

            print(f"\n{'=' * 60}")
            print(f"{severity.value} FINDINGS ({len(findings)})")
            print(f"{'=' * 60}\n")

            for i, finding in enumerate(findings, 1):
                print(f"[{i}] {finding.title}")
                print(f"    Severity: {finding.severity.value}")
                print(f"    Exploit Available: {'Yes' if finding.exploit_available else 'No'}")
                print(f"    Description: {finding.description}")
                if finding.evidence:
                    evidence_lines = finding.evidence.split('\n')[:5]
                    print(f"    Evidence:")
                    for line in evidence_lines:
                        print(f"      {line}")
                    if len(finding.evidence.split('\n')) > 5:
                        print(f"      ... (truncated)")
                if finding.remediation:
                    print(f"    Remediation: {finding.remediation}")
                print()

        # Print exploitable findings
        exploitable = [f for f in self.findings if f.exploit_available and f.severity in [Severity.CRITICAL, Severity.HIGH]]
        if exploitable:
            print("\n" + "=" * 60)
            print(f"🎯 EXPLOITABLE FINDINGS ({len(exploitable)})")
            print("=" * 60)
            for finding in exploitable:
                print(f"  • {finding.title} [{finding.severity.value}]")
            print()


def main():
    """Main function"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Automated Privilege Escalation Scanner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
⚠️  FOR AUTHORIZED TESTING ONLY
This tool scans for privilege escalation vectors.
NEVER use on systems you don't own or without authorization.
        """
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Verbose output"
    )

    args = parser.parse_args()

    scanner = PrivilegeEscalationScanner()
    scanner.scan()
    scanner.generate_report()


if __name__ == "__main__":
    main()

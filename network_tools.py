import subprocess
import re
from typing import Dict, Optional


def ping(host: str, count: int = 4) -> str:
    try:
        if subprocess.run(['which', 'ping'], capture_output=True, text=True).returncode == 0:
            cmd = ['ping', '-c', str(count), host]
        else:
            cmd = ['ping', '-n', str(count), host]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        return result.stdout + result.stderr
    except Exception as e:
        return f"Ping failed: {str(e)}"


def traceroute(host: str, max_hops: int = 30) -> str:
    try:
        if subprocess.run(['which', 'traceroute'], capture_output=True, text=True).returncode == 0:
            cmd = ['traceroute', '-m', str(max_hops), host]
        elif subprocess.run(['which', 'tracert'], capture_output=True, text=True).returncode == 0:
            cmd = ['tracert', '-h', str(max_hops), host]
        else:
            return "Traceroute/tracert command not found"
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        return result.stdout + result.stderr
    except Exception as e:
        return f"Traceroute failed: {str(e)}"


def nslookup(domain: str, server: Optional[str] = None) -> str:
    try:
        cmd = ['nslookup', domain]
        if server:
            cmd.append(server)
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        return result.stdout + result.stderr
    except Exception as e:
        return f"NSLookup failed: {str(e)}"


def check_port(host: str, port: int) -> str:
    import socket
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex((host, port))
        sock.close()
        if result == 0:
            return f"Port {port} on {host} is OPEN"
        else:
            return f"Port {port} on {host} is CLOSED or unreachable"
    except Exception as e:
        return f"Port check failed: {str(e)}"


def get_local_network_info() -> str:
    try:
        if subprocess.run(['which', 'ip'], capture_output=True, text=True).returncode == 0:
            cmd = ['ip', 'addr']
        elif subprocess.run(['which', 'ifconfig'], capture_output=True, text=True).returncode == 0:
            cmd = ['ifconfig']
        elif subprocess.run(['which', 'ipconfig'], capture_output=True, text=True).returncode == 0:
            cmd = ['ipconfig', '/all']
        else:
            return "No network info command found"
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        return result.stdout
    except Exception as e:
        return f"Failed to get network info: {str(e)}"

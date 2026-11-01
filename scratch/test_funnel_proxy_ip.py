import sys
import re
import ipaddress

def is_tailnet_or_local_ip(ip: str) -> bool:
    if ip in ("127.0.0.1", "localhost", "::1", "testclient"):
        return True
    try:
        addr = ipaddress.ip_address(ip)
        tailnet_network = ipaddress.ip_network("100.64.0.0/10")
        return addr in tailnet_network
    except Exception:
        return False

def get_real_client_ip(headers: dict, client_host: str) -> str:
    forwarded = headers.get("x-forwarded-for") or headers.get("X-Forwarded-For")
    if forwarded:
        # Take the first client IP in chain
        return forwarded.split(",")[0].strip()
    return client_host

# Test 1: Direct localhost
assert is_tailnet_or_local_ip(get_real_client_ip({}, "127.0.0.1")) == True

# Test 2: Tailscale Serve from private tailnet
assert is_tailnet_or_local_ip(get_real_client_ip({"x-forwarded-for": "100.105.42.12"}, "127.0.0.1")) == True

# Test 3: Tailscale Funnel from public internet
# Request arrives at localhost:8000 with X-Forwarded-For = 203.144.144.166
public_ip = get_real_client_ip({"x-forwarded-for": "203.144.144.166"}, "127.0.0.1")
assert is_tailnet_or_local_ip(public_ip) == False, "Public Funnel IP must be detected as non-tailnet!"

print("Tailscale Funnel Real Client IP detection tests passed 100%!")

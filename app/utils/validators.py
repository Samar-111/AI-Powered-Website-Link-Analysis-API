import ipaddress
import socket
from urllib.parse import urlparse

FORBIDDEN_HOSTS = {
    "localhost",
    "127.0.0.1",
    "0.0.0.0",
    "::1",
    "metadata.google.internal",
    "169.254.169.254",
    "instance-data"
}

def is_forbidden_ip(ip_str: str) -> bool:
    try:
        ip = ipaddress.ip_address(ip_str)
        return (
            ip.is_private
            or ip.is_loopback
            or ip.is_link_local
            or ip.is_multicast
            or ip.is_reserved
            or ip.is_unspecified
        )
    except ValueError:
        return False

def validate_and_sanitize_url(url: str, check_dns: bool = True) -> str:
    if not url or not isinstance(url, str):
        raise ValueError("URL must be a non-empty string.")

    cleaned_url = url.strip()
    if "://" in cleaned_url:
        if not cleaned_url.startswith(("http://", "https://")):
            scheme = cleaned_url.split("://")[0]
            raise ValueError(f"Invalid URL scheme '{scheme}'. Only http and https are supported.")
    else:
        cleaned_url = "https://" + cleaned_url

    parsed = urlparse(cleaned_url)
    if not parsed.scheme or parsed.scheme not in ("http", "https"):
        raise ValueError(f"Invalid URL scheme '{parsed.scheme}'. Only http and https are supported.")

    hostname = parsed.hostname
    if not hostname:
        raise ValueError("The provided URL does not contain a valid domain or hostname.")

    lowered_host = hostname.lower()
    if lowered_host in FORBIDDEN_HOSTS or lowered_host.endswith(".local") or lowered_host.endswith(".internal"):
        raise ValueError("Access to local, private, or metadata networks is prohibited (SSRF protection).")

    if check_dns:
        try:
            addr_info = socket.getaddrinfo(hostname, None)
            for entry in addr_info:
                ip_addr = entry[4][0]
                if is_forbidden_ip(ip_addr):
                    raise ValueError(f"Domain '{hostname}' resolves to a restricted/private IP address ({ip_addr}). Request denied.")
        except socket.gaierror:
            raise ValueError(f"Could not resolve domain '{hostname}'. Please provide a valid, accessible domain.")

    return cleaned_url

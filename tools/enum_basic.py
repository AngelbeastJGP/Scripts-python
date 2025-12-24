#!/usr/bin/env python3

import os
import sys
import subprocess

def banner():
    print("=" * 50)
    print(" Basic Enumeration Script - Angelbeast ")
    print("=" * 50)

def check_args():
    if len(sys.argv) != 2:
        print(f"Uso: {sys.argv[0]} <IP>")
        sys.exit(1)
    return sys.argv[1]

def ping_host(ip):
    print("\n[+] Comprobando conectividad...")
    subprocess.run(["ping", "-c", "1", ip])

def fast_scan(ip):
    print("\n[+] Escaneo rápido de puertos...")
    subprocess.run(["nmap", "-p-", "--min-rate", "1000", ip, "-oN", "nmap_fast.txt"])

def full_scan(ip):
    print("\n[+] Escaneo profundo de servicios...")
    subprocess.run(["nmap", "-sC", "-sV", ip, "-oN", "nmap_full.txt"])

def main():
    banner()
    ip = check_args()
    ping_host(ip)
    fast_scan(ip)
    full_scan(ip)
    print("\n[+] Enumeración básica completada.")

if __name__ == "__main__":
    main()

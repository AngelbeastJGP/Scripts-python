#!/usr/bin/env python3
import os
import re
import sys
import subprocess
from datetime import datetime

def banner():
    print("=" * 60)
    print(" Basic Enumeration Script v2 - Angelbeast ")
    print("=" * 60)

def run(cmd, outfile=None):
    """
    Ejecuta un comando. Si outfile está definido, guarda stdout en ese archivo.
    """
    try:
        if outfile:
            with open(outfile, "w", encoding="utf-8") as f:
                subprocess.run(cmd, stdout=f, stderr=subprocess.STDOUT, check=False)
        else:
            subprocess.run(cmd, check=False)
    except FileNotFoundError:
        print(f"[!] Comando no encontrado: {cmd[0]}")
        sys.exit(1)

def usage_exit(prog):
    print(f"Uso: {prog} <IP> [nombre_objetivo]")
    print(f"Ejemplo: {prog} 10.10.10.10 meow")
    sys.exit(1)

def parse_open_ports(nmap_fast_path):
    """
    Extrae puertos abiertos del output de nmap en formato normal (-oN).
    Devuelve: '22,80,445'
    """
    ports = []
    port_line = re.compile(r"^(\d+)/tcp\s+open")
    with open(nmap_fast_path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            m = port_line.match(line.strip())
            if m:
                ports.append(m.group(1))
    return ",".join(ports)

def summarize(nmap_full_path):
    """
    Muestra resumen de puertos/servicios a partir del full scan.
    """
    lines = []
    with open(nmap_full_path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            if re.match(r"^\d+/tcp\s+open", line):
                lines.append(line.rstrip())
    return lines

def main():
    banner()

    if len(sys.argv) < 2:
        usage_exit(sys.argv[0])

    ip = sys.argv[1].strip()
    name = sys.argv[2].strip() if len(sys.argv) >= 3 else ip.replace(".", "_")

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    outdir = os.path.join(os.getcwd(), f"{name}_{ts}")
    os.makedirs(outdir, exist_ok=True)

    print(f"\n[+] Target: {ip}")
    print(f"[+] Output: {outdir}")

    # 1) Ping
    print("\n[+] Ping...")
    run(["ping", "-c", "1", ip], outfile=os.path.join(outdir, "ping.txt"))

    # 2) Fast scan
    print("\n[+] Nmap fast scan (-p-)...")
    fast_path = os.path.join(outdir, "nmap_fast.txt")
    run(["nmap", "-p-", "--min-rate", "1000", ip, "-oN", fast_path])

    # 3) Parse ports
    ports = parse_open_ports(fast_path)
    if not ports:
        print("\n[!] No se detectaron puertos abiertos en el fast scan.")
        print("[!] Revisa el archivo nmap_fast.txt por si hay filtros/firewall.")
        sys.exit(0)

    print(f"\n[+] Puertos abiertos detectados: {ports}")

    # 4) Full scan sobre puertos encontrados
    print("\n[+] Nmap full scan (-sC -sV) sobre puertos detectados...")
    full_path = os.path.join(outdir, "nmap_full.txt")
    run(["nmap", "-sC", "-sV", "-p", ports, ip, "-oN", full_path])

    # 5) Resumen
    print("\n[+] Resumen (puerto/servicio):")
    for l in summarize(full_path):
        print("   " + l)

    print("\n[+] Listo. Revisa los archivos dentro de la carpeta de output.")

if __name__ == "__main__":
    main()

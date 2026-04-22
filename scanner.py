import os
import platform
import socket
import csv
from datetime import datetime

# -------- CONFIG --------
network_prefix = "192.168.1."   # Change to your network
start_ip = 1
end_ip = 50

ports_to_scan = [22, 80, 443]   # SSH, HTTP, HTTPS
timeout = 1

output_file = "scan_results.csv"

# -------- FUNCTIONS --------

def ping_host(ip):
    param = "-n" if platform.system().lower() == "windows" else "-c"
    command = f"ping {param} 1 {ip}"
    return os.system(command) == 0


def scan_ports(ip):
    open_ports = []
    for port in ports_to_scan:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((ip, port))
        if result == 0:
            open_ports.append(port)
        sock.close()
    return open_ports


# -------- MAIN --------

print("Starting Network Scan...")
start_time = datetime.now()

results = []

for i in range(start_ip, end_ip + 1):
    ip = network_prefix + str(i)
    print(f"Scanning {ip}...")

    if ping_host(ip):
        print(f"{ip} is UP")
        open_ports = scan_ports(ip)
        results.append([ip, "UP", ",".join(map(str, open_ports))])
    else:
        print(f"{ip} is DOWN")
        results.append([ip, "DOWN", ""])

# -------- SAVE TO CSV --------

with open(output_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["IP Address", "Status", "Open Ports"])
    writer.writerows(results)

end_time = datetime.now()

print("\nScan Complete!")
print(f"Results saved to {output_file}")
print(f"Duration: {end_time - start_time}")

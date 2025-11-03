import pygame
import sys
import random
import math
import time
from datetime import datetime, timedelta
import hashlib
import socket
import requests
import threading

# Initialize Pygame
pygame.init()
WIDTH, HEIGHT = 1600, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("FCTUC SECURITY COMMAND CENTER - PORT 452")

# Colors
DARK_SPACE = (5, 10, 25)
NASA_BLUE = (0, 100, 200)
SECURITY_GREEN = (0, 255, 100)
SECURITY_RED = (255, 50, 50)
SECURITY_YELLOW = (255, 255, 0)
HOLO_CYAN = (100, 255, 255)

# Fonts
font_small = pygame.font.SysFont('consolas', 14)
font_medium = pygame.font.SysFont('consolas', 18)
font_large = pygame.font.SysFont('consolas', 24)
font_title = pygame.font.SysFont('consolas', 32, bold=True)

class DynamicAccessSystem:
    def __init__(self):
        self.port = 452
        self.access_codes = {}
        self.last_code_update = datetime.now()
        self.code_interval = 360  # 6 minutes
        self.generate_new_codes()
        
    def generate_new_codes(self):
        """Generate new access codes every 6 minutes"""
        timestamp = int(time.time() // self.code_interval)
        base_seed = f"katchaw451_{timestamp}"
        
        self.access_codes = {
            'login': hashlib.sha256(f"{base_seed}_login".encode()).hexdigest()[:8],
            'password': hashlib.sha256(f"{base_seed}_password".encode()).hexdigest()[:12],
            'admin_token': hashlib.sha256(f"{base_seed}_admin".encode()).hexdigest()[:16]
        }
        self.last_code_update = datetime.now()
        
    def get_time_remaining(self):
        """Get time remaining until next code rotation"""
        next_update = self.last_code_update + timedelta(seconds=self.code_interval)
        remaining = next_update - datetime.now()
        return max(0, int(remaining.total_seconds()))
        
    def verify_access(self, login, password):
        """Verify access credentials"""
        if datetime.now() - self.last_code_update > timedelta(seconds=self.code_interval):
            self.generate_new_codes()
            
        return (login == self.access_codes['login'] and 
                password == self.access_codes['password'])

class IPGeolocation:
    def __init__(self):
        self.threat_database = {}
        self.suspicious_ips = set()
        
    def get_ip_info(self, ip_address):
        """Get geolocation information for IP address"""
        # Simulated geolocation data
        countries = ['United States', 'China', 'Russia', 'Brazil', 'Germany', 
                    'France', 'Japan', 'South Korea', 'India', 'Unknown']
        
        return {
            'ip': ip_address,
            'country': random.choice(countries),
            'city': 'Unknown',
            'isp': 'Unknown',
            'threat_level': random.choice(['LOW', 'MEDIUM', 'HIGH']),
            'latitude': random.uniform(-90, 90),
            'longitude': random.uniform(-180, 180)
        }
    
    def analyze_threat(self, ip_info):
        """Analyze IP threat level"""
        high_risk_countries = ['China', 'Russia', 'North Korea']
        if ip_info['country'] in high_risk_countries:
            ip_info['threat_level'] = 'HIGH'
            self.suspicious_ips.add(ip_info['ip'])
        
        return ip_info

class NetworkSecurity:
    def __init__(self):
        self.wifi_networks = []
        self.current_wifi = None
        self.malicious_ips = set()
        self.connection_log = []
        
    def scan_wifi_networks(self):
        """Scan for available WiFi networks"""
        networks = [
            {'ssid': 'FCTUC_Secure_1', 'signal': 95, 'security': 'WPA3'},
            {'ssid': 'Home_Network', 'signal': 80, 'security': 'WPA2'},
            {'ssid': 'Quantum_Shield', 'signal': 70, 'security': 'WPA3'},
            {'ssid': 'Public_WiFi', 'signal': 60, 'security': 'WEP'},
        ]
        
        # Sort by signal strength and security
        networks.sort(key=lambda x: (x['security'] == 'WPA3', x['signal']), reverse=True)
        self.wifi_networks = networks
        self.current_wifi = networks[0] if networks else None
        
        return networks
    
    def block_malicious_ip(self, ip_address):
        """Block malicious IP address"""
        if ip_address not in self.malicious_ips:
            self.malicious_ips.add(ip_address)
            self.connection_log.append({
                'timestamp': datetime.now(),
                'action': 'BLOCKED',
                'ip': ip_address,
                'reason': 'Suspicious activity'
            })
            print(f"🚫 BLOCKED malicious IP: {ip_address}")
    
    def enforce_wifi_only(self):
        """Enforce WiFi-only policy"""
        if not self.current_wifi:
            print("⚠️  NO WIFI CONNECTION - Isolating system...")
            # In real implementation, this would disable other network interfaces
            return False
        return True

class SecurityDashboard:
    def __init__(self):
        self.access_system = DynamicAccessSystem()
        self.geolocation = IPGeolocation()
        self.network = NetworkSecurity()
        self.active_threats = []
        self.last_scan = datetime.now()
        
        # Start background services
        self.start_background_services()
    
    def start_background_services(self):
        """Start background security monitoring"""
        def threat_monitor():
            while True:
                self.monitor_threats()
                time.sleep(10)
        
        def code_updater():
            while True:
                time.sleep(1)
                if self.access_system.get_time_remaining() == 0:
                    self.access_system.generate_new_codes()
                    print("🔄 Access codes updated!")
        
        threading.Thread(target=threat_monitor, daemon=True).start()
        threading.Thread(target=code_updater, daemon=True).start()
    
    def monitor_threats(self):
        """Monitor for security threats"""
        # Simulate threat detection
        if random.random() < 0.3:
            threat_types = [
                "Port Scan Detected", "Brute Force Attempt", "DNS Spoofing",
                "Malware Beacon", "Data Exfiltration", "Zero-Day Exploit"
            ]
            
            # Generate random attacker IP
            attacker_ip = f"192.168.1.{random.randint(2, 254)}"
            ip_info = self.geolocation.get_ip_info(attacker_ip)
            ip_info = self.geolocation.analyze_threat(ip_info)
            
            threat = {
                'type': random.choice(threat_types),
                'timestamp': datetime.now(),
                'attacker_ip': attacker_ip,
                'ip_info': ip_info,
                'severity': ip_info['threat_level']
            }
            
            self.active_threats.append(threat)
            
            # Block high threat IPs
            if ip_info['threat_level'] == 'HIGH':
                self.network.block_malicious_ip(attacker_ip)
            
            # Keep only recent threats
            self.active_threats = [t for t in self.active_threats 
                                 if (datetime.now() - t['timestamp']).seconds < 300]
    
    def draw_nasa_interface(self, surface):
        """Draw NASA-style interface"""
        # Dark space background
        surface.fill(DARK_SPACE)
        
        # Stars
        for _ in range(100):
            x = random.randint(0, WIDTH)
            y = random.randint(0, HEIGHT)
            size = random.randint(1, 3)
            brightness = random.randint(100, 255)
            pygame.draw.circle(surface, (brightness, brightness, brightness), (x, y), size)
        
        # Header with NASA-style branding
        header_rect = pygame.Rect(0, 0, WIDTH, 80)
        pygame.draw.rect(surface, (0, 30, 60), header_rect)
        pygame.draw.line(surface, NASA_BLUE, (0, 80), (WIDTH, 80), 2)
        
        title = font_title.render("FCTUC SECURITY COMMAND CENTER", True, HOLO_CYAN)
        surface.blit(title, (WIDTH//2 - title.get_width()//2, 20))
        
        subtitle = font_medium.render("PORT 452 - CLASSIFIED ACCESS ONLY", True, SECURITY_GREEN)
        surface.blit(subtitle, (WIDTH//2 - subtitle.get_width()//2, 55))
    
    def draw_access_panel(self, surface):
        """Draw dynamic access code panel"""
        panel_rect = pygame.Rect(50, 100, 400, 200)
        pygame.draw.rect(surface, (10, 30, 50), panel_rect, border_radius=10)
        pygame.draw.rect(surface, NASA_BLUE, panel_rect, 3, border_radius=10)
        
        title = font_large.render("DYNAMIC ACCESS SYSTEM", True, HOLO_CYAN)
        surface.blit(title, (70, 120))
        
        # Access codes
        time_remaining = self.access_system.get_time_remaining()
        codes = self.access_system.access_codes
        
        code_info = [
            f"Login: {codes['login']}",
            f"Password: {'*' * len(codes['password'])}",
            f"Admin Token: {codes['admin_token'][:8]}...",
            f"Code Refresh: {time_remaining // 60}:{time_remaining % 60:02d}"
        ]
        
        for i, info in enumerate(code_info):
            color = SECURITY_GREEN if i < 3 else SECURITY_YELLOW
            code_text = font_medium.render(info, True, color)
            surface.blit(code_text, (70, 160 + i * 30))
        
        # Access instructions
        instructions = [
            "ACCESS INSTRUCTIONS:",
            "• Codes rotate every 6 minutes",
            "• Use PORT 452 for connections",
            "• Admin home computer required",
            "• WiFi-only security policy"
        ]
        
        for i, instruction in enumerate(instructions):
            inst_text = font_small.render(instruction, True, SECURITY_GREEN)
            surface.blit(inst_text, (70, 280 + i * 20))
    
    def draw_threat_radar(self, surface, x, y, size=200):
        """Draw threat radar display"""
        # Radar background
        pygame.draw.circle(surface, (0, 20, 40), (x, y), size)
        pygame.draw.circle(surface, NASA_BLUE, (x, y), size, 2)
        
        # Radar lines
        for angle in range(0, 360, 30):
            rad_angle = math.radians(angle)
            end_x = x + math.cos(rad_angle) * size
            end_y = y + math.sin(rad_angle) * size
            pygame.draw.line(surface, (0, 50, 100), (x, y), (end_x, end_y), 1)
        
        # Sweeping line
        sweep_angle = (time.time() * 50) % 360
        rad_angle = math.radians(sweep_angle)
        end_x = x + math.cos(rad_angle) * size
        end_y = y + math.sin(rad_angle) * size
        pygame.draw.line(surface, HOLO_CYAN, (x, y), (end_x, end_y), 2)
        
        # Plot threats
        for threat in self.active_threats[-10:]:  # Last 10 threats
            ip_hash = hash(threat['attacker_ip'])
            angle = (ip_hash % 360) + time.time() * 10
            distance = (ip_hash % 80) + 20
            
            rad_angle = math.radians(angle % 360)
            threat_x = x + math.cos(rad_angle) * distance
            threat_y = y + math.sin(rad_angle) * distance
            
            color = SECURITY_RED if threat['severity'] == 'HIGH' else SECURITY_YELLOW
            pygame.draw.circle(surface, color, (int(threat_x), int(threat_y)), 4)
    
    def draw_network_panel(self, surface):
        """Draw network security panel"""
        panel_rect = pygame.Rect(500, 100, 500, 300)
        pygame.draw.rect(surface, (10, 30, 50), panel_rect, border_radius=10)
        pygame.draw.rect(surface, NASA_BLUE, panel_rect, 3, border_radius=10)
        
        title = font_large.render("NETWORK SECURITY", True, HOLO_CYAN)
        surface.blit(title, (520, 120))
        
        # WiFi status
        networks = self.network.scan_wifi_networks()
        current_wifi = self.network.current_wifi
        
        wifi_text = font_medium.render(f"Active WiFi: {current_wifi['ssid'] if current_wifi else 'NONE'}", 
                                     True, SECURITY_GREEN)
        surface.blit(wifi_text, (520, 160))
        
        security_text = font_medium.render(f"Security: {current_wifi['security'] if current_wifi else 'NONE'}", 
                                        True, SECURITY_GREEN)
        surface.blit(security_text, (520, 190))
        
        # Blocked IPs
        blocked_text = font_medium.render(f"Blocked IPs: {len(self.network.malicious_ips)}", 
                                       True, SECURITY_RED)
        surface.blit(blocked_text, (520, 220))
        
        # Security policy
        policy_text = font_small.render("SECURITY POLICY: WiFi-Only • Home Server • No External Internet", 
                                      True, SECURITY_YELLOW)
        surface.blit(policy_text, (520, 250))
        
        # Draw threat radar
        self.draw_threat_radar(surface, 750, 250, 80)
    
    def draw_threat_intel(self, surface):
        """Draw threat intelligence panel"""
        panel_rect = pygame.Rect(1050, 100, 500, 300)
        pygame.draw.rect(surface, (10, 30, 50), panel_rect, border_radius=10)
        pygame.draw.rect(surface, NASA_BLUE, panel_rect, 3, border_radius=10)
        
        title = font_large.render("THREAT INTELLIGENCE", True, HOLO_CYAN)
        surface.blit(title, (1070, 120))
        
        # Recent threats
        recent_threats = self.active_threats[-5:]  # Last 5 threats
        
        if recent_threats:
            for i, threat in enumerate(recent_threats):
                time_str = threat['timestamp'].strftime("%H:%M:%S")
                threat_text = font_small.render(
                    f"{time_str} - {threat['type']}", 
                    True, SECURITY_RED if threat['severity'] == 'HIGH' else SECURITY_YELLOW
                )
                surface.blit(threat_text, (1070, 160 + i * 25))
                
                ip_text = font_small.render(
                    f"IP: {threat['attacker_ip']} ({threat['ip_info']['country']})", 
                    True, HOLO_CYAN
                )
                surface.blit(ip_text, (1070, 175 + i * 25))
        else:
            safe_text = font_medium.render("No active threats detected", True, SECURITY_GREEN)
            surface.blit(safe_text, (1070, 160))
    
    def draw_satellite_view(self, surface):
        """Draw satellite geolocation view"""
        panel_rect = pygame.Rect(50, 320, 1000, 500)
        pygame.draw.rect(surface, (10, 30, 50), panel_rect, border_radius=10)
        pygame.draw.rect(surface, NASA_BLUE, panel_rect, 3, border_radius=10)
        
        title = font_large.render("SATELLITE THREAT TRACKING", True, HOLO_CYAN)
        surface.blit(title, (70, 340))
        
        # Draw world map simulation
        map_rect = pygame.Rect(100, 380, 900, 400)
        pygame.draw.rect(surface, (0, 20, 40), map_rect)
        pygame.draw.rect(surface, (0, 50, 100), map_rect, 2)
        
        # Plot threat locations
        for threat in self.active_threats[-20:]:
            ip_info = threat['ip_info']
            if 'latitude' in ip_info and 'longitude' in ip_info:
                # Convert to map coordinates
                map_x = 100 + (ip_info['longitude'] + 180) / 360 * 900
                map_y = 380 + (90 - ip_info['latitude']) / 180 * 400
                
                color = SECURITY_RED if threat['severity'] == 'HIGH' else SECURITY_YELLOW
                pygame.draw.circle(surface, color, (int(map_x), int(map_y)), 6)
                
                # Pulse effect for high threats
                if threat['severity'] == 'HIGH':
                    pulse = (math.sin(time.time() * 5) + 1) / 2
                    radius = 6 + int(pulse * 8)
                    pygame.draw.circle(surface, (255, 0, 0, 100), (int(map_x), int(map_y)), radius, 2)
    
    def draw_control_panel(self, surface):
        """Draw security control panel"""
        panel_rect = pygame.Rect(1070, 420, 500, 400)
        pygame.draw.rect(surface, (10, 30, 50), panel_rect, border_radius=10)
        pygame.draw.rect(surface, NASA_BLUE, panel_rect, 3, border_radius=10)
        
        title = font_large.render("SECURITY CONTROLS", True, HOLO_CYAN)
        surface.blit(title, (1090, 440))
        
        controls = [
            ("F1", "Emergency Lockdown", "Isolate all systems"),
            ("F2", "Rotate Access Codes", "Generate new credentials"),
            ("F3", "Block Suspicious IPs", "Active threat mitigation"),
            ("F4", "WiFi Security Scan", "Verify network integrity"),
            ("F5", "Threat Analysis", "Deep scan for anomalies"),
            ("F6", "System Integrity", "Check all security layers")
        ]
        
        for i, (key, action, description) in enumerate(controls):
            # Control button
            btn_rect = pygame.Rect(1090, 480 + i * 60, 460, 40)
            btn_color = (0, 50, 100) if i % 2 == 0 else (0, 40, 80)
            
            pygame.draw.rect(surface, btn_color, btn_rect, border_radius=5)
            pygame.draw.rect(surface, HOLO_CYAN, btn_rect, 2, border_radius=5)
            
            # Button text
            key_text = font_medium.render(key, True, SECURITY_YELLOW)
            action_text = font_medium.render(action, True, (255, 255, 255))
            desc_text = font_small.render(description, True, SECURITY_GREEN)
            
            surface.blit(key_text, (1100, 490 + i * 60))
            surface.blit(action_text, (1150, 490 + i * 60))
            surface.blit(desc_text, (1100, 510 + i * 60))
    
    def handle_controls(self, key):
        """Handle control key presses"""
        if key == pygame.K_F1:
            print("🚨 EMERGENCY LOCKDOWN ACTIVATED!")
            # Isolate system
            self.network.enforce_wifi_only()
            
        elif key == pygame.K_F2:
            print("🔄 Rotating access codes...")
            self.access_system.generate_new_codes()
            
        elif key == pygame.K_F3:
            print("🛡️  Blocking suspicious IPs...")
            for threat in self.active_threats:
                if threat['severity'] in ['HIGH', 'MEDIUM']:
                    self.network.block_malicious_ip(threat['attacker_ip'])
                    
        elif key == pygame.K_F4:
            print("📡 Scanning WiFi security...")
            self.network.scan_wifi_networks()
            
        elif key == pygame.K_F5:
            print("🔍 Running threat analysis...")
            self.monitor_threats()
            
        elif key == pygame.K_F6:
            print("⚙️  Checking system integrity...")
            # Verify all systems are running
            systems_ok = all([
                self.access_system.get_time_remaining() > 0,
                self.network.current_wifi is not None,
                len(self.network.malicious_ips) < 100  # Reasonable threshold
            ])
            print(f"System Integrity: {'✅ OK' if systems_ok else '❌ COMPROMISED'}")
    
    def run(self):
        """Run the security dashboard"""
        clock = pygame.time.Clock()
        running = True
        
        print("🚀 Starting FCTUC Security Command Center...")
        print(f"🔐 Access Port: {self.access_system.port}")
        print("📡 Initializing satellite tracking...")
        print("🛡️  WiFi-only security policy: ACTIVE")
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key in [pygame.K_F1, pygame.K_F2, pygame.K_F3, 
                                     pygame.K_F4, pygame.K_F5, pygame.K_F6]:
                        self.handle_controls(event.key)
            
            # Update display
            self.draw_nasa_interface(screen)
            self.draw_access_panel(screen)
            self.draw_network_panel(screen)
            self.draw_threat_intel(screen)
            self.draw_satellite_view(screen)
            self.draw_control_panel(screen)
            
            # Footer
            footer_text = font_medium.render(
                f"FCTUC SECURITY SYSTEM ACTIVE | "
                f"Home Server: ONLINE | "
                f"Threats: {len(self.active_threats)} | "
                f"Time: {datetime.now().strftime('%H:%M:%S')}", 
                True, SECURITY_GREEN
            )
            screen.blit(footer_text, (WIDTH//2 - footer_text.get_width()//2, HEIGHT - 30))
            
            pygame.display.flip()
            clock.tick(60)
        
        pygame.quit()
        print("🛑 Security system shut down safely.")

if __name__ == "__main__":
    dashboard = SecurityDashboard()
    dashboard.run()

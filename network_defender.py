#!/usr/bin/env python3
"""
FCTUC Network Defender
WiFi-only security with malicious IP blocking
"""

import subprocess
import psutil
import time
import threading
from datetime import datetime

class NetworkDefender:
    def __init__(self):
        self.allowed_wifi_ssids = ['FCTUC_Secure_1', 'Home_Network', 'Quantum_Shield']
        self.blocked_ips = set()
        self.security_log = []
        
    def get_current_wifi(self):
        """Get current WiFi network"""
        try:
            # Linux-specific WiFi detection
            result = subprocess.run(['nmcli', '-t', '-f', 'ACTIVE,SSID', 'dev', 'wifi'], 
                                  capture_output=True, text=True)
            
            for line in result.stdout.strip().split('\n'):
                if line.startswith('yes:'):
                    return line.split(':')[1]
                    
        except Exception as e:
            print(f"WiFi detection error: {e}")
            
        return None
    
    def is_approved_wifi(self, ssid):
        """Check if WiFi SSID is approved"""
        return ssid in self.allowed_wifi_ssids if ssid else False
    
    def block_ip(self, ip_address):
        """Block IP address using iptables"""
        if ip_address not in self.blocked_ips:
            try:
                # Block incoming traffic
                subprocess.run(['sudo', 'iptables', '-A', 'INPUT', '-s', ip_address, '-j', 'DROP'], 
                             check=True)
                # Block outgoing traffic  
                subprocess.run(['sudo', 'iptables', '-A', 'OUTPUT', '-d', ip_address, '-j', 'DROP'],
                             check=True)
                
                self.blocked_ips.add(ip_address)
                self.log_security_event(f"BLOCKED_IP {ip_address}")
                print(f"🚫 Blocked IP: {ip_address}")
                
            except subprocess.CalledProcessError as e:
                print(f"IP blocking failed: {e}")
    
    def monitor_network_connections(self):
        """Monitor network connections for suspicious activity"""
        while True:
            try:
                current_wifi = self.get_current_wifi()
                
                if not self.is_approved_wifi(current_wifi):
                    print("⚠️  Unapproved WiFi - Isolating network...")
                    self.isolate_network()
                else:
                    # Check for suspicious connections
                    connections = psutil.net_connections()
                    for conn in connections:
                        if conn.status == 'ESTABLISHED' and conn.raddr:
                            remote_ip = conn.raddr.ip
                            # Check if IP is suspicious (simplified)
                            if self.is_suspicious_ip(remote_ip):
                                self.block_ip(remote_ip)
                
                time.sleep(10)
                
            except Exception as e:
                print(f"Network monitoring error: {e}")
                time.sleep(30)
    
    def is_suspicious_ip(self, ip):
        """Determine if IP is suspicious"""
        # Simple heuristic - in real implementation, use threat intelligence
        suspicious_patterns = [
            ip.startswith('192.168.1.') and int(ip.split('.')[-1]) > 200,
            ip.startswith('10.0.0.') and int(ip.split('.')[-1]) < 10,
        ]
        
        return any(suspicious_patterns)
    
    def isolate_network(self):
        """Isolate system from network"""
        try:
            # Disable network interfaces except loopback
            interfaces = psutil.net_if_stats()
            for interface, stats in interfaces.items():
                if interface != 'lo' and stats.isup:
                    subprocess.run(['sudo', 'ip', 'link', 'set', interface, 'down'], 
                                 check=True)
                    print(f"🔒 Disabled interface: {interface}")
                    
        except Exception as e:
            print(f"Network isolation error: {e}")
    
    def log_security_event(self, event):
        """Log security events"""
        log_entry = {
            'timestamp': datetime.now(),
            'event': event
        }
        self.security_log.append(log_entry)
        
        # Keep only last 1000 events
        if len(self.security_log) > 1000:
            self.security_log.pop(0)

def main():
    defender = NetworkDefender()
    
    print("🛡️  FCTUC Network Defender Started")
    print("📡 Monitoring WiFi connections...")
    print("🔒 Enforcing WiFi-only security policy")
    
    # Start monitoring in background thread
    monitor_thread = threading.Thread(target=defender.monitor_network_connections)
    monitor_thread.daemon = True
    monitor_thread.start()
    
    try:
        # Keep main thread alive
        while True:
            time.sleep(60)
            # Periodic status report
            current_wifi = defender.get_current_wifi()
            print(f"📊 Status: WiFi={current_wifi} | Blocked IPs: {len(defender.blocked_ips)}")
            
    except KeyboardInterrupt:
        print("\n🛑 Network Defender stopped")

if __name__ == "__main__":
    main()

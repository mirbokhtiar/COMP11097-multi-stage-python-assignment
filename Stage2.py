import platform
import subprocess
import socket
import re

# === Validation Helpers ===
def is_valid_ip(address):
    pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
    if re.match(pattern, address):
        parts = address.split('.')
        return all(0 <= int(part) <= 255 for part in parts)
    return False

def is_valid_hostname(name):
    if is_valid_ip(name):
        return False
    return bool(re.match(r"^(?!\-)([A-Za-z0-9\-]{1,63}\.)+[A-Za-z]{2,6}$", name))

def is_host_up(host):
    command = ['ping', '-n', '1', host] if platform.system().lower() == 'windows' else ['ping', '-c', '1', host]
    try:
        result = subprocess.run(command, capture_output=True, text=True)
        return result.returncode == 0
    except Exception:
        return False

# === Menu Option M: Ping (with back option) ===
def menu_option_M():
    print("\n--- Ping Tool ---")
    while True:
        target = input("Enter a host name or IP address to ping (or type 'back' to return): ").strip()
        if target.lower() == 'back':
            return
        if not (is_valid_ip(target) or is_valid_hostname(target)):
            print("❌ Invalid host name or IP address. Please try again.")
            continue

        command = ['ping', '-n', '4', target] if platform.system().lower() == 'windows' else ['ping', '-c', '4', target]
        print(f"\n🔍 Pinging {target}...\n")
        try:
            result = subprocess.run(command, capture_output=True, text=True)
            print(result.stdout)
            status = "✅ Host is UP.\n" if result.returncode == 0 else "❌ Host appears to be DOWN.\n"
            print(status)
        except Exception as e:
            print(f"⚠️ Error while pinging: {e}")

# === Menu Option I: Port Scan (with back option) ===
def menu_option_I():
    print("\n--- Port Scan Tool ---")
    while True:
        host = input("Enter a host name or IP to scan (or type 'back' to return): ").strip()
        if host.lower() == 'back':
            return
        if is_valid_ip(host) or is_valid_hostname(host):
            break
        print("❌ Invalid host or IP. Please try again.")

    print(f"\n🔍 Checking if host {host} is up...\n")
    if not is_host_up(host):
        print(f"❌ {host} appears to be DOWN. All ports are assumed to be CLOSED.\n")
        return
    else:
        print(f"✅ {host} is UP. Proceeding with port scan...\n")

    while True:
        print("\nChoose scan method:")
        print("1 - Common ports")
        print("2 - Port range (e.g., 20-100)")
        print("3 - Specific ports (comma-separated)")
        print("Type 'back' to return to the main menu.")

        method = input("Enter your choice (1/2/3/back): ").strip().lower()
        if method == 'back':
            return
        elif method == '1':
            ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 8080]
            break
        elif method == '2':
            range_input = input("Enter port range (e.g., 20-100 or type 'back' to return): ").strip()
            if range_input.lower() == 'back':
                return
            try:
                start, end = map(int, range_input.split('-'))
                ports = list(range(start, end + 1))
                break
            except:
                print("❌ Invalid range format. Try again.")
        elif method == '3':
            port_list = input("Enter ports (comma-separated, or type 'back' to return): ").strip()
            if port_list.lower() == 'back':
                return
            try:
                ports = [int(p.strip()) for p in port_list.split(',') if p.strip().isdigit()]
                if ports:
                    break
                else:
                    print("❌ No valid ports entered.")
            except:
                print("❌ Invalid input. Please try again.")
        else:
            print("❌ Invalid selection. Please choose 1, 2, 3, or 'back'.")

    print(f"\n🔎 Scanning {host} on selected ports...\n")
    for port in ports:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                result = s.connect_ex((host, port))
                if result == 0:
                    print(f"✅ Port {port} is OPEN")
                else:
                    print(f"❌ Port {port} is CLOSED")
        except Exception as e:
            print(f"⚠️ Error scanning port {port}: {e}")

# === Menu Option R: Route Trace (with back option) ===
def menu_option_R():
    print("\n--- Route Trace Tool ---")
    while True:
        target = input("Enter a host name or IP address to trace (or type 'back' to return): ").strip()
        if target.lower() == 'back':
            return
        if not (is_valid_ip(target) or is_valid_hostname(target)):
            print("❌ Invalid host name or IP address. Please try again.")
            continue

        command = ['tracert', target] if platform.system().lower() == 'windows' else ['traceroute', target]
        print(f"\n📍 Tracing route to {target}...\n")
        try:
            result = subprocess.run(command, capture_output=True, text=True)
            print(result.stdout)
        except Exception as e:
            print(f"⚠️ Error during route trace: {e}")

# === Menu Option B: Help ===
def menu_option_B():
    print("\n--- Help Menu ---")
    print("""
M - Ping:
    • Enter a host name or IP address to ping.
    • The tool validates the input and shows if the host is UP or DOWN.
    • You can type 'back' to return to the menu.

I - Port Scan:
    • Enter a host or IP and scan for open ports.
    • Choose from common ports, a range (e.g., 20-100), or specific ports (e.g., 80,443).
    • If the host is down, scanning is skipped.
    • Type 'back' to return during any step.

R - Route Trace:
    • Enter a host or IP to trace the route.
    • Displays each network hop.
    • You can type 'back' to cancel and return to the menu.

B - Help:
    • Displays this help message explaining all menu options.

Q - Quit:
    • Exits the program.
""")

# === Main Menu ===
def main_menu():
    while True:
        print("\n===== Welcome to the MIRB Network Tool Menu =====")
        print("M - Ping")
        print("I - Port Scan")
        print("R - Route Trace")
        print("B - Help")
        print("Q - Quit")

        choice = input("Enter your choice: ").strip().upper()
        if choice == 'M':
            menu_option_M()
        elif choice == 'I':
            menu_option_I()
        elif choice == 'R':
            menu_option_R()
        elif choice == 'B':
            menu_option_B()
        elif choice == 'Q':
            print("👋 Exiting the program. Goodbye!")
            break
        else:
            print("❌ Invalid input. Please enter M, I, R, B, or Q.")

# === Run the Program ===
if __name__ == "__main__":
    main_menu()

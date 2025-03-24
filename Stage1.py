# === Stage 1: Menu System with Stub Functions ===

def menu_option_M():
    print("You selected option M (Ping) — [Stub Function]")

def menu_option_I():
    print("You selected option I (Port Scan) — [Stub Function]")

def menu_option_R():
    print("You selected option R (Route Trace) — [Stub Function]")

def menu_option_B():
    print("You selected option B (Help) — [Stub Function]")

def main_menu():
    while True:
        print("\n===== Welcome to the MIRB Network Tool Menu =====")
        print("Please choose an option:")
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
            print("Thank you for using the MIRB Menu. Goodbye!")
            break
        else:
            print("❌ Invalid input. Please enter M, I, R, B, or Q.")

# === Run the Program ===
if __name__ == "__main__":
    main_menu()

import sys
from time import sleep
from database import init_db, clear_screen, load_data
from manager import Manager
from doctor import Doctor

def get_password_masked(prompt="Password: ", mask="*"):
    print(prompt, end="", flush=True)
    password = ""
    if sys.platform.startswith("win"):
        import msvcrt
        while True:
            ch = msvcrt.getwch()
            if ch in ("\r", "\n"):
                print()
                return password
            if ch == "\x08" and password:
                password = password[:-1]
                print("\b \b", end="", flush=True)
            elif ch.isprintable():
                password += ch
                print(mask, end="", flush=True)
    else:
        import tty, termios
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            while True:
                ch = sys.stdin.read(1)
                if ch in ("\r", "\n"):
                    print()
                    return password
                if ch in ("\x7f", "\b") and password:
                    password = password[:-1]
                    print("\b \b", end="", flush=True)
                elif ch.isprintable():
                    password += ch
                    print(mask, end="", flush=True)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)

def login():
    init_db()
    while True:
        clear_screen()
        print("═" * 50)
        print("        💊 CLINIC MANAGEMENT SYSTEM 💉")
        print("═" * 50)
        print("1. Manager 👔")
        print("2. Doctor 🩺")
        print("3. Exit 🚪")
        choice = input("\nSelect role (1-3): ").strip()

        if choice == '3':
            print("\nEscaping system... Thank you! 👋\n")
            sys.exit(0)
        if choice not in ['1', '2']:
            input("Invalid! Press Enter...")
            continue

        role = "Manager" if choice == '1' else "Doctor"
        username = input(f"{role} Username: ").strip()
        if not username:
            continue

        password = get_password_masked("Password: ")
        print("\r \nPlease wait, verifying credentials... ⚠️")
        sleep(1)

        users = load_data("users.txt")
        for user in users:
            if len(user) >= 3 and user[0] == username and user[1] == password and user[2] == role:
                obj = Manager(username) if role == "Manager" else Doctor(username)
                obj.login()
                return obj

        print("\nInvalid credentials! ❌")
        input("\nPress Enter to retry...")

def main():
    while True:
        user = login()
        user.show_menu()
        input(f"\n{user._role} logged out successfully. Press Enter to continue...")

if __name__ == "__main__":
    main()

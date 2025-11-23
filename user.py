class User:
    def __init__(self, username):
        self.username = username
        self._role = "User"
        self._is_logged_in = False

    def login(self):
        if not self._is_logged_in:
            self._is_logged_in = True
            print(f"{self.username} logged in as {self._role}. ✅")
            self._notify("Welcome back! ✅")
        else:
            print(f"{self.username} is already logged in. ❗")

    def logout(self):
        if self._is_logged_in:
            self._is_logged_in = False
            self._notify("You have been logged out. ✅")
        else:
            print(f"{self.username} is already logged out. ❗")

    def _notify(self, msg):
        print(f"Notification: {msg}")

    def _header(self):
        from database import clear_screen
        clear_screen()
        print(f" Hello {self.username} 👋| Role: {self._role}")
        print("═" * 50)
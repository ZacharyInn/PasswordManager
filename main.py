from cryptography.fernet import Fernet

class PasswordManager:

    def __init__(self):
        self.key = None
        self.password_file = None
        self.password_dict = {}

    #option 1, creates a new encryption key, should end in .key
    def create_key(self, path):
        self.key = Fernet.generate_key()
        with open(path, 'wb') as f:
            f.write(self.key)

    #option 2, loads an existing encryption key, should end in .key
    def load_key(self, path):
        with open(path, 'rb') as f:
            self.key = f.read()

    #option 3, creates a new password file
    def create_pass_file(self, path, initial_values = None):
        self.password_file = path

        if initial_values is not None:
            for key, value in initial_values.items():
                self.add_password(key, value)

    #option 4, loads an existing password file
    def load_pass_file(self, path):
        self.passoword_file = path
        with open(path, 'r') as f:
            for line in f:
                site, encrypted = line.split(":")
                self.password_dict[site] = Fernet(self.key).decrypt(encrypted.encode()).decode()
    
    #option 5, adds a new password to a new site
    def add_password(self, site, password):
        self.password_dict[site] = password

        if self.password_file is not None:
            with open(self.password_file, 'a+') as f:
                encrypted = Fernet(self.key).encrypt(password.encode())
                f.write(site + ":" + encrypted.decode() + "\n")

    #option 6, gets the password of an existing site
    def get_password(self, site):
        return self.password_dict[site]


def main():
    password = {}

    pm = PasswordManager()

    print("""Password Manager Menu:
    (1) Create a new key
    (2) Load an existing key
    (3) Create new password file
    (4) Load exisiting password file
    (5) Add a new password
    (6) Get a password
    (7) Exit
    """)    

    done = False
    while not done:
        choice = input("Enter your choice: ")
        if choice == "1":
            path = input("Enter new key name (must end in .key): ")
            pm.create_key(path)
        elif choice == "2":
            path = input("Enter key name: ")
            pm.load_key(path)
        elif choice == "3":
            path = input("Enter new password file name: ")
            pm.create_pass_file(path, password)
        elif choice == "4":
            path = input("Enter password file name: ")
            pm.load_pass_file(path)
        elif choice == "5":
            site = input("Enter the website name: ")
            password = input("Enter the new password: ")
            pm.add_password(site, password)
        elif choice == "6":
            site = input("Which website's password do you want?: ")
            print(f"Password for {site} is {pm.get_password(site)}")
        elif choice == "7":
            done = True
            print("Exiting...")
        else:
            print("Error, invalid choice.")

if __name__ == "__main__":
    main()
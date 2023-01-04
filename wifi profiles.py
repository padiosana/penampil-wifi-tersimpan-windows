import subprocess

def save_log(log):
    file_path = input("Enter the file path to save the log: ")
    with open(file_path, "w") as f:
        f.write(log)
    print("Log saved successfully!")

profiles = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output=True).stdout

lines = profiles.splitlines()

log = ""

for line in lines:
    if b"Profile" in line:
        profile_name = line.split(b":")[1].strip()

        result = subprocess.run(["netsh", "wlan", "show", "profile", profile_name, "key=clear"], capture_output=True)

        lines = result.stdout.splitlines()

        for line in lines:
            if b"Key Content" in line:
                password = line.split(b":")[1].strip()
                log += f"---------------------------\n"
                log += f"SSID     : {profile_name.decode()}\n"
                log += f"password : {password.decode()}\n"
                log += f"---------------------------\n"
                print(f"---------------------------")
                print(f"SSID     : {profile_name.decode()}")
                print(f"password : {password.decode()}")
                print(f"---------------------------")

while True:
    choice = input("Enter 's' to save the log, 'e' to exit: ")
    if choice == "s":
        save_log(log)
    elif choice == "e":
        break
    else:
        print("Invalid choice. Please try again.")

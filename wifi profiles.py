import os
import subprocess
import multiprocessing

def save_log(log):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_name = "wifi_passwords_log.txt"
    file_path = os.path.join(script_dir, file_name)
    
    with open(file_path, "w") as f:
        f.write(log)
    print(f"\nLog saved successfully to: {file_path}\n")

def scan_wifi():
    profiles = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output=True).stdout

    lines = profiles.splitlines()

    ssid_list = [line.split(b":")[1].strip() for line in lines if b"Profile" in line]

    with multiprocessing.Pool() as pool:
        results = pool.map(scan_password, ssid_list)

    ssid_passwords = [(ssid, password) for ssid, password in results if password]

    # Mengurutkan SSID berdasarkan huruf dan kapitalisasi
    ssid_passwords = sorted(ssid_passwords, key=lambda x: x[0].lower())

    return ssid_passwords

def scan_password(ssid):
    result = subprocess.run(["netsh", "wlan", "show", "profile", ssid, "key=clear"], capture_output=True)
    lines = result.stdout.splitlines()

    for line in lines:
        if b"Key Content" in line:
            password = line.split(b":")[1].strip()
            return ssid.decode(), password.decode()

    return ssid.decode(), None

def print_wifi(ssid_passwords):
    log = "No.  SSID                           Password\n"
    log += "--------------------------------------------\n"

    print("No.  SSID                           Password")
    print("--------------------------------------------")

    for idx, (ssid, password) in enumerate(ssid_passwords, start=1):
        ssid_format = f"{idx:2}.  {ssid:<30}  {password}"
        log += f"{ssid_format}\n"

        print(ssid_format)

    log += "--------------------------------------------\n"
    return log

def main():
    ssid_passwords = scan_wifi()
    log = print_wifi(ssid_passwords)

    while True:
        print("\nMenu:")
        print("1. Save log")
        print("2. Rescan Wi-Fi")
        print("3. Exit")
        choice = input("Enter the number of your choice: ")

        if choice == "1":
            save_log(log)
        elif choice == "2":
            print("\nScanning Wi-Fi networks...\n")
            ssid_passwords = scan_wifi()
            log = print_wifi(ssid_passwords)
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

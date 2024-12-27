import os
import json
import datetime
import hashlib
import platform
import argparse

LICENSE_FILE = "tmp/licenses.json"

def get_key_from_device():
    """Generate unique key based on device information."""
    hostname = platform.node()
    system_info = platform.system() + platform.machine()
    raw_data = f"{hostname}-{system_info}"
    hashed_id = hashlib.sha256(raw_data.encode()).hexdigest()[:33]
    return hashed_id

def generate_license():
    """Generate a license key and save it to a file."""
    license_key = get_key_from_device()
    try:
        with open(LICENSE_FILE, "r") as file:
            licenses = json.load(file)
    except FileNotFoundError:
        licenses = {}

    if license_key in licenses:
        print("License already exists:")
        print(f"License Key: {licenses[license_key]['license_key']}")
        print(f"Expiry Date: {licenses[license_key]['expiry_date']}")
    else:
        expiry_date = (datetime.datetime.now() + datetime.timedelta(days=30)).strftime("%d-%m-%Y")
        licenses[license_key] = {
            "license_key": license_key,
            "expiry_date": expiry_date
        }

        os.makedirs(os.path.dirname(LICENSE_FILE), exist_ok=True)
        with open(LICENSE_FILE, "w") as file:
            json.dump(licenses, file, indent=4)
        print("License created successfully:")
        print(f"License Key: {license_key}")
        print(f"Expiry Date: {expiry_date}")

def main():
    parser = argparse.ArgumentParser(description="License Generator Tool")
    parser.add_argument("--generate", action="store_true", help="Generate a new license")
    args = parser.parse_args()

    if args.generate:
        generate_license()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

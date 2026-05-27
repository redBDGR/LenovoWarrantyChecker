import requests
import sys
import re
import json

def main():
    if len(sys.argv) != 2:
        print("Usage: python GetLenovoWarranty.py <serial_number>")
        sys.exit(1)

    serialNumber = sys.argv[1]

    # Initial product lookup
    initUrl = f"https://pcsupport.lenovo.com/au/en/api/v4/mse/getproducts?productId={serialNumber}"
    print(f"Requesting initial machine data from: {initUrl}")

    try:
        initInfo = requests.get(initUrl, timeout=10).json()
    except requests.exceptions.RequestException as e:
        print(f"Failed to reach Lenovo API: {e}")
        sys.exit(1)

    if not initInfo:
        print("No results returned from Lenovo API. Check the serial number.")
        sys.exit(1)

    # Extract machine type from ID
    # Example: LAPTOPS-AND-NETBOOKS/.../21NS/21NS00QKAU/PF60DP5X -> 21NS
    match = re.search(r"/([A-Z0-9]+)/\1[A-Z0-9]+/", initInfo[0]['Id'])
    if not match:
        print("No machine type found in Id, this indicates a RegEx or data failure.")
        print(initInfo[0]['Id'])
        sys.exit(1)

    machineType = match.group(1)

    if not machineType:
        sys.exit(1)

    # Request warranty and device info
    formatDeviceData = {
        "serialNumber": initInfo[0]['Serial'],
        "machineType":  machineType,
        "country":      "au",
        "language":     "en"
    }

    try:
        deviceInfo = requests.post(
            "https://pcsupport.lenovo.com/au/en/api/v4/upsell/redport/getIbaseInfo",
            json=formatDeviceData,
            timeout=10
        ).json()
    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve warranty info: {e}")
        sys.exit(1)

    print(json.dumps(deviceInfo, indent=4))

if __name__ == "__main__":
    main()
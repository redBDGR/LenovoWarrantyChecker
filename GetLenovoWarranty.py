import requests
import sys
import re
import json

def main():
    if len(sys.argv) != 2:
        print("Usage: python GetLenovoWarranty.py <serial_number>", file=sys.stderr)
        sys.exit(1)

    serial_number = sys.argv[1]

    init_url = f"https://pcsupport.lenovo.com/au/en/api/v4/mse/getproducts?productId={serial_number}"
    print(f"Requesting initial machine data from: {init_url}", file=sys.stderr)

    try:
        response = requests.get(init_url, timeout=10)
        response.raise_for_status()
        init_info = response.json()
    except requests.exceptions.HTTPError as e:
        print(f"Lenovo API returned an error: {e}", file=sys.stderr)
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"Failed to reach Lenovo API: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError:
        print("Lenovo API returned an unexpected response (not JSON).", file=sys.stderr)
        sys.exit(1)

    if not init_info:
        print("No results returned from Lenovo API. Check the serial number.", file=sys.stderr)
        sys.exit(1)

    try:
        product_id = init_info[0]['Id']
        serial = init_info[0]['Serial']
    except (KeyError, IndexError):
        print("Unexpected response structure from Lenovo API.", file=sys.stderr)
        sys.exit(1)

    # Extract machine type from ID
    # Example: LAPTOPS-AND-NETBOOKS/.../21NS/21NS00QKAU/XXXXXXXXXXXX -> 21NS
    match = re.search(r"/([A-Z0-9]+)/\1[A-Z0-9]+/", product_id)
    if not match:
        print(f"Could not parse machine type from product ID: {product_id}", file=sys.stderr)
        sys.exit(1)

    machine_type = match.group(1)

    payload = {
        "serialNumber": serial,
        "machineType":  machine_type,
        "country":      "au",
        "language":     "en"
    }

    try:
        response = requests.post(
            "https://pcsupport.lenovo.com/au/en/api/v4/upsell/redport/getIbaseInfo",
            json=payload,
            timeout=10
        )
        response.raise_for_status()
        device_info = response.json()
    except requests.exceptions.HTTPError as e:
        print(f"Warranty API returned an error: {e}", file=sys.stderr)
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve warranty info: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError:
        print("Warranty API returned an unexpected response (not JSON).", file=sys.stderr)
        sys.exit(1)

    print(json.dumps(device_info, indent=4))

if __name__ == "__main__":
    main()

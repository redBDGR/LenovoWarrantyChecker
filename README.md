# Lenovo Warranty Checker

A Python CLI tool to retrieve warranty and device information for Lenovo machines using the Lenovo Support API.

## How It Works

1. Accepts a Lenovo serial number as a command-line argument
2. Queries the Lenovo product lookup API to identify the machine type from the serial
3. Submits a second request to retrieve full warranty and device information
4. Outputs the result as formatted JSON

## Requirements

- Python 3.7+
- `requests` library (`requirements.txt` included)

```bash
pip install -r requirements.txt
```

## Usage

```bash
python GetLenovoWarranty.py <serial_number>
```

**Example:**

```bash
python GetLenovoWarranty.py XXXXXXXXXXXX
```

The script prints a status line to stdout before the JSON payload:

```
Requesting initial machine data from: https://pcsupport.lenovo.com/au/en/api/v4/mse/getproducts?productId=XXXXXXXXXXXX
```

The JSON response structure varies by machine and warranty type. Fields typically include device details (model, machine type, manufacture date) and one or more warranty entitlement objects.

## Error Handling

The script exits with a message if:

- No serial number is provided
- The Lenovo API is unreachable or times out
- No product is found for the given serial number
- The machine type cannot be parsed from the API response

## Region

Targets the Australian Lenovo Support API (`pcsupport.lenovo.com/au/en`). To target a different region, update the `country` and `language` values in `formatDeviceData` and adjust the base URLs accordingly.

## Disclaimer

This tool uses undocumented Lenovo Support API endpoints. It is intended for internal use only and is not affiliated with or endorsed by Lenovo. Use at your own risk — endpoints may change without notice.

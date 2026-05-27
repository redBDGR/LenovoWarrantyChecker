# Lenovo Warranty Checker

A Python CLI tool to retrieve warranty and device information for Lenovo machines using the Lenovo Support API.

## How It Works

1. Accepts a Lenovo serial number as a command-line argument
2. Queries the Lenovo product lookup API to identify the machine type
3. Submits a second request to retrieve full warranty and device information
4. Outputs the result as formatted JSON

## Requirements

- Python 3.7+
- `requests` library

Install dependencies:

```bash
pip install requests
```

## Usage

```bash
python GetLenovoWarranty.py <serial_number>
```

**Example:**

```bash
python GetLenovoWarranty.py PF60DP5X
```

**Example output:**

```json
{
    "warrantyStatus": "Active",
    "startDate": "2024-01-15",
    "endDate": "2027-01-15",
    "machineType": "21NS",
    ...
}
```

## Error Handling

The script will exit with a message if:

- No serial number is provided
- The Lenovo API is unreachable
- No product is found for the given serial number
- The machine type cannot be parsed from the API response

## Notes

- Targets the Australian Lenovo Support API (`pcsupport.lenovo.com/au/en`)
- To target a different region, update the `country` and `language` values in `formatDeviceData` and adjust the base URLs accordingly
- API endpoints are unofficial and may change without notice

## Disclaimer

This tool uses undocumented Lenovo Support API endpoints. It is intended for personal or internal use only. Use at your own risk.

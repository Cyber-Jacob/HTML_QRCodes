# HTML_QRCodes
This is a repo to create a QR code out of HTML elements. QR codes constructed this way tend most all email security filters and detection logic, and are still recognizable by end-user. Created for testing malicious payloads and detection logic of common email security providers.

## Usage

```
pip install requirements.txt
python3 qrcodegen.py "https://youtu.be/dQw4w9WgXcQ?si=3juruoFL160r7dIS" > QR_Table.html
```

## Design
This was designed to test current email security solutions, including common "AI" email security, email security gateways, and API-based post-delivery email security.

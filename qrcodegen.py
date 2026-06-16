#!/usr/bin/env python3
"""
Generate a QR code as an HTML <table> made of black/white <td> cells (no images).

Install:
  pip install qrcode[pil]

Usage:
  python qr_table.py "https://example.com" > qr-table.html
  python qr_table.py "https://example.com" --module 4 --quiet 4 --ecc M > qr-table.html
"""

import argparse
import html
import sys

import qrcode
from qrcode.constants import ERROR_CORRECT_L, ERROR_CORRECT_M, ERROR_CORRECT_Q, ERROR_CORRECT_H


ECC_MAP = {
    "L": ERROR_CORRECT_L,
    "M": ERROR_CORRECT_M,
    "Q": ERROR_CORRECT_Q,
    "H": ERROR_CORRECT_H,
}

def qr_to_html_table(
    payload: str,
    module_px: int = 4,
    quiet_zone: int = 4,
    ecc: str = "M",
    black: str = "#000000",
    white: str = "#FFFFFF",
    align: str = "center",
) -> str:
    ecc = ecc.upper()
    if ecc not in ECC_MAP:
        raise ValueError("ecc must be one of: L, M, Q, H")

    # Build QR matrix (True=black, False=white)
    qr = qrcode.QRCode(
        version=None,  # auto
        error_correction=ECC_MAP[ecc],
        box_size=1,     # we control pixels via <td> sizing
        border=0,       # we'll add quiet zone ourselves
    )
    qr.add_data(payload)
    qr.make(fit=True)
    m = qr.get_matrix()  # list[list[bool]]
    h = len(m)
    w = len(m[0])

    # Add quiet zone
    out_h = h + 2 * quiet_zone
    out_w = w + 2 * quiet_zone
    table_px_w = out_w * module_px
    table_px_h = out_h * module_px

    # Email-client friendly table attributes
    lines = []
    lines.append(
        f'<table role="presentation" border="0" cellpadding="0" cellspacing="0" '
        f'width="{table_px_w}" height="{table_px_h}" align="{align}" '
        f'style="border-collapse:collapse; border-spacing:0;">'
    )

    for y in range(-quiet_zone, h + quiet_zone):
        lines.append(f'  <tr height="{module_px}">')
        for x in range(-quiet_zone, w + quiet_zone):
            is_black = (0 <= y < h and 0 <= x < w and m[y][x])
            color = black if is_black else white
            lines.append(f'    <td width="{module_px}" height="{module_px}" bgcolor="{color}"></td>')
        lines.append("  </tr>")
    lines.append("</table>")

    # Helpful non-rendered comment for debugging
    lines.append(f"<!-- QR payload: {html.escape(payload)} -->")

    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("url", help="Any URL/string to encode into the QR code")
    ap.add_argument("--module", type=int, default=4, help="Module size in pixels (td width/height)")
    ap.add_argument("--quiet", type=int, default=4, help="Quiet zone size in modules (recommended 4)")
    ap.add_argument("--ecc", choices=["L", "M", "Q", "H"], default="M", help="Error correction level")
    ap.add_argument("--black", default="#000000", help="Black module color")
    ap.add_argument("--white", default="#FFFFFF", help="White module color")
    args = ap.parse_args()

    html_table = qr_to_html_table(
        args.url,
        module_px=args.module,
        quiet_zone=args.quiet,
        ecc=args.ecc,
        black=args.black,
        white=args.white,
    )

    sys.stdout.write(html_table)
    if not html_table.endswith("\n"):
        sys.stdout.write("\n")


if __name__ == "__main__":
    main()
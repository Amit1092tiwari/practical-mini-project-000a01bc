"""
Batch QR Code Generator
Generates QR codes in bulk from a list of URLs, strings, or a text file.
Suitable for batch job workers, asset generation pipelines, and CI/CD tests.

Usage:
    python batch_qr_generator.py --input-file urls.txt --output-dir ./generated_qrs
    python batch_qr_generator.py --items "https://github.com" "https://google.com"
"""

import argparse
import logging
from pathlib import Path
from typing import List, Optional
import qrcode
from PIL import Image

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


def generate_qr(data: str, output_path: Path, logo_path: Optional[Path] = None):
    """Generates a single QR code, optionally embedding a central logo."""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white").convert("RGB")

    if logo_path and logo_path.exists():
        logo = Image.open(str(logo_path))
        qr_width, qr_height = img.size
        logo_max_size = int(qr_width * 0.25)
        logo.thumbnail((logo_max_size, logo_max_size), Image.Resampling.LANCZOS)

        pos_x = (qr_width - logo.width) // 2
        pos_y = (qr_height - logo.height) // 2
        img.paste(logo, (pos_x, pos_y))

    img.save(str(output_path))


def run_batch(items: List[str], output_dir: Path, logo_path: Optional[Path] = None):
    """Generates QR codes in bulk for a list of items."""
    output_dir.mkdir(parents=True, exist_ok=True)
    logging.info("Starting batch QR generation for %d items...", len(items))

    for idx, item in enumerate(items, start=1):
        clean_item = item.strip()
        if not clean_item:
            continue

        filename = f"qr_{idx:04d}.png"
        out_file = output_dir / filename
        generate_qr(clean_item, out_file, logo_path=logo_path)
        logging.info("[%d/%d] Generated: %s -> %s", idx, len(items), clean_item, filename)

    logging.info("Batch completed. Output saved to %s", output_dir)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Batch QR Code Generator")
    parser.add_argument("--items", nargs="*", default=[], help="List of URLs or strings to encode")
    parser.add_argument("--input-file", type=Path, help="Text file with one item per line")
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).parent / "batch_qrs",
                        help="Target output directory")
    parser.add_argument("--logo", type=Path, default=Path(__file__).parent / "test-image.jpg",
                        help="Path to logo image to embed in center")

    args = parser.parse_args()

    items_to_process = list(args.items)
    if args.input_file and args.input_file.exists():
        with open(args.input_file, "r", encoding="utf-8") as f:
            items_to_process.extend([line.strip() for line in f if line.strip()])

    if not items_to_process:
        # Default sample batch
        items_to_process = [
            "http://bit.ly/hackersrealm",
            "https://github.com/Amit1092tiwari/Python-Projects",
            "https://python.org",
        ]

    run_batch(items_to_process, args.output_dir, args.logo if args.logo.exists() else None)

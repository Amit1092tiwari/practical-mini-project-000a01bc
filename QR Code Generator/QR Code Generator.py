"""
Python QR Code Generator
Supports modern QR generation via `qrcode` (recommended) with optional logo overlay,
and legacy generation via `MyQR`.

Installation:
    pip install qrcode[pil] Pillow
"""

from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent
URL = "http://bit.ly/hackersrealm"
BG_IMAGE = BASE_DIR / "test-image.jpg"
OUTPUT_STANDARD = BASE_DIR / "qrchannel.png"
OUTPUT_CUSTOM = BASE_DIR / "qrchannelcustomized.png"


def generate_with_qrcode():
    """Generates standard and logo-embedded QR codes using the modern `qrcode` library."""
    import qrcode
    from PIL import Image

    print(f"Generating standard QR code for: {URL}")
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(URL)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
    img.save(str(OUTPUT_STANDARD))
    print(f"Saved standard QR code to: {OUTPUT_STANDARD.name}")

    if BG_IMAGE.exists():
        print(f"Generating logo-embedded QR code with {BG_IMAGE.name}...")
        logo = Image.open(str(BG_IMAGE))

        # Resize logo to fit inside the QR code center (~25% of QR width)
        qr_width, qr_height = img.size
        logo_max_size = int(qr_width * 0.25)
        logo.thumbnail((logo_max_size, logo_max_size), Image.Resampling.LANCZOS)

        pos_x = (qr_width - logo.width) // 2
        pos_y = (qr_height - logo.height) // 2
        img.paste(logo, (pos_x, pos_y))

        img.save(str(OUTPUT_CUSTOM))
        print(f"Saved customized QR code to: {OUTPUT_CUSTOM.name}")
    else:
        print(f"Notice: '{BG_IMAGE.name}' not found; skipped customized QR code.")


def generate_with_myqr():
    """Generates artistic QR codes using the legacy `MyQR` library."""
    from MyQR import myqr

    print("Generating QR codes using MyQR...")
    myqr.run(
        words=URL,
        save_name=OUTPUT_STANDARD.name,
        save_dir=str(BASE_DIR)
    )

    if BG_IMAGE.exists():
        myqr.run(
            words=URL,
            picture=str(BG_IMAGE),
            colorized=True,
            save_name=OUTPUT_CUSTOM.name,
            save_dir=str(BASE_DIR)
        )
    print("Done generating with MyQR!")


if __name__ == '__main__':
    try:
        generate_with_qrcode()
    except ImportError:
        try:
            generate_with_myqr()
        except ImportError:
            print(
                "Error: No supported QR code library found.\n"
                "Please install dependencies with: pip install qrcode[pil] Pillow\n"
                "Or for legacy MyQR: pip install myqr"
            )
            sys.exit(1)

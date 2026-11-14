# Python QR Code Generator

**Video Tutorial:** https://youtu.be/K2TyQhf2Ycg

## Project Information

The objective of the project is to build a QR code generator using Python. It supports generating standard black-and-white QR codes as well as customized QR codes with embedded image logos.

## Installation

Install the recommended modern libraries:
```bash
pip install "qrcode[pil]" Pillow
```

*(Optional legacy support for Python < 3.10)*:
```bash
pip install myqr
```

## Usage

Run the script from anywhere:
```bash
python "QR Code Generator/QR Code Generator.py"
```

The script will output:
- `qrchannel.png`: Standard high-resolution QR code
- `qrchannelcustomized.png`: Customized QR code with embedded logo

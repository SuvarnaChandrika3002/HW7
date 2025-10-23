import argparse
import logging.config
import os
import sys
from datetime import datetime
from pathlib import Path

import qrcode 
import validators
from dotenv import load_dotenv

load_dotenv()


QR_DIRECTORY = os.getenv("QR_CODE_DIR", "qr_codes")
FILL_COLOR = os.getenv("FILL_COLOR", "red")  
BACK_COLOR = os.getenv("BACK_COLOR", "white")


def setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
        ],
    )


def create_directory(path: Path) -> None:
    try:
        path.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        logging.error(f"Failed to create directory {path}: {e}")
        sys.exit(1)


def is_valid_url(url: str) -> bool:
    if validators.url(url):
        return True
    else:
        logging.error(f"Invalid URL provided: {url}")
        return False


def generate_qr_code(
    data: str, path: Path, fill_color: str = "red", back_color: str = "white"
) -> None:
    if not is_valid_url(data):
        return 

    try:
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color=fill_color, back_color=back_color)

        with path.open("wb") as qr_file:
            img.save(qr_file)
        logging.info(f"QR code successfully saved to {path}")

    except Exception as e:
        error_msg = f"Error generating or saving QR code: {e}"
        logging.error(error_msg)


def main() -> None:

    parser = argparse.ArgumentParser(description="Generate a QR code.")
    parser.add_argument(
        "--url",
        help="The URL to encode in the QR code",
        default="https://github.com/SuvarnaChandrika3002",
    )
    args = parser.parse_args()

    setup_logging()

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    qr_filename = f"QRCode_{timestamp}.png"

    qr_code_full_path = Path.cwd() / QR_DIRECTORY / qr_filename

    create_directory(Path.cwd() / QR_DIRECTORY)

    generate_qr_code(args.url, qr_code_full_path, FILL_COLOR, BACK_COLOR)


if __name__ == "__main__":
    main()
"""
Batch Edge Detection Processor (Headless)
Performs Canny and Laplacian edge detection on directories of images in batch.
Suitable for headless pipelines, automated testing, and CI/CD/batch processing.

Usage:
    python batch_edge_processor.py --input-dir ./images --output-dir ./output
"""

import argparse
import json
import logging
from pathlib import Path
from typing import Dict, Any
import cv2

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


def process_image(img_path: Path, output_dir: Path, method: str = "both") -> Dict[str, Any]:
    """Process a single image headlessly and save edge-detected artifacts."""
    img = cv2.imread(str(img_path))
    if img is None:
        return {"file": img_path.name, "status": "failed", "error": "Unable to read image"}

    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(img_gray, (3, 3), 0)

    result = {"file": img_path.name, "status": "success", "outputs": []}

    # Canny Edge Detection
    if method in ("canny", "both"):
        canny = cv2.Canny(blurred, 100, 200)
        canny_out = output_dir / f"canny_{img_path.name}"
        cv2.imwrite(str(canny_out), canny)
        result["outputs"].append(str(canny_out.name))

    # Laplacian Edge Detection
    if method in ("laplacian", "both"):
        laplacian = cv2.Laplacian(blurred, cv2.CV_64F)
        laplacian_out = output_dir / f"laplacian_{img_path.name}"
        cv2.imwrite(str(laplacian_out), laplacian)
        result["outputs"].append(str(laplacian_out.name))

    return result


def run_batch(input_dir: Path, output_dir: Path, method: str = "both"):
    """Scans input directory and executes headless edge detection."""
    if not input_dir.exists():
        raise FileNotFoundError(f"Input directory does not exist: {input_dir}")

    output_dir.mkdir(parents=True, exist_ok=True)
    supported_exts = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
    image_files = [f for f in input_dir.iterdir() if f.is_file() and f.suffix.lower() in supported_exts]

    logging.info("Found %d images in %s", len(image_files), input_dir)
    results = []

    for img_file in image_files:
        logging.info("Processing: %s", img_file.name)
        res = process_image(img_file, output_dir, method=method)
        results.append(res)

    # Save execution manifest
    manifest_path = output_dir / "batch_report.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    successful = sum(1 for r in results if r["status"] == "success")
    logging.info("Batch complete: %d/%d images processed successfully. Report saved to %s",
                 successful, len(image_files), manifest_path.name)
    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Batch Edge Detection Processor")
    parser.add_argument("--input-dir", type=Path, default=Path(__file__).parent,
                        help="Directory containing source images")
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).parent / "batch_output",
                        help="Directory to save edge detection results")
    parser.add_argument("--method", choices=["canny", "laplacian", "both"], default="both",
                        help="Edge detection algorithm to apply")

    args = parser.parse_args()
    run_batch(args.input_dir, args.output_dir, args.method)

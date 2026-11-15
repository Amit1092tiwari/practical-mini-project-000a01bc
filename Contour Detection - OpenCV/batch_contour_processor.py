"""
Batch Contour Detection Processor (Headless)
Performs thresholding and contour extraction on directories of images in batch.
Extracts metrics (contour count, areas, bounding boxes) and saves annotated outputs.

Usage:
    python batch_contour_processor.py --input-dir ./images --output-dir ./output
"""

import argparse
import json
import logging
from pathlib import Path
from typing import Dict, Any
import cv2

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


def process_image(img_path: Path, output_dir: Path, threshold: int = 50) -> Dict[str, Any]:
    """Process a single image headlessly and save contour-annotated artifacts."""
    img = cv2.imread(str(img_path))
    if img is None:
        return {"file": img_path.name, "status": "failed", "error": "Unable to read image"}

    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(img_gray, threshold, 255, cv2.THRESH_BINARY)

    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    # Draw contours on a copy
    annotated = img.copy()
    cv2.drawContours(annotated, contours, -1, (0, 255, 0), 2, lineType=cv2.LINE_AA)

    out_file = output_dir / f"contours_{img_path.name}"
    cv2.imwrite(str(out_file), annotated)

    # Compute basic contour statistics
    areas = [cv2.contourArea(c) for c in contours]
    total_area = sum(areas)
    max_area = max(areas) if areas else 0.0

    return {
        "file": img_path.name,
        "status": "success",
        "output_image": out_file.name,
        "total_contours": len(contours),
        "total_contour_area": round(total_area, 2),
        "max_contour_area": round(max_area, 2),
    }


def run_batch(input_dir: Path, output_dir: Path, threshold: int = 50):
    """Scans input directory and executes headless contour detection."""
    if not input_dir.exists():
        raise FileNotFoundError(f"Input directory does not exist: {input_dir}")

    output_dir.mkdir(parents=True, exist_ok=True)
    supported_exts = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
    image_files = [f for f in input_dir.iterdir() if f.is_file() and f.suffix.lower() in supported_exts]

    logging.info("Found %d images in %s", len(image_files), input_dir)
    results = []

    for img_file in image_files:
        logging.info("Detecting contours in: %s", img_file.name)
        res = process_image(img_file, output_dir, threshold=threshold)
        results.append(res)

    manifest_path = output_dir / "batch_report.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    successful = sum(1 for r in results if r["status"] == "success")
    logging.info("Batch complete: %d/%d images processed successfully. Report saved to %s",
                 successful, len(image_files), manifest_path.name)
    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Batch Contour Detection Processor")
    parser.add_argument("--input-dir", type=Path, default=Path(__file__).parent,
                        help="Directory containing source images")
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).parent / "batch_output",
                        help="Directory to save contour detection results")
    parser.add_argument("--threshold", type=int, default=50,
                        help="Binary threshold value (0-255)")

    args = parser.parse_args()
    run_batch(args.input_dir, args.output_dir, args.threshold)

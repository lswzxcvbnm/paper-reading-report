#!/usr/bin/env python3
"""Render a local PDF page, crop in displayed coordinates, and retain provenance.

Requires Pillow and Poppler's pdftoppm. Page numbers are one-based PDF indices.
"""

import argparse
import json
import math
from pathlib import Path
import shutil
import subprocess
import tempfile


def parse_box(value):
    try:
        coordinates = tuple(float(part.strip()) for part in value.split(","))
    except ValueError as exc:
        raise argparse.ArgumentTypeError("box must contain four numbers") from exc
    if len(coordinates) != 4 or not all(math.isfinite(v) for v in coordinates):
        raise argparse.ArgumentTypeError("box must contain four finite numbers")
    left, top, right, bottom = coordinates
    if not (0 <= left < right <= 1 and 0 <= top < bottom <= 1):
        raise argparse.ArgumentTypeError("require 0 <= left < right <= 1 and 0 <= top < bottom <= 1")
    return coordinates


def positive_integer(value):
    try:
        number = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("must be an integer") from exc
    if number < 1:
        raise argparse.ArgumentTypeError("must be at least 1")
    return number


def capture(args):
    from PIL import Image

    source = Path(args.pdf).expanduser().resolve()
    output = Path(args.out).expanduser().resolve()
    manifest = output.with_suffix(output.suffix + ".json")
    if not source.is_file():
        raise ValueError(f"PDF not found: {source}")
    if source == output or source == manifest:
        raise ValueError("output must not replace the source PDF")
    if output.suffix.lower() != ".png":
        raise ValueError("output must have a .png suffix")
    for destination in (output, manifest):
        if destination.exists() and (not args.overwrite or not destination.is_file()):
            raise ValueError(f"output exists; choose another name or use --overwrite: {destination}")

    renderer = shutil.which(args.pdftoppm)
    if renderer is None:
        raise ValueError("pdftoppm was not found; install Poppler or pass --pdftoppm PATH")

    with tempfile.TemporaryDirectory(prefix="paper-capture-") as temporary:
        prefix = Path(temporary) / "page"
        command = [
            renderer, "-f", str(args.page), "-l", str(args.page),
            "-singlefile", "-r", str(args.dpi), "-png", str(source), str(prefix),
        ]
        process = subprocess.run(command, capture_output=True, timeout=120, check=False)
        page_image = prefix.with_suffix(".png")
        if process.returncode != 0 or not page_image.is_file():
            details = process.stderr.decode("utf-8", errors="replace").strip()
            raise ValueError(f"PDF render failed (page {args.page}): {details[:2000]}")

        with Image.open(page_image) as page:
            width, height = page.size
            left, top, right, bottom = args.box
            pixel_box = (
                math.floor(left * width), math.floor(top * height),
                math.ceil(right * width), math.ceil(bottom * height),
            )
            cropped = page.crop(pixel_box)
            metadata = {
                "source_pdf": str(source),
                "pdf_page_index_1based": args.page,
                "label_user_supplied": args.label,
                "renderer": "pdftoppm",
                "dpi": args.dpi,
                "coordinate_system": "normalized displayed page, origin at top-left",
                "normalized_box_ltrb": list(args.box),
                "page_image_pixels_wh": [width, height],
                "pixel_box_ltrb": list(pixel_box),
                "capture_pixels_wh": list(cropped.size),
                "image_filename": output.name,
            }
            temporary_image = Path(temporary) / "capture.png"
            cropped.save(temporary_image, format="PNG", dpi=(args.dpi, args.dpi))
            cropped.close()

        temporary_manifest = Path(temporary) / "capture.png.json"
        temporary_manifest.write_text(
            json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        output.parent.mkdir(parents=True, exist_ok=True)
        # Copy only after rendering and metadata generation have succeeded.
        # Exclusive creation avoids accidental replacement in normal operation.
        image_created = False
        try:
            mode = "wb" if args.overwrite else "xb"
            with output.open(mode) as stream, temporary_image.open("rb") as source_stream:
                image_created = True
                shutil.copyfileobj(source_stream, stream)
            with manifest.open(mode) as stream, temporary_manifest.open("rb") as source_stream:
                shutil.copyfileobj(source_stream, stream)
        except OSError:
            if image_created and not args.overwrite:
                output.unlink(missing_ok=True)
            raise

    return {"image": str(output), "metadata": str(manifest), **metadata}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pdf", required=True, help="local source PDF path")
    parser.add_argument("--page", type=positive_integer, required=True, help="1-based PDF page index")
    parser.add_argument("--out", required=True, help="destination PNG path")
    parser.add_argument("--box", type=parse_box, default=(0.0, 0.0, 1.0, 1.0),
                        help="left,top,right,bottom in displayed page coordinates, each in [0,1]")
    parser.add_argument("--dpi", type=positive_integer, default=240)
    parser.add_argument("--label", default="", help="manually verified figure/table/equation label")
    parser.add_argument("--pdftoppm", default="pdftoppm", help="renderer name or executable path")
    parser.add_argument("--overwrite", action="store_true", help="replace existing PNG and metadata")
    args = parser.parse_args()
    if not 36 <= args.dpi <= 600:
        parser.error("dpi must be between 36 and 600")
    try:
        result = capture(args)
    except ImportError:
        parser.exit(1, "Pillow is required; install it in the selected conda environment.\n")
    except (OSError, ValueError, subprocess.TimeoutExpired) as exc:
        parser.exit(1, f"Capture failed: {exc}\n")
    print(json.dumps(result, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    main()

from pathlib import Path
import argparse
import sys

from renderer import render_to_png

#!/usr/bin/env python3
"""
CLI for htmlsnap.rendering
Modify HELP_TEXT below to change the help message shown in --help.
"""


HELP_TEXT = """Render an HTML file to an image.

Positional arguments:
    html_path            Path to the HTML file to be rendered.

Optional arguments:
    -s, --size           Image size as WIDTHxHEIGHT (e.g. 1024x768). Default: 800x600
    -S, --selector       CSS selector string to target a specific element (optional).

Examples:
    python -m htmlsnap /path/to/file.html
    python -m htmlsnap /path/to/file.html -s 1280x720 -S "#main > .article"

Modify this string to change the help/usage shown to users.
"""


def existing_file(path_str: str) -> Path:
    p = Path(path_str)
    if not p.replace(" ", ""):
        print("Error: Path cannot be empty or just whitespace.")
        raise argparse.ArgumentTypeError(f"Invalid path: {path_str}")
    if not p.exists():
        print(f"File not found: {path_str}")
        raise argparse.ArgumentTypeError(f"File not found: {path_str}")
    if not p.is_file():
        raise argparse.ArgumentTypeError(f"Path is not a file: {path_str}")
    return p


def parse_size(size_str: str):
    """Parse WIDTHxHEIGHT into a (width, height) tuple of ints."""
    if isinstance(size_str, (tuple, list)) and len(size_str) == 2:
            return tuple(map(int, size_str))
    try:
        sep = 'x' if 'x' in size_str else ('X' if 'X' in size_str else None)
        if sep is None:
            raise ValueError
        w_str, h_str = size_str.split(sep, 1)
        w, h = int(w_str), int(h_str)
        if w <= 0 or h <= 0:
            raise ValueError
        return (w, h)
    except Exception:
        raise argparse.ArgumentTypeError(
            "Size must be in WIDTHxHEIGHT format, e.g. 800x600"
        )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Render HTML to image",
        epilog=HELP_TEXT,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "html_path",
        # type=existing_file,
        help="Path to the HTML file to render.",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default="output.png",
        help="Output image file path (default: output.png).",
        metavar="OUTPUT",
    )
    parser.add_argument(
        "-s",
        "--size",
        type=parse_size,
        default=(800, 600),
        help="Image size as WIDTHxHEIGHT (default: 800x600).",
        metavar="WIDTHxHEIGHT",
    )
    parser.add_argument(
        "-S",
        "--selector",
        type=str,
        default=None,
        help="CSS selector to target a specific element (optional).",
        metavar="SELECTOR",
    )
    parser.add_argument(
        "-w",
        "--overwrite",
        action="store_true",
        help="Overwrite output file if it already exists without prompting.",
    )
    return parser


def render_html_to_image(html_path: Path, output_path: Path, width: int, height: int, selector: str | None, overwrite: bool = False):

    # Example placeholder behavior: print what would be done.
    print(f"Rendering: {html_path!s}")
    print(f"Size: {width}x{height}")
    print(f"Selector: {selector!r}")

    render_to_png(
        html_path, 
        output_path, width, height, selector=selector, overwrite=overwrite)
    


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    render_html_to_image(args.html_path, args.output, args.size[0], args.size[1], args.selector, overwrite=args.overwrite)
    return 0


if __name__ == "__main__":
    main()
import pytest
from pathlib import Path
from unittest.mock import patch

from htmlsnap.cli import parse_size, build_parser, main


def test_parse_size_valid():
    assert parse_size("800x600") == (800, 600)
    assert parse_size("1920X1080") == (1920, 1080)


def test_parse_size_tuple_passthrough():
    assert parse_size((1024, 768)) == (1024, 768)


@pytest.mark.parametrize("bad", [
    "800",
    "x600",
    "800x",
    "abcx600",
    "800xabc",
    "-1x600",
    "800x0",
])
def test_parse_size_invalid(bad):
    with pytest.raises(Exception):
        parse_size(bad)


def test_parser_defaults():
    parser = build_parser()
    args = parser.parse_args(["foo.html"])

    assert args.html_path == "foo.html"
    assert args.output == "output.png"
    assert args.size == (800, 600)
    assert args.selector is None
    assert args.overwrite is False


# @patch("htmlsnap.cli.render_html_to_image")
# def test_main_calls_renderer(mock_render):
#     main([
#         "test.html",
#         "-o", "out.png",
#         "-s", "1024x768",
#         "-S", "#main",
#         "-w"
#     ])

#     mock_render.assert_called_once_with(
#         "test.html",
#         "out.png",
#         1024,
#         768,
#         "#main",
#         overwrite=True
#     )
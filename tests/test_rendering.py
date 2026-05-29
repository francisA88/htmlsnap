import pytest
from pathlib import Path
from unittest.mock import patch, mock_open

from htmlsnap.renderer import render_to_png


ASSETS = Path(__file__).parent / "assets"
SNAPSHOTS = Path(__file__).parent / "snapshots"


@pytest.fixture
def sample_html():
    return ASSETS / "sample.html"


@pytest.fixture
def output_png():
    return SNAPSHOTS / "sample.png"


@patch("htmlsnap.renderer.destroy")
@patch("htmlsnap.renderer.lib")
def test_render_full_page(mock_lib, mock_destroy, sample_html, output_png):
    mock_lib.renderToPNG.return_value = True

    result = render_to_png(
        sample_html,
        output_png,
        overwrite=True
    )

    assert result is True
    mock_lib.initializeRenderer.assert_called_once()
    mock_lib.loadHTML.assert_called_once()
    mock_lib.renderToPNG.assert_called_once()
    mock_destroy.assert_called_once()


@patch("htmlsnap.renderer.destroy")
@patch("htmlsnap.renderer.lib")
def test_render_selector(mock_lib, mock_destroy, sample_html, output_png):
    mock_lib.renderCroppedToImage.return_value = True

    result = render_to_png(
        sample_html,
        output_png,
        selector="#main",
        overwrite=True
    )

    assert result is True
    mock_lib.renderCroppedToImage.assert_called_once()


@patch("htmlsnap.renderer.lib")
def test_missing_source_returns_none(mock_lib):
    result = render_to_png(
        "does_not_exist.html",
        "out.png",
        overwrite=True
    )

    assert result is None
    mock_lib.loadHTML.assert_not_called()


@patch("builtins.input", return_value="n")
@patch("htmlsnap.renderer.lib")
def test_overwrite_cancel(mock_lib, mock_input, tmp_path):
    src = tmp_path / "test.html"
    src.write_text("<html></html>")

    out = tmp_path / "out.png"
    out.write_text("existing")

    result = render_to_png(src, out)

    assert result is None
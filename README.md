# htmlsnap

**Fast, native HTML-to-image rendering for Python.**

Render full HTML documents or specific DOM elements into PNG images using a lightweight native rendering engine powered by **Ultralight**.

`htmlsnap` is built for developers who need **deterministic, scriptable, production-grade rendering** without spinning up a full browser automation stack.

---

## Why htmlsnap?

Most "HTML to image" tools are either:

* **Heavyweight**
  (launch Chromium, Playwright, Puppeteer...)

* **Slow**
  (cold starts, browser process overhead)

* **Overkill**
  for static rendering pipelines

`htmlsnap` uses a native rendering backend for **fast, direct rendering**.

This makes it ideal for:

### Automated visual asset generation

Generate:

* social preview cards
* Open Graph images
* share banners
* article thumbnails
* dashboard previews

---

### Component snapshot pipelines

Render specific elements using CSS selectors.

Perfect for:

* design system previews
* UI component snapshots
* style guide generation
* automated visual exports

---

### Static rendering workflows

Use HTML/CSS as a declarative graphics format.

Generate:

* certificates
* reports
* badges
* invoices
* templated graphics
* dynamic marketing assets

---

### Visual regression testing

Render and compare snapshots across builds.

Useful for:

* frontend testing
* rendering consistency checks
* CI visual diffing

---

## Features

* Native high-performance rendering
* Render full pages to PNG
* Render specific DOM elements using CSS selectors
* Adjustable output resolution
* Cross-platform prebuilt binaries
* Python API
* Command-line interface
* No browser automation dependency
* Scriptable and CI-friendly

---

## Installation

Currently, installation is supported **directly from GitHub releases**.

Prebuilt archives are distributed separately for:

* **Linux**
* **Windows**

Each archive contains:

* Python package source
* Prebuilt platform-native renderer library
* Bundled platform-specific Ultralight binaries

---

### Linux

```bash
pip install git+https://github.com/<username>/htmlsnap.git
```

---

### Windows

```powershell
pip install git+https://github.com/<username>/htmlsnap.git
```

---

## Requirements

* Python 3.10+
* 64-bit operating system

Supported platforms:

| Platform       | Status    |
| -------------- | --------- |
| Linux x86_64   | Supported |
| Windows x86_64 | Supported |

---

## Quick Start

### Render a full HTML document

```python
from htmlsnap.renderer import render_to_png

render_to_png(
    "page.html",
    "output.png"
)
```

---

### Render at custom resolution

```python
render_to_png(
    "page.html",
    "large.png",
    width=1920,
    height=1080
)
```

---

### Render a specific DOM element

```python
render_to_png(
    "page.html",
    "card.png",
    selector="#main-card"
)
```

---

## Command Line Usage

### Basic rendering

```bash
python -m htmlsnap page.html
```

---

### Custom output

```bash
python -m htmlsnap page.html -o result.png
```

---

### Custom size

```bash
python -m htmlsnap page.html -s 1920x1080
```

---

### Render specific element

```bash
python -m htmlsnap page.html -S "#hero"
```

---

### Overwrite existing files

```bash
python -m htmlsnap page.html -o out.png -w
```

---

## CLI Options

| Option              | Description                        |
| ------------------- | ---------------------------------- |
| `-o`, `--output`    | Output PNG file                    |
| `-s`, `--size`      | Output resolution (`WIDTHxHEIGHT`) |
| `-S`, `--selector`  | CSS selector for element rendering |
| `-w`, `--overwrite` | Overwrite existing output          |

---

## Python API

### `render_to_png`

```python
render_to_png(
    source_file,
    dest_file,
    width=800,
    height=600,
    selector=None,
    overwrite=False
)
```

### Parameters

#### `source_file`

Path to source HTML file.

#### `dest_file`

Output PNG path.

#### `width`

Viewport width.

#### `height`

Viewport height.

#### `selector`

Optional CSS selector for rendering a specific element.

#### `overwrite`

Whether to overwrite existing output.

---

## Project Structure

```text
htmlsnap/
├── resources/
├── libs/
├── __main__.py
├── __init__.py
├── cli.py
├── renderer.py
├── lib.py
```

### `renderer.py`

High-level rendering interface.

Responsibilities:

* renderer lifecycle
* HTML loading
* image generation
* selector-based rendering

---

### `cli.py`

Command-line interface.

Responsibilities:

* argument parsing
* input validation
* CLI execution flow

---

### `lib.py`

Native library loader.

Responsibilities:

* load platform-specific shared library
* declare native symbols
* expose C bindings

---

## Example Use Cases

---

### Generate Open Graph cards

```bash
python -m htmlsnap og_template.html -o article-preview.png
```

---

### Export UI cards

```bash
python -m htmlsnap dashboard.html -S ".summary-card"
```

---

### Render reports

```python
for report in reports:
    render_to_png(report.html, report.output)
```

---

## Testing

Run tests using:

```bash
pytest tests/
```

Test assets:

```text
tests/assets/
```

Generated snapshots:

```text
tests/snapshots/
```

---

## Performance Philosophy

`htmlsnap` exists because rendering HTML should not require launching a full browser stack for every image.

It prioritizes:

* lower overhead
* faster startup
* deterministic rendering
* automation-friendly workflows

---

## License Notes

This project depends on **Ultralight**.

Ultralight licensing terms may impose restrictions on certain commercial usage scenarios.

Users are responsible for ensuring compliance with Ultralight's licensing requirements.

See Ultralight licensing documentation for details.

---

## Roadmap

Planned improvements:

* macOS binaries
* batch rendering
* direct HTML string rendering
* PDF export
* transparent background support
* async rendering API
* richer viewport controls

---

## Contributing

Contributions are welcome.

Areas of interest:

* platform packaging
* rendering improvements
* test coverage
* documentation
* performance optimization

---

## Vision

HTML is one of the most expressive layout languages ever created.

`htmlsnap` turns it into a programmable image generation engine.

Use web technologies as a graphics DSL.

Render anything.

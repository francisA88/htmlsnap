import pathlib

from .lib import lib

def destroy():
    lib.destroySurface()
    lib.destroyRenderer()

def render_to_png(source_file, dest_file, width=800, height=600, selector=None, overwrite=False):
    lib.initializeRenderer(width, height)
    if pathlib.Path(dest_file).exists():
        print(f"Warning: {dest_file} already exists and will be overwritten.")
        if not overwrite:
            test = input("Do you want to continue? (y/n): ")
            if test.lower() != 'y':
                print("Operation cancelled.")
                return
    
    if not pathlib.Path(source_file).exists():
        print(f"Error: Source file {source_file} does not exist.")
        return

    lib.loadHTML(open(source_file, 'r').read().encode('utf-8'))
    lib.updateRenderer()
    if selector:
        ok = lib.renderCroppedToImage(selector.encode('utf-8'), dest_file.encode('utf-8'))
        if ok:
            print(f"Rendered element '{selector}' from {source_file} to {dest_file}")
    else:
        ok = lib.renderToPNG(dest_file.encode('utf-8'))
        if ok:
            print(f"Rendered {source_file} to {dest_file}")

    if not ok:
        print(f"Failed to render {source_file} to {dest_file}")

    destroy()
    return ok



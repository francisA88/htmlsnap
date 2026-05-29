from setuptools import setup
from setuptools.command.build_py import build_py
import subprocess
import shutil
from pathlib import Path


ROOT = Path(__file__).parent
SRC_BIN = ROOT / "src/cpp/ultralight/bin"
DST_BIN = ROOT / "src/htmlsnap/libs/ultralight/bin"


class BuildWithNative(build_py):
    def run(self):
        print("Compiling native renderer...")
        subprocess.check_call(["bash", "compile_ext.sh"])

        print("Copying Ultralight runtime...")
        if DST_BIN.exists():
            shutil.rmtree(DST_BIN)

        shutil.copytree(SRC_BIN, DST_BIN)

        super().run()


setup(
    cmdclass={"build_py": BuildWithNative},
)
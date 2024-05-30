# Copyright (C) 2023, NG:ITL
import versioneer
from pathlib import Path
from setuptools import find_packages, setup


def read(fname):
    return open(Path(__file__).parent / fname).read()


setup(
    name="raai_module_control_panel",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    author="NGITL",
    author_email="calvinteuber7@gmail.com",
    description=("Control panel module containing the control UI of RaceAgainstAI"),
    license="GPL 3.0",
    keywords="module",
    url="https://github.com/vw-wob-it-edu-ngitl/raai_module_control_panel",
    packages=find_packages(),
    long_description=read("README.md"),
    install_requires=["pyside6==6.3.1", "inkscape_svg_layer_extractor~=0.0.2", "pynng~=0.7.2"],
)

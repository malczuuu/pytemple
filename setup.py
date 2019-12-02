from setuptools import setup
import os
import sys

_here = os.path.abspath(os.path.dirname(__file__))

if sys.version_info[0] < 3:
    with open(os.path.join(_here, "README.md")) as f:
        long_description = f.read()
else:
    with open(os.path.join(_here, "README.md"), encoding="utf-8") as f:
        long_description = f.read()

version = {}
with open(os.path.join(_here, "pytemple", "version.py")) as f:
    exec(f.read(), version)

setup(
    name="pytemple",
    version=version["__version__"],
    description="Replacing value placeholders in template files",
    long_description=long_description,
    author="Damian Malczewski",
    author_email="damian.m.malczewski@gmail.com",
    url="https://github.com/malczuuu/pytemple",
    license="MIT",
    packages=["pytemple"],
    install_requires=[],
    scripts=[],
    include_package_data=True,
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3.6"],
    )

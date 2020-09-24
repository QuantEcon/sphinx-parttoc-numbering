from setuptools import setup, find_packages
from pathlib import Path

lines = Path("sphinx_parttoc_numbering").joinpath("__init__.py")
for line in lines.read_text().split("\n"):
    if line.startswith("__version__ ="):
        version = line.split(" = ")[-1].strip('"')
        break

setup(
    name="sphinx-parttoc-numbering",
    version=version,
    description="Supporting part in HTML section numbering",
    packages=find_packages("sphinx_parttoc_numbering"),
    license="MIT",
    install_requires=["sphinx"],
    extras_require={
        "code_style": ["flake8<3.8.0,>=3.7.0", "black", "pre-commit==1.17.0"],
        "testing": [
            "pytest~=5.4",
            "pytest-cov~=2.8",
            "coverage<5.0",
            "pytest-regressions",
            "jupyter-book",
        ],
    },
)

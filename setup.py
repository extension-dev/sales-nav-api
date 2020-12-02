import setuptools
import ast
import re
from pathlib import Path

CURRENT_DIR = Path(__file__).parent


def get_version() -> str:
    black_py = CURRENT_DIR / "sales_nav_api/__init__.py"
    _version_re = re.compile(r"__version__\s+=\s+(?P<version>.*)")
    with open(black_py, "r", encoding="utf8") as f:
        match = _version_re.search(f.read())
        version = match.group("version") if match is not None else '"unknown"'
    return str(ast.literal_eval(version))


setuptools.setup(
    name="sales_nav_api",
    version=get_version(),
    author="include.ai boys",
    author_email="founders@include.ai",
    description="Python wrapper for the Linkedin Sales Navigator API",
    long_description="Python wrapper for the Linkedin Sales Navigator API",
    long_description_content_type="text/markdown",
    url="https://github.com/includeai/sales-nav-api/tree/master/sales_nav_api",
    license="MIT",
    packages=setuptools.find_packages(),
    install_requires=["requests", "beautifulsoup4", "lxml"],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)

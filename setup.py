import setuptools
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()


setuptools.setup(
    name="itsmostdef",
    version="0.1.0",
    description="Whats in my fastq file?",
    author="William Rosenbaum",
    author_email="william.rosenbaum@gmail.com",
    license="MIT",
    packages=setuptools.find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.10",
    install_requires=[
        "pandas",
        "pyfastx",
    ],
    entry_points={"console_scripts": ["itsmostdef...=itsmostdef.main:main"]},
)

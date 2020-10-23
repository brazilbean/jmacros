import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jmacros",
    version="0.0.1",
    author="Gordon Bean",
    author_email="brazilbean@gmail.com",
    description="Recursively evaluates customizable macros in JSON objects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/brazilbean/jmacros",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
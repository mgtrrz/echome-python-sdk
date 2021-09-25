import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="echome-sdk",
    version="0.3.0",
    author="Marcus Gutierrez",
    author_email="markg90@gmail.com",
    description="EcHome python library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mgtrrz/echome-python-sdk",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'requests>=2.26'
    ]
)

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="webull",
    version="0.1.0",
    author="ted chou",
    description="The unofficial python interface for the WeBull API",
    license='MIT',
    author_email="ted.chou12@gmail.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tedchou12/webull.git",
    packages=setuptools.find_packages(),
    install_requires=[
        "certifi>=2020.4.5.1",
        "chardet>=3.0.4",
        "idna>=2.9",
        "numpy>=1.18.4",
        "pandas>=0.25.3",
        "python-dateutil>=2.8.1",
        "pytz>=2020.1",
        "requests>=2.23.0",
        "six>=1.14.0",
        "urllib3>=1.25.9",
        "email-validator>=1.1.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

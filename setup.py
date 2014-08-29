import sys
from setuptools import setup, find_packages

setup(
    name="namestand",
    version="0.0.0",
    description="Standardize any lists of strings, but especially database/CSV column-names.",
    long_description="",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3"
    ],
    keywords="rename columns standardize standardizing names",
    author="Jeremy Singer-Vine",
    author_email="jeremy.singer-vine@buzzfeed.com",
    url="http://github.com/buzzfeednews/namestand/",
    license="MIT",
    packages=find_packages(exclude=["test",]),
    namespace_packages=[],
    include_package_data=False,
    zip_safe=False,
    tests_require=[
        "nose",
    ],
    test_suite="test",
)

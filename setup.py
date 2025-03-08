from setuptools import setup, find_packages

setup(
    name="rsu-taxer",
    version="1.0.0",
    description="RSU calculator",
    author="wenlian",
    author_email="breakds@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "analyzer=pnl_analyzer.analyzer:main",
        ]
    },
    python_requires=">=3.11",
)

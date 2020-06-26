from setuptools import find_packages, setup

setup(
    name='replayd',
    version='0.0.1',
    description='replayd',
    url='',
    package_dir={"": "src"},
    packages=find_packages(
        where="src",
        exclude=["contrib", "docs", "tests*", "__pycache__"],
    ),
    entry_points={
        "console_scripts": [
            "replayd=replayd.cli:main",
        ],
    },
    install_requires=[
        'faker',
        'xmltodict',
        'kafka-python',
        'cerberus',
        'xeger',
    ],
)

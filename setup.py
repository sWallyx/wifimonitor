from setuptools import setup

setup(
    name='wifimonitor',
    packages=['wifimonitor'],
    version='1',
    description='A tshark wrapper to analyze devices around ou',
    author='sWallyx',
    keywords=['tshark', 'wifi', 'location', 'count', 'people'],
    classifiers=[],
    install_requires=[
        "click",
        "netifaces",
        "pick",
    ],
    setup_requires=[],
    tests_require=[],
)
from setuptools import setup

setup(
    name='myst2canvas',
    author="Mara Cielanga Colclough",
    version="0.1",
    packages=["myst2canvas"],
    package_dir={'myst2canvas': 'myst2canvas'},
    entry_points={
        'console_scripts': [
            'myst2canvas = myst2canvas.command:myst2canvas',
        ]
    },
)

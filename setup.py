from setuptools import setup

setup(
    name='md2canvas',
    author="Mara Cielanga Colclough",
    version="0.1",
    packages=["md2canvas"],
    package_dir={'md2canvas': 'md2canvas'},
    entry_points={
        'console_scripts': [
            'md2canvas = md2canvas.command:md2canvas',
            'anstrip = md2canvas.command:strip_answers',
        ]
    },
)

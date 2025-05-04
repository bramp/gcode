from setuptools import setup, find_packages

setup(
    name='gcode-parser',
    version='0.1.0',
    author='Andrew Brampton',
    author_email='github@bramp.net',
    description='G-code parser with features to make extracting slicer specific comments/settings easy',
    packages=find_packages(where='gcode'),
    package_dir={'': 'gcode'},
    install_requires=[
        # Add any dependencies required for your project here
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: BSD 3-Clause License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
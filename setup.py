from setuptools import setup, find_packages

setup(
    name='gcode-parser',
    version='0.1.0',
    author='Your Name',
    author_email='your.email@example.com',
    description='A Python package for parsing G-code files',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        # Add any dependencies required for your project here
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
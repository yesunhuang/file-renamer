from setuptools import setup, find_packages

setup(
    name='file-renamer',
    version='0.1.0',
    author='Your Name',
    author_email='your.email@example.com',
    description='A tool for renaming files and folders with user-defined prefixes and extracting labels from names.',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        # List your project dependencies here
    ],
    entry_points={
        'console_scripts': [
            'file-renamer=main:main',  # Adjust this according to your main function location
        ],
    },
)
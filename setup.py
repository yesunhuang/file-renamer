from setuptools import setup, find_packages

setup(
    name='file-renamer',
    version='1.3.1',
    author='Yesun Huang',
    author_email='yesunhuang@uchicago.edu',
    description='A tool for renaming files and folders with user-defined prefixes and extracting labels from names.',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'Flask>=2.0.1',
        'requests>=2.25.1',
        'click>=8.0.1',
        'PyQt5>=5.15.6',
        'pillow>=10.0.0',
        'google-generativeai>=0.3.0',
        'openai>=1.0.0',
    ],
    entry_points={
        'console_scripts': [
            'file-renamer=main:main',  # Adjust this according to your main function location
        ],
    },
)
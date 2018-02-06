"""
Install script used to install the code.
"""

def main():
    """Install the stockings package."""
    # Recommended install method (in a virtual environment): $ python setup.py develop
    try:
        from setuptools import setup
    except ImportError:
        from distutils.core import setup

    config = {
        'description': 'Play around with stock data',
        'author': 'Matt Christie, Ethan Nelson, and Aaron Letterly',
        'download_url': '',
        'author_email': 'christiemj09@gmail.com',
        'version': '0.1',
        'install_requires': [],  # Can list dependencies here, or just rely on requirements file
        'packages': ['stockings'],
        'scripts': [],  # Can add scripts to the package
        'entry_points': {
            'console_scripts': []  # Can turn functions in your code into scripts
        },
        'name': 'stockings'
    }

    setup(**config)    

if __name__ == '__main__':
    main()

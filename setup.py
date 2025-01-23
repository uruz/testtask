from setuptools import setup, find_packages

setup(
    name='wallet-api',
    author='AB',
    author_email='alex@boriskin.me',
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'web = wallet_api.manage:main',
        ],
    },
)

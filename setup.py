from setuptools import setup, find_packages
import anastasia

setup(
    name='anastasia',
    version="0.1.0",
    packages=find_packages(),
    author="Anastadev",
    author_email="lpw.wisniewski@gmail.com",
    description="Telegram bot, student oriented.",
    long_description=open('README.md').read(),
    include_package_data=True,
    url='https://github.com/Anastadev/anastasia/',
    install_requires=[
        "python-telegram-bot",
        "icalendar",
        "beautifulsoup4",
        "requests",
        "pymongo"
    ],
    classifiers=[
        "Programming Language :: Python",
        "Natural Language :: French",
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        "Programming Language :: Python :: 3.6",
        "Topic :: Utilities"
    ],
    entry_points={
        'console_scripts': [
            'anastasia = anastasia.main:main',
        ],
    },
)
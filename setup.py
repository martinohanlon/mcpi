from setuptools import setup

__project__ = 'mcpi'
__desc__ = 'Python library for the Minecraft Pi edition and RaspberryJuice API'
__version__ = '1.1.0'
__author__ = "Martin O'Hanlon"
__author_email__ = 'martin@ohanlonweb.com'
__license__ = 'MIT'
__url__ = 'https://github.com/martinohanlon/mcpi'

__classifiers__ = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Education",
    "Intended Audience :: Developers",
    "Topic :: Education",
    "Topic :: Games/Entertainment",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.3",
    "Programming Language :: Python :: 3.4",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
]

setup(name=__project__,
      version = __version__,
      description = __desc__,
      url = __url__,
      author = __author__,
      author_email = __author_email__,
      license = __license__,
      packages = [__project__],
      classifiers = __classifiers__,
      zip_safe=False)
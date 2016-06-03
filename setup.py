from setuptools import setup
setup(
  name = 'schiene',
  packages = ['schiene'],
  version = '0.17',
  license = 'MIT',
  description = 'schiene is a Python library for interacting with Bahn.de',
  author = 'Kevin Kennell',
  author_email = 'kevin@kennell.de',
  install_requires=[
        'requests>=2.10.0',
        'beautifulsoup4>=4.4.1'
  ],
  url = 'https://github.com/kennell/schiene',
  keywords = ['bahn', 'api'],
  classifiers = [],
)

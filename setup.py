from distutils.core import setup
setup(
  name = 'schiene',
  packages = ['schiene'],
  version = '0.15',
  license = 'MIT',
  description = 'schiene is a Python library for interacting with Bahn.de',
  author = 'Kevin Kennell',
  author_email = 'kevin@fileperms.org',
  install_requires=[
        'requests>=2.7.0',
        'beautifulsoup4>=4.4.0'
  ],
  url = 'https://github.com/kennell/schiene',
  keywords = ['bahn', 'api'],
  classifiers = [],
)

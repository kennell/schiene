from distutils.core import setup
setup(
  name = 'schiene',
  packages = ['schiene'],
  version = '0.13',
  license = 'MIT',
  description = 'schiene is a Python library for interacting with Bahn.de',
  author = 'Kevin Kennell',
  author_email = 'kevin@fileperms.org',
  install_requires=[
        'requests>=2.7.0',
        'beautifulsoup4>=4.4.0'
  ],
  url = 'https://github.com/kennell/schiene',
  download_url = 'https://github.com/kennell/schiene/tarball/0.13',
  keywords = ['bahn', 'api'],
  classifiers = [],
)

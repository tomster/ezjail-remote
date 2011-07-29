from setuptools import setup, find_packages

version = '0.1'

setup(name='ezjailremote',
      version=version,
      description="",
      long_description = (
          open('README.rst').read()
          + '\n' +
          'Change history\n'
          '**************\n'
          + '\n' +
          open('HISTORY.rst').read()
          + '\n' +
          'Download\n'
          '********\n'),
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='ezjail, FreeBSD, fabric',
      author='Tom Lazar',
      author_email='tom@tomster.org',
      url='https://github.com/tomster/ezjail-remote',
      license='BSD',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        "Fabric",
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
        [console_scripts]
        ezjail-remote=ezjailremote:commandline
      """,
      )

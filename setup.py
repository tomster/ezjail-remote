from setuptools import setup, find_packages

version = '0.2.1'

setup(name='ezjailremote',
      version=version,
      description="a remote control and convenience wrapper for ezjail",
      long_description=(
          open('README.rst').read()
          + '\n' +
          'Change history\n'
          '==============\n'
          + '\n' +
          open('HISTORY.rst').read()
          + '\n' +
          'Download\n'
          '========\n'),
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: BSD :: FreeBSD',
        'Programming Language :: Python',
        'Topic :: System :: Systems Administration',
      ],  # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
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
      extras_require={
          'tests': ['unittest2']
      },
      entry_points="""
      # -*- Entry points: -*-
        [console_scripts]
        ezjail-remote=ezjailremote:commandline
      """,
      )

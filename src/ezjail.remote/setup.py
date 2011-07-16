from setuptools import setup, find_packages

version = '0.0'

requires = [
    "Fabric",
]

test_requires = [
    "zope.testing",
    "unittest2",
]


setup(name='ezjail.remote',
      version=version,
      description="",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='Tom Lazar',
      author_email='tom@tomster.org',
      url='',
      license='BSD',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
         requires
      ],
      extras_require = {
        "tests": test_requires,
      },
      entry_points="""
      # -*- Entry points: -*-
        [console_scripts]
        ezjail-remote=ezjailremote.command:main
      """,
      )

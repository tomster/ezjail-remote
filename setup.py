from setuptools import setup, find_packages

version = '0.1'

setup(name='ezjailremote',
      version=version,
      description="",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='',
      author_email='',
      url='',
      license='',
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

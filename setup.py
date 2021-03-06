import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.rst')) as f:
    README = f.read()

with open(os.path.join(here, 'requirements.txt')) as f:
    requires = filter(None, f.readlines())

with open(os.path.join(here, 'VERSION')) as f:
    version = f.read().strip()

setup(name='goggles',
      version=version,
      description='Tools for deep diving in Vumi log files.',
      long_description=README,
      classifiers=["Programming Language :: Python"],
      author='Simon de Haan',
      author_email='simon@praekeltfoundation.org',
      url='http://github.com/smn/goggles',
      license='BSD',
      keywords='vumi log',
      scripts=[],
      packages=find_packages(),
      include_package_data=True,
      dependency_links=[
          ('https://github.com/dreid/treq/archive/master.tar.gz'
           '#egg=treq-0.2.1+dev'),
      ],
      zip_safe=False,
      install_requires=requires,
      tests_require=requires)

from setuptools import setup

setup(name='redag',
      version='1.0',
      description='Python relation data generation framework',
      author='Tomasz Cakala',
      author_email='tc360950@gmail.com',
      packages=['redag'],
      install_requires=['networkx>=2.6.3']
     )
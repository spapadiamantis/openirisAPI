from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 3 - Alpha',
  'Intended Audience :: Research',
  'Topic :: Software Development :: Build Tools',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='openirisapi',
  version='0.0.1',
  description='A very basic API built upon requests for openiris.io',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='https://gitlab.in2p3.fr/sotirios.PAPADIAMANTIS/openirisAPI.git',  
  author='Sotiris Papadiamantis',
  author_email='sotirios.papadiamantis@univ-amu.fr',
  license='MIT', 
  classifiers=classifiers,
  keywords='calculator', 
  packages=find_packages(),
  install_requires=['pandas', 'json', 'requests', 'ast'] 
)

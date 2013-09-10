from setuptools import setup, find_packages

setup(
    name='niquery',
    version='0.0.1',
    author='Nolan Nichols',
    author_email='nolan.nichols@gmail.com',
    packages=find_packages(exclude=["tests.*", "tests"]),
    scripts=[],
    url='http://pypi.python.org/pypi/niquery/',
    license='Apache 2.0',
    description='Framework to query neuroimaging databases.',
    long_description=open('README').read(),
    install_requires=["Pyro4", "requests", "numpy", "nibabel", 'web'],
)

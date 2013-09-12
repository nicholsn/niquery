from setuptools import setup, find_packages

setup(
    name='niquery',
    version='0.0.2',
    author='Nolan Nichols',
    author_email='nolan.nichols@gmail.com',
    packages=find_packages(exclude=["tests.*", "tests"]),
    scripts=[],
    url='http://pypi.python.org/pypi/niquery/',
    license='Apache 2.0',
    description='Framework to query neuroimaging databases as RDF.',
    long_description=open('README').read(),
    install_requires=["Flask", "Flask-RESTful", "prov", "PyLD", "rdflib", "requests"],
)

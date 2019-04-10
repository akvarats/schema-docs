from setuptools import setup, find_packages


setup(
    name='schema_docs',
    version='0.1',
    description='schema_docs',
    long_description="",
    author='Alexander Kvaratskheliya',
    author_email='akvarats@gmail.com',
    url='https://github.com/akvarats/schema_docs',
    license="",
    packages=find_packages(exclude=('tests', 'docs')),
    install_requires=[
        "python-dateutil"
    ]
)

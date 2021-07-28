from setuptools import setup, find_packages

setup(
    name='swapcard_demo',
    version='1.0',
    package_dir={'':'pages'},
    packages=find_packages("pages", exclude=["tests"]),
    url='',
    license='',
    author='gabrielcarioca',
    author_email='gabrielcarioca23@gmail.com',
    description='Technical Project for Swapcard'
)

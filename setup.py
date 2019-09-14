import setuptools
import os


requirementPath = 'requirements.txt'
if (os.path.isfile(requirementPath)):
    with open(requirementPath) as f:
        install_requires = f.read().splitlines()

with open("README.md", "r") as readme_file:
    long_description = readme_file.read()

setuptools.setup(
    name="irrigationserver",
    version="0.1",
    author="Marti Municoy",
    author_email="martimunicoy@gmail.com",
    description="This is a Python3 module to set up an irrigation server to control a garden water system through a web server",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/martimunicoy/IrrigationServer",
    packages=setuptools.find_packages(),
    license='MIT',
    install_requires=install_requires
)

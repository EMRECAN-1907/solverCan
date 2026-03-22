from setuptools import setup, find_packages

setup(
    name="solverCan",
    version="0.1.4",
    description="Mathematical Function Solver from Dataset",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Emrecan Bayhan",
    author_email="bayhan.emrecan1@gmail.com",
    license="MIT",
    packages=find_packages(),
    install_requires=["matplotlib>=3.0"],
    python_requires=">=3.7",
)
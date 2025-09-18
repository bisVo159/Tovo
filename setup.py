from setuptools import setup, find_packages

setup(
    name="tovo",                         # keep it clean
    version="0.1.0",
    packages=find_packages(),            # <-- no `where="src"`
    include_package_data=True,
    python_requires=">=3.8",
)


from setuptools import setup, find_packages

setup(
    name='pybeamdimap',
    author='Panji P. Brotoisworo',
    url='https://github.com/pbrotoisworo/py-beam-dimap',
    version=0.1,
    description='Interface to easily parse and navigate BEAM-DIMAP XML data',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'pytest'
    ],
    classifiers=[
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    keywords="Copernicus, Dimap, S2nap, Remote Sensing",
)

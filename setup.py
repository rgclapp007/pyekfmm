#!/usr/bin/env python
# -*- encoding: utf8 -*-

from setuptools import setup, Extension
# Import the original build_ext command to subclass it
from setuptools.command.build_ext import build_ext as _build_ext

# DO NOT import numpy at the top level here for get_include()

long_description = """
Source code: https://github.com/aaspip/pyekfmm""".strip()

# Custom build_ext command to handle NumPy includes at build time
class BuildExtNumpy(_build_ext):
    def finalize_options(self):
        _build_ext.finalize_options(self)
        # Import numpy and add its include directory ONLY when extensions are actually built.
        # This ensures numpy is available as a build dependency.
        try:
            import numpy
            self.include_dirs.append(numpy.get_include())
        except ImportError:
            print("NumPy is required to build C extensions, but it's not installed.")
            print("Please ensure NumPy is listed in your pyproject.toml's build-system.requires")
            print("or ensure it's installed in the build environment.")
            raise # Re-raise the ImportError to fail the build clearly if NumPy isn't there

# Define Extension objects.
# The numpy include_dirs will be added by our custom BuildExtNumpy command.
eikonalc_module = Extension('eikonalc', sources=['pyekfmm/src/eikonal.c'])
eikonalvtic_module = Extension('eikonalvtic', sources=['pyekfmm/src/eikonalvti.c'])

setup(
    name="pyekfmm",
    version="0.0.8.8",
    license='MIT License',
    description="Fast Marching Method for Traveltime Calculation",
    long_description=long_description,
    author="pyekfmm developing team",
    author_email="chenyk2016@gmail.com",
    url="https://github.com/aaspip/pyekfmm",
    
    packages=['pyekfmm'],
    include_package_data=True,
    zip_safe=False, # C extensions generally mean zip_safe should be False
    
    # Runtime dependencies
    install_requires=[
        "numpy>=1.16.0",  # Specify a reasonable minimum NumPy version
        "scipy",
        "matplotlib"
    ],
    
    # Build-time C extensions
    ext_modules=[eikonalc_module, eikonalvtic_module],
    
    # Use the custom build_ext to handle numpy includes
    cmdclass={'build_ext': BuildExtNumpy},
    
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Operating System :: Unix",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8", # As per original, consider if it supports newer versions
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Physics"
    ],
    keywords=[
        "seismology", "exploration seismology", "array seismology", "traveltime", "ray tracing", "earthquake location", "earthquake relocation", "surface wave tomography", "body wave tomography"
    ],
    extras_require={
        "docs": ["sphinx", "ipython", "runipy"]
    }
)

# What is pyvrs?

pyvrs is a Python interface for C++ library [VRS](https://github.com/facebookresearch/vrs) using [pybind11](https://github.com/pybind/pybind11).

# Documentation

See [API documentation](https://pyvrs.readthedocs.io/en/latest/)

# Installation
## Install released builds
pypi package is built with [this Github Action](https://github.com/facebookresearch/pyvrs/blob/main/.github/workflows/deploy.yml) manually.
```
pip install vrs
```

## From source
```
# Build locally
git clone --recursive https://github.com/facebookresearch/pyvrs.git
cd pyvrs
# if you are updating an existing checkout
git submodule sync --recursive
git submodule update --init --recursive

# Install VRS dependencies: https://github.com/facebookresearch/vrs#instructions-macos-and-ubuntu-and-container

python -m pip install -e .
```

## Using `vcpkg`
1. Open a Developer Command Prompt for VS 2019/2022 at the root of this repository.
2. (optional) Set the `VCPKG_ROOT` environmental variable using `set VCPKG_ROOT={PATH_TO_VCPKG_ROOT}`. _This is necessary when `vcpkg` is not at `../vcpkg`._
3. (optional) Set the `VCPKG_TRIPLET` environmental variable using `set VCPKG_TRIPLET=x64-windows-vc142`. _This is necessary when the default triplet does not compile._
4. (optional) Add a `vcpkg` baseline using `VCPKG_ROOT/vcpkg.exe x-update-baseline --add-initial-baseline`.  
5. `pip install .` (using editable mode `-e` results in dislocated package & dlls, meaning we need to copy the `*.dll` from the build directory to the root path where the `*.pyd` is located)

# Contributing

We welcome contributions! See [CONTRIBUTING](CONTRIBUTING.md) for details on how
to get started, and our [code of conduct](CODE_OF_CONDUCT.md).

# License

VRS is released under the [Apache 2.0 license](LICENSE).

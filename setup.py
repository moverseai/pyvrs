#!/usr/bin/env python
# Copyright (c) Meta Platforms, Inc. and affiliates.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import subprocess
import sys
from pathlib import Path

from setuptools import Extension, find_packages, setup
from setuptools.command.build_ext import build_ext

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

def _get_sha():
    sha = "Unknown"
    try:
        sha = (
            subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=str(ROOT_DIR))
            .decode("ascii")
            .strip()
        )
    except Exception:
        pass
    return sha


def get_version():
    path = os.path.join(ROOT_DIR, "version.txt")
    version = open(path, "r").read().strip()

    if os.getenv("PYVRS_TEST_BUILD"):
        sha = _get_sha()
        if sha != "Unknown":
            version += "+" + sha[:7]

    return version

class CMakeExtension(Extension):
    def __init__(self, name, sourcedir=""):
        Extension.__init__(self, name, sources=[])
        self.sourcedir = os.path.abspath(sourcedir)


class CMakeBuild(build_ext):
    def run(self):
        try:
            subprocess.check_output(["cmake", "--version"])
        except OSError:
            raise RuntimeError("CMake is not available.")
        super().run()

    def build_extension(self, ext):
        extdir = os.path.abspath(os.path.dirname(self.get_ext_fullpath(ext.name)))

        if not extdir.endswith(os.path.sep):
            extdir += os.path.sep

        if "DEBUG" in os.environ:
            cfg = "Debug" if os.environ["DEBUG"] == "1" else "Release"
        else:
            cfg = "Debug" if self.debug else "Release"

        #moverse stuff
        VCPKG_ENV_VAR = 'VCPKG_ROOT'
        if VCPKG_ENV_VAR in os.environ:
            vcpkg_path = os.path.join(os.environ[VCPKG_ENV_VAR], "scripts", "buildsystems", "vcpkg.cmake")
        else:
            vcpkg_path = os.path.join(Path(__file__).parent.parent, "vcpkg", "scripts", "buildsystems", "vcpkg.cmake")

        cmake_args = [
            f"-DCMAKE_BUILD_TYPE={cfg}",
            f"-DCMAKE_LIBRARY_OUTPUT_DIRECTORY={extdir}",
            # r"-DCMAKE_TOOLCHAIN_FILE=..\vcpkg\scripts\buildsystems\vcpkg.cmake",
            # r"-DCMAKE_TOOLCHAIN_FILE=C:\Users\vlad\code\vcpkg_vrs_player\scripts\buildsystems\vcpkg.cmake",
            f"-DCMAKE_TOOLCHAIN_FILE={vcpkg_path}",
            f"-DPYTHON_EXECUTABLE={sys.executable}",
            "-GCodeBlocks",
            # '-DVCPKG_TARGET_TRIPLET=x64-windows-vc142',
        ]
        build_args = ["--target", os.path.basename(ext.name)]

        VCPKG_TRIPLET_ENV_VAR = 'VCPKG_TRIPLET'
        if VCPKG_TRIPLET_ENV_VAR in os.environ:
            cmake_args += [f'-DVCPKG_TARGET_TRIPLET={os.environ[VCPKG_TRIPLET_ENV_VAR]}']

        # Default to Ninja
        if "CMAKE_GENERATOR" not in os.environ:
            cmake_args += ["-GNinja"]

        if not os.path.exists(self.build_temp):
            os.makedirs(self.build_temp)
        subprocess.check_call(
            ["cmake", ext.sourcedir] + cmake_args, cwd=self.build_temp
        )
        subprocess.check_call(
            ["cmake", "--build", "."] + build_args, cwd=self.build_temp
        )


def main():
    with open(os.path.join(ROOT_DIR, "README.md"), encoding="utf-8") as f:
        long_description = f.read()

    setup(
        name="vrs",
        version=get_version(),
        description="Python API for VRS",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/facebookresearch/pyvrs",
        author="Meta Reality Labs Research",
        license="Apache-2.0",
        install_requires=["numpy", "typing", "dataclasses"],
        python_requires=">=3.7",
        packages=find_packages(),
        zip_safe=False,
        ext_modules=[CMakeExtension("vrsbindings", sourcedir=ROOT_DIR)],
        cmdclass={
            "build_ext": CMakeBuild,
        },
    )


if __name__ == "__main__":
    main()

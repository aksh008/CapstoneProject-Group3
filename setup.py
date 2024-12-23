from pathlib import Path
from setuptools import find_packages, setup
from setuptools.command.bdist_wheel import bdist_wheel
import shutil

# Package meta-data.
NAME = 'harit_model'
DESCRIPTION = "Plant Disease Classification Model"
URL = "https://github.com/aksh008/CapstoneProject-Group3/tree/main/harit_model"
EMAIL = "------"
AUTHOR = "----------"
REQUIRES_PYTHON = ">=3.7.0"

long_description = DESCRIPTION

# Load the package's VERSION file as a dictionary.
about = {}
ROOT_DIR = Path(__file__).resolve().parent
REQUIREMENTS_DIR = ROOT_DIR / 'requirements'
PACKAGE_DIR = ROOT_DIR / 'harit_model'
with open(PACKAGE_DIR / "VERSION") as f:
    _version = f.read().strip()
    about["__version__"] = _version

# What packages are required for this module to be executed?
def list_reqs(fname="requirements.txt"):
    with open(REQUIREMENTS_DIR / fname) as fd:
        return fd.read().splitlines()

# Custom command to copy the wheel file
class BdistWheelCopyCommand(bdist_wheel):
    def run(self):
        bdist_wheel.run(self)
        for wheel_file in Path(self.dist_dir).glob('*.whl'):
            shutil.copy(wheel_file, ROOT_DIR / 'harit_model_api')
            print(f"Copied {wheel_file.name} to {ROOT_DIR}/harit_model_api folder")

# Where the magic happens:
setup(
    name=NAME,
    version=about["__version__"],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(exclude=("tests",)),
    package_data={"harit_model": ["VERSION"]},
    install_requires=list_reqs(),
    extras_require={},
    include_package_data=True,
    license="BSD-3",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    cmdclass={
        'bdist_wheel': BdistWheelCopyCommand,
    },
)
import sys
from pathlib import Path
file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))
 
 
from harit_model.config.core import PACKAGE_ROOT, config
# with open(PACKAGE_ROOT / "VERSION") as version_file:
#     __version__ = version_file.read().strip()

def increment_version(version: str) -> str:
    """Increment the patch version (e.g., 1.0.0 -> 1.0.1)."""
    major, minor, patch = map(int, version.split("."))
    patch += 1  # Increment patch version
    return f"{major}.{minor}.{patch}"

# Read the current version
with open(PACKAGE_ROOT / "VERSION", "r") as version_file:
    current_version = version_file.read().strip()

# Increment the version
new_version = increment_version(current_version)

# Write the new version back to the VERSION file
with open(PACKAGE_ROOT / "VERSION", "w") as version_file:
    version_file.write(new_version)

# Use the updated version in your script
__version__ = new_version

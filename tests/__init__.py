"""Test package for Cloud Pioneer.

This package contains all test modules for the Cloud Pioneer project.
Tests are organized by module and functionality.
"""

import os
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.absolute()
sys.path.insert(0, str(project_root))

# Import test modules
from . import test_agent, test_main  # noqa: F401

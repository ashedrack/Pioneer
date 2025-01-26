"""Test package for Cloud Pioneer.

import os
import sys

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from . import test_agent, test_main

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


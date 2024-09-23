import os
import sys
import time
import pytest
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.funcs import run_module

run_module()
time.sleep(5)
import os, sys, unittest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

print("Running all tests...\n")
suite = unittest.defaultTestLoader.discover(os.path.dirname(__file__), pattern="test_*.py")
unittest.TextTestRunner(verbosity=2).run(suite)
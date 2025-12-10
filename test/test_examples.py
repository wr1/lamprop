import subprocess
import sys


def test_example_yaml():
    """Test that example_yaml.py runs without error."""
    result = subprocess.run(
        [sys.executable, "examples/example_yaml.py"],
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0

def test_example_py():
    """Test that example_py.py runs without error."""
    result = subprocess.run(
        [sys.executable, "examples/example_py.py"],
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0

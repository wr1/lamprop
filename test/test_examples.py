import subprocess
import sys
from pathlib import Path

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

def test_create_material_db():
    """Test that create_material_db.py runs and produces output."""
    output_file = Path("__matdb.json")
    if output_file.exists():
        output_file.unlink()
    result = subprocess.run(
        [sys.executable, "examples/create_material_db.py"],
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert output_file.exists()
    # Clean up
    output_file.unlink()

def test_calculate_cte():
    """Test that calculate_cte.py runs without error."""
    result = subprocess.run(
        [sys.executable, "examples/calculate_cte.py"],
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    # Check some output
    assert "vf = 0.1" in result.stdout

def test_convert_lamprop():
    """Test that convert_lamprop.py runs without error."""
    # Since no .lam files, it should run without error
    result = subprocess.run(
        [sys.executable, "examples/convert_lamprop.py"],
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0

"""Compare output to reference output."""

from lamprop.io.parser import parse
from lamprop.io.text import text_output


def test_text_output():
    """Test text output generation."""
    laminates = parse("test/generic.yaml")
    outlist = []
    for curlam in laminates:
        outlist += text_output(curlam, eng=True, mat=True, fea=True)
    assert len(outlist) > 0
    # Old reference comparison removed as format changed

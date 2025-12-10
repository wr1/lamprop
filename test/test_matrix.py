# file: test_matrix.py
#
# Tests for matrix utilities using numpy.

import numpy as np

from lamprop.core.utils import delete

_rndm = np.array(
    [
        [0.21, 0.76, 0.07, 0.94, 0.33, 0.57],
        [0.76, 0.07, 0.94, 0.33, 0.57, 0.98],
        [0.07, 0.94, 0.33, 0.57, 0.98, 0.49],
        [0.94, 0.33, 0.57, 0.98, 0.49, 0.36],
        [0.33, 0.57, 0.98, 0.49, 0.36, 0.01],
        [0.57, 0.98, 0.49, 0.36, 0.01, 0.71],
    ]
)

_invm = np.array(
    [
        [-1.52, -0.48, 0.34, 1.54, -0.88, 0.88],
        [-0.48, -0.66, 0.52, 0.04, 0.01, 0.93],
        [0.34, 0.52, -0.51, -0.71, 1.23, -0.29],
        [1.54, 0.04, -0.71, -0.01, 0.5, -0.8],
        [-0.88, 0.01, 1.23, 0.5, -0.45, -0.4],
        [0.88, 0.93, -0.29, -0.8, -0.4, 0.03],
    ]
)


def test_ident():
    """Test identity matrix."""
    m = np.eye(6)
    for j in range(len(m)):
        for k in range(len(m[0])):
            if j == k:
                assert m[j, k] == 1
            else:
                assert m[j, k] == 0


def test_zeros():
    """Test zeros matrix."""
    m = np.zeros((6, 6))
    for j in range(len(m)):
        for k in range(len(m[0])):
            assert m[j, k] == 0


def test_det_dia():
    """Test determinant of diagonal matrix."""
    m = np.diag([1, 2, 3])
    assert np.linalg.det(m) == 6


def test_det_3():
    """Test determinant of 3x3 matrix."""
    m = np.array([[6, 1, 1], [4, -2, 5], [2, 8, 7]])
    assert np.linalg.det(m) == -306


def test_det_6():
    """Test determinant of 6x6 matrix."""
    assert round(np.linalg.det(_rndm), 2) == -0.45


def test_inv_6():
    """Test inverse of 6x6 matrix."""
    inv = np.round(np.linalg.inv(_rndm), 2)
    expected = np.round(_invm, 2)
    np.testing.assert_array_almost_equal(inv, expected)


def test_delete():
    """Test deleting row and column."""
    smaller = np.array(
        [
            [0.21, 0.76, 0.07, 0.33, 0.57],
            [0.07, 0.94, 0.33, 0.98, 0.49],
            [0.94, 0.33, 0.57, 0.49, 0.36],
            [0.33, 0.57, 0.98, 0.36, 0.01],
            [0.57, 0.98, 0.49, 0.01, 0.71],
        ]
    )
    assert np.array_equal(delete(_rndm, 1, 3), smaller)

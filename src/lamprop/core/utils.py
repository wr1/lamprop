"""Utility functions for matrix operations."""
import math
import numpy as np

_LIMIT = 1e-10

def tbar(degrees: float) -> np.ndarray:
    """Matrix for rotating lamina coordinates around the z-axis."""
    theta = math.radians(degrees)
    c, s = math.cos(theta), math.sin(theta)
    Tbar = np.array([
        [c * c, s * s, 0, 0, 0, c * s],
        [s * s, c * c, 0, 0, 0, -c * s],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 0, c, -s, 0],
        [0, 0, 0, s, c, 0],
        [-2 * c * s, 2 * c * s, 0, 0, 0, c * c - s * s],
    ])
    return Tbar

def clean(m: np.ndarray) -> np.ndarray:
    """Set matrix numbers < _LIMIT with 0."""
    rv = m.copy()
    rv[np.abs(rv) < _LIMIT] = 0.0
    return rv

def delete(m: np.ndarray, r: int, k: int) -> np.ndarray:
    """Delete row r and column k from matrix m."""
    return np.delete(np.delete(m, r, axis=0), k, axis=1)

def is_ortho(C: np.ndarray) -> bool:
    """Determine if a stiffness matrix is orthotropic."""
    zero_indices = [
        (0, 3), (0, 4), (0, 5),
        (1, 3), (1, 4), (1, 5),
        (2, 3), (2, 4), (2, 5),
        (3, 0), (3, 1), (3, 2), (3, 4), (3, 5),
        (4, 0), (4, 1), (4, 2), (4, 3), (4, 5),
        (5, 0), (5, 1), (5, 2), (5, 3), (5, 4),
    ]
    for i, j in zero_indices:
        if not np.isclose(C[i, j], 0.0):
            return False
    return True

def is_ti(C: np.ndarray) -> bool:
    """Determine if the stiffness matrix C is transversely isotropic."""
    if not is_ortho(C):
        return False
    return np.isclose(C[4, 4], C[5, 5]) and np.isclose(
        C[3, 3], 2 * (C[1, 1] - C[1, 2])
    )

def to_abaqus_i(C: np.ndarray) -> np.ndarray:
    """Convert stiffness matrix to Abaqus format and SI units."""
    D = C * 1e6
    D[0, 3] = C[0, 5] * 1e6
    D[0, 5] = C[0, 3] * 1e6
    D[1, 3] = C[1, 5] * 1e6
    D[1, 5] = C[1, 3] * 1e6
    D[2, 3] = C[2, 5] * 1e6
    D[2, 5] = C[2, 3] * 1e6
    D[3, 3] = C[5, 5] * 1e6
    D[5, 5] = C[3, 3] * 1e6
    return D

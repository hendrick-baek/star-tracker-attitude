import numpy as np


def Rz(theta: float) -> np.ndarray:
    """
    Z-axis rotation matrix

    Parameters
    ----------
    theta : float
        Rotation angle in radians

    Returns
    -------
    R : (3,3) ndarray
        Rotation matrix
    """
    return np.array([
        [np.cos(theta), -np.sin(theta), 0.0],
        [np.sin(theta),  np.cos(theta), 0.0],
        [0.0,            0.0,           1.0]
    ])


def is_orthogonal(R: np.ndarray, tol: float = 1e-8) -> bool:
    """
    Check if R^T R ≈ I
    """
    I = np.eye(3)
    return np.allclose(R.T @ R, I, atol=tol)


def preserves_norm(R: np.ndarray, v: np.ndarray, tol: float = 1e-8) -> bool:
    """
    Check if rotation preserves vector norm
    """
    return np.isclose(
        np.linalg.norm(R @ v),
        np.linalg.norm(v),
        atol=tol
    )

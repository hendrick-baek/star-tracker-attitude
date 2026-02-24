import numpy as np

####### day 1: basic rotation matrices #######
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

####### day 2: Rodrigues' rotation formula #######

def skew(u: np.ndarray) -> np.ndarray:
    """
    Return skew-symmetric matrix of vector u.
    [u]_x such that [u]_x v = u x v
    """
    ux, uy, uz = u
    return np.array([
        [0.0, -uz,  uy],
        [uz,   0.0, -ux],
        [-uy,  ux,   0.0]
    ])


def axis_angle_to_R(u: np.ndarray, theta: float) -> np.ndarray:
    """
    Rodrigues' rotation formula.

    Parameters
    ----------
    u : (3,) ndarray
        Rotation axis (not necessarily unit length)
    theta : float
        Rotation angle in radians

    Returns
    -------
    R : (3,3) ndarray
        Rotation matrix in SO(3)
    """
    u = u / np.linalg.norm(u)  # normalize axis
    K = skew(u)
    I = np.eye(3)

    R = I + np.sin(theta) * K + (1 - np.cos(theta)) * (K @ K)
    return R
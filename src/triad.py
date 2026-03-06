import numpy as np


def normalize(v):
    """
    Normalize a 3D vector.
    """
    norm = np.linalg.norm(v)
    if norm < 1e-12:
        raise ValueError("Cannot normalize a near-zero vector.")
    return v / norm


def solve_triad(r1, r2, b1, b2):
    """
    TRIAD attitude determination.

    Convention
    ----------
    b = R r

    Parameters
    ----------
    r1, r2 : ndarray shape (3,)
        Inertial-frame unit vectors
    b1, b2 : ndarray shape (3,)
        Corresponding body-frame unit vectors

    Returns
    -------
    R : ndarray shape (3, 3)
        Rotation matrix from inertial frame to body frame
    """
    # Normalize inputs
    r1 = normalize(r1)
    r2 = normalize(r2)
    b1 = normalize(b1)
    b2 = normalize(b2)

    # Inertial triad
    t1_r = r1
    cross_r = np.cross(r1, r2)
    norm_cross_r = np.linalg.norm(cross_r)
    if norm_cross_r < 1e-12:
        raise ValueError("TRIAD failed: r1 and r2 are nearly parallel.")
    t2_r = cross_r / norm_cross_r
    t3_r = np.cross(t1_r, t2_r)

    # Body triad
    t1_b = b1
    cross_b = np.cross(b1, b2)
    norm_cross_b = np.linalg.norm(cross_b)
    if norm_cross_b < 1e-12:
        raise ValueError("TRIAD failed: b1 and b2 are nearly parallel.")
    t2_b = cross_b / norm_cross_b
    t3_b = np.cross(t1_b, t2_b)

    # Basis matrices
    T_r = np.column_stack((t1_r, t2_r, t3_r))
    T_b = np.column_stack((t1_b, t2_b, t3_b))

    # Rotation: inertial -> body
    R = T_b @ T_r.T

    return R
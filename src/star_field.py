import numpy as np


def random_unit_vectors(M: int) -> np.ndarray:
    """
    Generate M random unit vectors uniformly over the sphere (isotropic).
    Output shape: (M, 3)
    """
    v = np.random.randn(M, 3)
    v /= np.linalg.norm(v, axis=1, keepdims=True)
    return v


def spherical_cap_fraction(fov_deg: float) -> float:
    """
    Fraction of sphere area covered by a spherical cap with half-angle fov_deg.
    fraction = (1 - cos(theta)) / 2
    """
    theta = np.deg2rad(fov_deg)
    return (1.0 - np.cos(theta)) / 2.0


def expected_visible_count(N_total: int, fov_deg: float) -> float:
    return N_total * spherical_cap_fraction(fov_deg)


def filter_fov_body(b_vectors: np.ndarray, boresight: np.ndarray, fov_deg: float) -> np.ndarray:
    """
    FOV filter in BODY/CAMERA frame.
    Condition: b · c >= cos(theta_fov)
    """
    c = boresight / np.linalg.norm(boresight)
    cos_lim = np.cos(np.deg2rad(fov_deg))
    dots = b_vectors @ c
    return b_vectors[dots >= cos_lim]
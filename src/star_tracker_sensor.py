import numpy as np
from star_field import filter_fov_body


def assign_magnitude_uniform(M: int, m_min: float = 0.0, m_max: float = 8.0) -> np.ndarray:
    """
    Simple magnitude model: uniform in [m_min, m_max].
    Lower magnitude = brighter.
    """
    return np.random.uniform(m_min, m_max, size=(M,))


def apply_magnitude_cut(vectors: np.ndarray, mags: np.ndarray, m_lim: float) -> tuple[np.ndarray, np.ndarray]:
    """
    Keep stars with magnitude <= m_lim (visible/detectable).
    """
    mask = mags <= m_lim
    return vectors[mask], mags[mask]


def simulate_visible_stars(
    b_all: np.ndarray,
    boresight: np.ndarray,
    fov_deg: float,
    mags: np.ndarray,
    m_lim: float
) -> tuple[np.ndarray, np.ndarray]:
    """
    Pipeline (body frame):
    1) FOV filter
    2) magnitude cut
    """
    b_fov = filter_fov_body(b_all, boresight, fov_deg)

    # Important: we must apply the same mask to magnitudes.
    # We'll recompute the FOV mask here to keep it explicit and correct.
    c = boresight / np.linalg.norm(boresight)
    cos_lim = np.cos(np.deg2rad(fov_deg))
    dots = b_all @ c
    mask_fov = dots >= cos_lim

    mags_fov = mags[mask_fov]

    b_final, mags_final = apply_magnitude_cut(b_fov, mags_fov, m_lim)
    return b_final, mags_final
import numpy as np
from star_field import random_unit_vectors, filter_fov_body
from star_tracker_sensor import assign_magnitude_uniform, apply_magnitude_cut


def add_measurement_noise(vectors, sigma):
    noise = np.random.randn(*vectors.shape) * sigma
    noisy = vectors + noise
    noisy /= np.linalg.norm(noisy, axis=1, keepdims=True)
    return noisy


def simulate_star_tracker_measurements(
    N_total,
    R_true,
    fov_deg,
    m_lim,
    noise_sigma,
):
    """
    Full star tracker simulation pipeline
    """

    # 1 inertial stars
    r_all = random_unit_vectors(N_total)

    # 2 body vectors
    b_true = (R_true @ r_all.T).T

    # 3 magnitude assignment
    mags = assign_magnitude_uniform(N_total)

    # 4 FOV filtering
    boresight = np.array([0.0, 0.0, 1.0])
    b_fov = filter_fov_body(b_true, boresight, fov_deg)

    # find corresponding r vectors
    cos_lim = np.cos(np.deg2rad(fov_deg))
    dots = b_true @ boresight
    mask_fov = dots >= cos_lim

    r_fov = r_all[mask_fov]
    mags_fov = mags[mask_fov]

    # 5 magnitude cut
    r_vis, mags_vis = apply_magnitude_cut(r_fov, mags_fov, m_lim)

    mask_mag = mags_fov <= m_lim
    b_vis = b_fov[mask_mag]

    # 6 noise
    b_meas = add_measurement_noise(b_vis, noise_sigma)

    return r_vis, b_meas
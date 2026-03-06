import numpy as np

from quaternion import quat_to_rot
from wahba import solve_wahba
from triad import solve_triad
from star_tracker_simulator import simulate_star_tracker_measurements


def attitude_error_deg(R_true, R_est):
    """
    Compute the principal rotation angle error in degrees.
    """
    R_err = R_est @ R_true.T
    trace_val = np.trace(R_err)
    cos_angle = 0.5 * (trace_val - 1.0)
    cos_angle = np.clip(cos_angle, -1.0, 1.0)
    angle_rad = np.arccos(cos_angle)
    return np.degrees(angle_rad)


def main():
    np.random.seed(42)

    # True attitude quaternion
    q_true = np.array([0.9659258, 0.0, 0.2588190, 0.0])
    q_true = q_true / np.linalg.norm(q_true)
    R_true = quat_to_rot(q_true)

    # Simulated star tracker measurements
    # NOTE:
    # Your actual simulator signature is:
    # simulate_star_tracker_measurements(N_total, R_true, fov_deg, m_lim, noise_sigma)
    r_visible, b_meas = simulate_star_tracker_measurements(
        N_total=10000,
        R_true=R_true,
        fov_deg=20.0,
        m_lim=2.0,
        noise_sigma=0.001
    )

    num_visible = len(r_visible)
    print(f"Visible stars: {num_visible}")

    if num_visible < 2:
        raise ValueError("Need at least 2 visible stars for TRIAD.")

    # -------------------------
    # TRIAD estimate
    # -------------------------
    r1 = r_visible[0]
    r2 = r_visible[1]
    b1 = b_meas[0]
    b2 = b_meas[1]

    R_est_triad = solve_triad(r1, r2, b1, b2)
    triad_error = attitude_error_deg(R_true, R_est_triad)

    # -------------------------
    # Davenport / Wahba estimate
    # -------------------------
    # IMPORTANT:
    # Your solve_wahba signature is:
    # solve_wahba(b_vectors, r_vectors, weights=None)
    # and it returns a quaternion, not a rotation matrix.
    q_est_wahba = solve_wahba(b_meas, r_visible)
    R_est_wahba = quat_to_rot(q_est_wahba).T
    wahba_error = attitude_error_deg(R_true, R_est_wahba)

    print("\nTrue Rotation Matrix:")
    print(R_true)

    print("\nTRIAD Estimated Rotation Matrix:")
    print(R_est_triad)

    print("\nDavenport/Wahba Estimated Rotation Matrix:")
    print(R_est_wahba)

    print(f"\nTRIAD Attitude Error (deg): {triad_error:.6f}")
    print(f"Davenport/Wahba Attitude Error (deg): {wahba_error:.6f}")


if __name__ == "__main__":
    main()
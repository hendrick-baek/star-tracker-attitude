import numpy as np

from quaternion import quat_to_rot
from wahba import solve_wahba_rotation
from quest import solve_quest_rotation
from star_tracker_simulator import simulate_star_tracker_measurements


def attitude_error_deg(R_true, R_est):

    R_err = R_est @ R_true.T

    trace_val = np.trace(R_err)

    cos_angle = 0.5 * (trace_val - 1)

    cos_angle = np.clip(cos_angle, -1.0, 1.0)

    angle = np.arccos(cos_angle)

    return np.degrees(angle)


def main():

    np.random.seed(42)

    q_true = np.array([0.9659258, 0, 0.2588190, 0])
    q_true = q_true / np.linalg.norm(q_true)

    R_true = quat_to_rot(q_true)

    r_visible, b_meas = simulate_star_tracker_measurements(
        N_total=10000,
        R_true=R_true,
        fov_deg=20.0,
        m_lim=2.0,
        noise_sigma=0.001
    )

    print("Visible stars:", len(r_visible))

    # QUEST
    R_est_quest = solve_quest_rotation(b_meas, r_visible)

    # Davenport
    R_est_dav = solve_wahba_rotation(b_meas, r_visible)

    err_quest = attitude_error_deg(R_true, R_est_quest)
    err_dav = attitude_error_deg(R_true, R_est_dav)

    print("\nQUEST Error (deg):", err_quest)
    print("Davenport Error (deg):", err_dav)


if __name__ == "__main__":
    main()
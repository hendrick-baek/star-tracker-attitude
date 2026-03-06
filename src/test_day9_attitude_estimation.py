import numpy as np
from rotations import Rz
from star_tracker_simulator import simulate_star_tracker_measurements
from wahba import solve_wahba
from quaternion import quat_to_rot


def attitude_error(R_true, R_est):

    val = (np.trace(R_true.T @ R_est) - 1) / 2
    val = np.clip(val, -1.0, 1.0)

    return np.degrees(np.arccos(val))


def main():

    np.random.seed(0)

    # simulation parameters
    N_total = 20000
    fov_deg = 20
    m_lim = 6
    noise_sigma = 0.001

    # true spacecraft attitude
    R_true = Rz(np.deg2rad(30))

    # generate measurements
    r_i, b_i = simulate_star_tracker_measurements(
        N_total,
        R_true,
        fov_deg,
        m_lim,
        noise_sigma
    )

    print("Visible stars:", len(r_i))

    # solve Wahba
    q_est = solve_wahba(r_i, b_i)

    # convert to rotation matrix
    R_est = quat_to_rot(q_est)

    # compute error
    err = attitude_error(R_true, R_est)

    print()
    print("True Rotation:")
    print(R_true)

    print()
    print("Estimated Rotation:")
    print(R_est)

    print()
    print("Attitude Error (deg):", err)


if __name__ == "__main__":
    main()
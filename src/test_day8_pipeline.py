import numpy as np
from rotations import Rz
from star_tracker_simulator import simulate_star_tracker_measurements


def main():

    np.random.seed(0)

    N_total = 20000
    fov_deg = 20
    m_lim = 6
    noise_sigma = 0.001

    R_true = Rz(np.deg2rad(30))

    r_i, b_i = simulate_star_tracker_measurements(
        N_total,
        R_true,
        fov_deg,
        m_lim,
        noise_sigma
    )

    print("Visible stars:", len(r_i))

    print("First 5 inertial vectors:")
    print(r_i[:5])

    print("First 5 body measurements:")
    print(b_i[:5])


if __name__ == "__main__":
    main()
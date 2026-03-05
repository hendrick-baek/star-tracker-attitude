import numpy as np
from star_field import random_unit_vectors
from star_tracker_sensor import assign_magnitude_uniform, simulate_visible_stars


def main():
    np.random.seed(1)

    N_total = 200_000
    boresight = np.array([0.0, 0.0, 1.0])
    fov = 20

    b_all = random_unit_vectors(N_total)
    mags = assign_magnitude_uniform(N_total, m_min=0.0, m_max=8.0)

    for m_lim in [2.0, 4.0, 6.0, 8.0]:
        b_vis, mags_vis = simulate_visible_stars(b_all, boresight, fov, mags, m_lim)
        print(f"FOV={fov} deg | m_lim={m_lim:.1f} | visible={len(b_vis):,}")

if __name__ == "__main__":
    main()
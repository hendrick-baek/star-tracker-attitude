import numpy as np
from star_field import random_unit_vectors, spherical_cap_fraction, expected_visible_count, filter_fov_body

# Convention:
# b = R r  (inertial -> body)
# For Day 7 count validation, we can directly treat generated vectors as b (body directions),
# because isotropic distribution is rotationally invariant.

def main():
    np.random.seed(0)

    N_total = 200_000   # large for stable count
    boresight = np.array([0.0, 0.0, 1.0])

    for fov in [10, 20, 30, 40, 60]:
        b_all = random_unit_vectors(N_total)
        b_vis = filter_fov_body(b_all, boresight, fov)

        frac_theory = spherical_cap_fraction(fov)
        exp_cnt = expected_visible_count(N_total, fov)
        obs_cnt = len(b_vis)
        obs_frac = obs_cnt / N_total

        print(f"FOV={fov:>2} deg | theory frac={frac_theory:.6f} | obs frac={obs_frac:.6f} "
              f"| exp cnt={exp_cnt:,.0f} | obs cnt={obs_cnt:,.0f}")

if __name__ == "__main__":
    main()
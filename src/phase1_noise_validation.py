import numpy as np
from rotations import Rz
from wahba import solve_wahba
from quaternion import quat_to_rot


# ----------------------------------
# Rotation error (degree)
# ----------------------------------
def rotation_error_deg(R_true, R_est):
    R_err = R_true.T @ R_est
    cos_theta = (np.trace(R_err) - 1) / 2
    cos_theta = np.clip(cos_theta, -1.0, 1.0)
    theta = np.arccos(cos_theta)
    return np.rad2deg(theta)


# ----------------------------------
# Random unit vectors
# ----------------------------------
def random_unit_vectors(N):
    v = np.random.randn(N, 3)
    v /= np.linalg.norm(v, axis=1, keepdims=True)
    return v


# ----------------------------------
# Single trial
# ----------------------------------
def run_trial(num_vectors, sigma):

    # True rotation (z-axis 30 deg)
    theta = np.deg2rad(30)
    R_true = Rz(theta)

    # Inertial vectors
    r = random_unit_vectors(num_vectors)

    # True body measurement
    b_true = (R_true @ r.T).T

    # Add Gaussian noise
    b_noisy = b_true + sigma * np.random.randn(*b_true.shape)
    b_noisy /= np.linalg.norm(b_noisy, axis=1, keepdims=True)

    # Estimate rotation
    q_est = solve_wahba(r, b_noisy)
    R_est = quat_to_rot(q_est)

    # Compute error
    return rotation_error_deg(R_true, R_est)


# ----------------------------------
# Monte Carlo experiment
# ----------------------------------
def monte_carlo(trials, num_vectors, sigma):

    errors = []

    for _ in range(trials):
        err = run_trial(num_vectors, sigma)
        errors.append(err)

    errors = np.array(errors)

    return np.mean(errors), np.std(errors) #평균오차, 표준편차 반환


# ----------------------------------
# Phase 1 validation experiments
# ----------------------------------
def experiment_sigma_sweep():

    print("\n===== Sigma Sweep =====")

    sigmas = [0.001, 0.01, 0.05]

    for sigma in sigmas:
        mean_err, std_err = monte_carlo(
            trials=500,
            num_vectors=5,
            sigma=sigma
        )

        print(f"Sigma = {sigma}")
        print(f"Mean Error (deg): {mean_err:.6f}")
        print(f"Std  Error (deg): {std_err:.6f}")
        print("")


def experiment_vector_sweep():

    print("\n===== Vector Count Sweep =====")

    vector_counts = [2, 3, 5, 8]

    for N in vector_counts:
        mean_err, std_err = monte_carlo(
            trials=500,
            num_vectors=N,
            sigma=0.01
        )

        print(f"Vectors = {N}")
        print(f"Mean Error (deg): {mean_err:.6f}")
        print(f"Std  Error (deg): {std_err:.6f}")
        print("")


if __name__ == "__main__":

    experiment_sigma_sweep()
    experiment_vector_sweep()
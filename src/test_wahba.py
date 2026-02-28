import numpy as np
from wahba import solve_wahba
from quaternion import quat_to_rot


def main():
    # True rotation (z-axis 45 deg)
    theta = np.deg2rad(45)

    R_true = np.array([
        [np.cos(theta), -np.sin(theta), 0],
        [np.sin(theta),  np.cos(theta), 0],
        [0, 0, 1]
    ])

    # Generate inertial vectors
    r_vectors = np.random.randn(5, 3)
    r_vectors /= np.linalg.norm(r_vectors, axis=1, keepdims=True)

    # Rotate to body frame
    b_vectors = (R_true.T @ r_vectors.T).T
    
    # Solve Wahba
    q_est = solve_wahba(b_vectors, r_vectors)
    R_est = quat_to_rot(q_est)

    print("True R:")
    print(R_true)
    print("\nEstimated R:")
    print(R_est)

    print("\nError norm:")
    print(np.linalg.norm(R_true - R_est))

    print("\nCheck against transpose:")
    print("||R_true - R_est.T|| =", np.linalg.norm(R_true - R_est.T))
    print("||R_true.T - R_est|| =", np.linalg.norm(R_true.T - R_est))


if __name__ == "__main__":
    main()
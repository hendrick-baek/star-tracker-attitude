import numpy as np
from rotations import rodrigues
from quaternion import (
    normalize,
    conjugate,
    multiply,
    rotate_vector,
    quat_to_rot
)


def axis_angle_to_quat(axis: np.ndarray, theta: float) -> np.ndarray:
    axis = axis / np.linalg.norm(axis)
    w = np.cos(theta / 2)
    xyz = axis * np.sin(theta / 2)
    return np.concatenate(([w], xyz))


def main():
    axis = np.array([0, 0, 1])
    theta = np.deg2rad(45)

    q = axis_angle_to_quat(axis, theta)
    v = np.array([1, 0, 0])

    # Quaternion rotation
    v_q = rotate_vector(q, v)

    # Quaternion -> Matrix
    R_q = quat_to_rot(q)
    v_Rq = R_q @ v

    # Rodrigues
    R_rod = rodrigues(axis, theta)
    v_Rrod = R_rod @ v

    print("Quaternion rotation:", v_q)
    print("Quat->Matrix rotation:", v_Rq)
    print("Rodrigues rotation:", v_Rrod)

    print("\nDifferences:")
    print("q vs R(q):", np.linalg.norm(v_q - v_Rq))
    print("q vs Rodrigues:", np.linalg.norm(v_q - v_Rrod))
    
if __name__ == "__main__":
    main()
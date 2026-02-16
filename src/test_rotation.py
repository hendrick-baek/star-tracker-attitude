import numpy as np
from rotations import Rz, is_orthogonal, preserves_norm


def main():
    theta = np.deg2rad(45)
    R = Rz(theta)

    print("Rotation matrix R:")
    print(R)
    print()

    # Orthogonality check
    print("R^T R ≈ I:", is_orthogonal(R))
    print("R^T R:")
    print(R.T @ R)
    print()

    # Norm preservation test
    print("Testing norm preservation:")
    for i in range(5):
        v = np.random.randn(3)
        print(
            f"Test {i+1}:",
            preserves_norm(R, v)
        )


if __name__ == "__main__":
    main()

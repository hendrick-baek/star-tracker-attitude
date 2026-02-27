import numpy as np
from rotations import (
    Rz,
    is_orthogonal,
    preserves_norm,
    axis_angle_to_R,
    rodrigues
)


def test_day1():
    print("===== Day1: Z-axis Rotation Test =====")

    theta = np.deg2rad(45)
    R = Rz(theta)

    print("Orthogonal:", is_orthogonal(R))
    print("det(R):", np.linalg.det(R))

    print("Norm preservation:")
    for i in range(3):
        v = np.random.randn(3)
        print(f"Test {i+1}:", preserves_norm(R, v))

    print()


def test_day2():
    print("===== Day2: Axis-Angle (Rodrigues) Test =====")

    u = np.array([0.0, 0.0, 1.0])  # z-axis
    theta = np.deg2rad(45)

    R = axis_angle_to_R(u, theta)
    R_expected = Rz(theta)

    print("Orthogonal:", is_orthogonal(R))
    print("det(R):", np.linalg.det(R))

    print("Difference from Rz:",
          np.linalg.norm(R - R_expected))

    print()


def main():
    test_day1()
    test_day2()


if __name__ == "__main__":
    main()
import numpy as np


def build_B(b_vectors, r_vectors, weights=None):
    """
    Construct B matrix from vector observations.

    Parameters
    ----------
    b_vectors : (N,3) ndarray
        Body-frame unit vectors
    r_vectors : (N,3) ndarray
        Inertial-frame unit vectors
    weights : (N,) ndarray or None
        Optional weights

    Returns
    -------
    B : (3,3) ndarray
    """
    if weights is None:
        weights = np.ones(len(b_vectors)) #동일한 가중치로 설정 (가중치가 제공되지 않은 경우)

    B = np.zeros((3, 3)) #B 초기화

    for b, r, a in zip(b_vectors, r_vectors, weights): #zip()로 b, r, a를 동시에 순회
        B += a * np.outer(b, r) #B += a * np.outer(b, r) : B에 가중치 a를 곱한 b와 r의 외적을 누적하여 더함

    return B


def build_K(B):
    """
    Construct Davenport K matrix from B.
    """
    sigma = np.trace(B)
    S = B + B.T
# K = S - sigma * I
    z = np.array([
        B[1, 2] - B[2, 1],
        B[2, 0] - B[0, 2],
        B[0, 1] - B[1, 0]
    ])
# z 벡터는 B 행렬의 비대칭 부분에서 계산된 3차원 벡터로, B의 off-diagonal 요소들의 차이로 구성됨
    K = np.zeros((4, 4))

    K[0, 0] = sigma
    K[0, 1:] = z
    K[1:, 0] = z
    K[1:, 1:] = S - sigma * np.eye(3)
# K 행렬은 Davenport q-method에서 사용되는 4x4 대칭 행렬로, sigma는 B의 trace, S는 B와 B의 전치의 합, z는 B의 비대칭 부분에서 계산된 벡터를 이용하여 구성됨
    return K 


def solve_wahba(b_vectors, r_vectors, weights=None):
    """
    Solve Wahba problem using Davenport q-method.
    Returns optimal quaternion.
    """
    B = build_B(b_vectors, r_vectors, weights)
    K = build_K(B)

    eigvals, eigvecs = np.linalg.eigh(K) #K의 고유값과 고유벡터 계산 (eigh는 대칭 행렬에 최적화된 고유값 분해 함수)
    q_opt = eigvecs[:, np.argmax(eigvals)]

    # Normalize (just in case)
    q_opt = q_opt / np.linalg.norm(q_opt)

    return q_opt

from quaternion import quat_to_rot

def solve_wahba_rotation(b_vectors, r_vectors, weights=None):
    """
    Solve Wahba problem and return rotation matrix
    with project convention:

        b = R r

    Parameters
    ----------
    b_vectors : ndarray, shape (N, 3)
        Body-frame measured unit vectors
    r_vectors : ndarray, shape (N, 3)
        Inertial-frame reference unit vectors
    weights : ndarray, optional
        Weights for Wahba cost

    Returns
    -------
    R : ndarray, shape (3, 3)
        Rotation matrix from inertial frame to body frame
    """
    q_opt = solve_wahba(b_vectors, r_vectors, weights)
    R = quat_to_rot(q_opt).T
    return R

"""
Wahba Problem Solver (Davenport q-method)
=========================================

This module implements the Wahba attitude determination solution
using the Davenport q-method.

Project Rotation Convention
---------------------------
Throughout this project we use the following convention:

    b = R r

where

    r : inertial-frame unit vector
    b : body-frame (camera) unit vector
    R : rotation matrix from inertial frame -> body frame

Important Implementation Detail
-------------------------------
The core Wahba solver `solve_wahba()` returns the optimal quaternion
that maximizes the Wahba objective function using the Davenport
K-matrix eigenvalue method.

However, when converting this quaternion to a rotation matrix using

    quat_to_rot(q)

the resulting matrix corresponds to the opposite mapping relative to
the project convention. In practice, this means the rotation matrix
obtained from the quaternion is effectively the transpose of the
desired inertial -> body rotation.

This behavior originates from the quaternion-to-rotation conversion
convention used in `quat_to_rot()`.

As a result, the correct rotation matrix for this project must be

    R = quat_to_rot(q).T

Wrapper Function
----------------
To avoid scattering `.T` corrections throughout the codebase,
this module provides a wrapper:

    solve_wahba_rotation()

which internally performs

    q = solve_wahba(...)
    R = quat_to_rot(q).T

and directly returns the rotation matrix that satisfies the
project convention:

    b = R r

Recommended Usage
-----------------
For most attitude estimation tasks in this project, use:

    solve_wahba_rotation(...)

If the quaternion solution itself is needed (for analysis or debugging),
`solve_wahba()` can still be called directly.

Summary
-------
solve_wahba()          -> returns optimal quaternion
solve_wahba_rotation() -> returns rotation matrix (inertial -> body)

This design preserves the original solver while ensuring consistent
frame conventions across the project.
"""
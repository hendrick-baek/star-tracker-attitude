import numpy as np
from wahba import build_B
from quaternion import quat_to_rot


def solve_quest(b_vectors, r_vectors, weights=None, max_iter=50, tol=1e-12):
    """
    Solve Wahba problem using the QUEST algorithm.

    Returns optimal quaternion.

    Parameters
    ----------
    b_vectors : (N,3) ndarray
        Body-frame unit vectors
    r_vectors : (N,3) ndarray
        Inertial-frame unit vectors
    weights : (N,) ndarray or None
        Optional weights
    max_iter : int
        Maximum Newton iterations
    tol : float
        Convergence tolerance
    """

    if weights is None:
        weights = np.ones(len(b_vectors))

    # Construct B matrix
    B = build_B(b_vectors, r_vectors, weights)

    sigma = np.trace(B)
    S = B + B.T

    z = np.array([
        B[1,2] - B[2,1],
        B[2,0] - B[0,2],
        B[0,1] - B[1,0]
    ])

    # Initial eigenvalue estimate
    lambda_est = np.sum(weights)

    for _ in range(max_iter):

        M = (sigma + lambda_est) * np.eye(3) - S

        Minv = np.linalg.inv(M)

        f = np.dot(z, Minv @ z) - lambda_est + sigma

        dfdlambda = - np.dot(z, Minv @ Minv @ z) - 1

        lambda_new = lambda_est - f / dfdlambda

        if abs(lambda_new - lambda_est) < tol:
            lambda_est = lambda_new
            break

        lambda_est = lambda_new

    # Rodrigues parameter
    M = (sigma + lambda_est) * np.eye(3) - S
    p = np.linalg.inv(M) @ z

    # Quaternion reconstruction
    q = np.zeros(4)
    q[0] = 1.0
    q[1:] = p

    q = q / np.linalg.norm(q)

    return q


def solve_quest_rotation(b_vectors, r_vectors, weights=None):
    """
    QUEST solver returning rotation matrix.

    Convention:
        b = R r
    """

    q = solve_quest(b_vectors, r_vectors, weights)

    R = quat_to_rot(q).T

    return R
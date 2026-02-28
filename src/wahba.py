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
        weights = np.ones(len(b_vectors))

    B = np.zeros((3, 3))

    for b, r, a in zip(b_vectors, r_vectors, weights):
        B += a * np.outer(b, r)

    return B


def build_K(B):
    """
    Construct Davenport K matrix from B.
    """
    sigma = np.trace(B)
    S = B + B.T

    z = np.array([
        B[1, 2] - B[2, 1],
        B[2, 0] - B[0, 2],
        B[0, 1] - B[1, 0]
    ])

    K = np.zeros((4, 4))

    K[0, 0] = sigma
    K[0, 1:] = z
    K[1:, 0] = z
    K[1:, 1:] = S - sigma * np.eye(3)

    return K


def solve_wahba(b_vectors, r_vectors, weights=None):
    """
    Solve Wahba problem using Davenport q-method.
    Returns optimal quaternion.
    """
    B = build_B(b_vectors, r_vectors, weights)
    K = build_K(B)

    eigvals, eigvecs = np.linalg.eigh(K)
    q_opt = eigvecs[:, np.argmax(eigvals)]

    # Normalize (just in case)
    q_opt = q_opt / np.linalg.norm(q_opt)

    return q_opt
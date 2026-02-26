import numpy as np


def normalize(q: np.ndarray) -> np.ndarray:
    """Return unit quaternion."""
    return q / np.linalg.norm(q)


def conjugate(q: np.ndarray) -> np.ndarray:
    """Quaternion conjugate."""
    w, x, y, z = q
    return np.array([w, -x, -y, -z])
#q* = (w, -v) where q = (w, v)

def multiply(q1: np.ndarray, q2: np.ndarray) -> np.ndarray:
    """Quaternion multiplication q1 ⊗ q2."""
    w1, x1, y1, z1 = q1
    w2, x2, y2, z2 = q2

    return np.array([
        w1*w2 - x1*x2 - y1*y2 - z1*z2,
        w1*x2 + w2*x1 + y1*z2 - z1*y2,
        w1*y2 + w2*y1 + z1*x2 - x1*z2,
        w1*z2 + w2*z1 + x1*y2 - y1*x2
    ])
#쿼터니언 곱: q1 ⊗ q2 = (w1*w2 - v1·v2, w1*v2 + w2*v1 + v1×v2)
#첫줄: dot product 느낌(스칼라 부분)
#나머지 세줄: cross product 느낌(벡터 부분)

def rotate_vector(q: np.ndarray, v: np.ndarray) -> np.ndarray:
    """Rotate 3D vector v using quaternion q."""
    q = normalize(q)
    p = np.concatenate(([0.0], v)) #벡터 v를 순수 허수 쿼터니언 p로 변환 (w=0)
    q_conj = conjugate(q)

    p_rot = multiply(multiply(q, p), q_conj) #회전된 벡터 p_rot = q ⊗ p ⊗ q*
    return p_rot[1:]  # return vector part only


def quat_to_rot(q: np.ndarray) -> np.ndarray:
    """Convert unit quaternion to rotation matrix."""
    q = normalize(q)
    w, x, y, z = q

    R = np.array([
        [1 - 2*(y**2 + z**2), 2*(x*y - w*z),     2*(x*z + w*y)],
        [2*(x*y + w*z),       1 - 2*(x**2 + z**2), 2*(y*z - w*x)],
        [2*(x*z - w*y),       2*(y*z + w*x),     1 - 2*(x**2 + y**2)]
    ])

    return R
#쿼터니언에서 회전 행렬로 변환
#R @ v 와 rotate_vector(q, v)가 같은 결과를 낳도록 설계됨
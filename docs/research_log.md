# Research Log

---

## Day 1 – Rotation Matrix Foundations

### Goal
Understand the mathematical structure of 3D rotations and verify properties
required for attitude estimation.

### Theory Summary

A valid rotation matrix must satisfy:

R^T R = I 
det(R) = 1  

This ensures:

- Length preservation
- Angle preservation
- Orthogonality of column vectors
- Inverse equals transpose

### Implementation

Implemented:

- Z-axis rotation matrix function
- Orthogonality check
- Norm preservation check

### Numerical Verification

- R^T R ≈ I (within numerical tolerance)
- Norm preserved for multiple random vectors

### Insight

Rotation matrices form the group SO(3).  
This structure will later connect to quaternion representation and Wahba’s problem.

### Next Step

Study axis–angle representation and derive general rotation formula.

---

## Day 2 – Axis–Angle Representation & Rodrigues Formula

### Goal

Understand how a general 3D rotation can be represented
using a single rotation axis and angle, and implement
Rodrigues' rotation formula.

---

### Theory Summary

Any rotation in 3D (an element of SO(3)) can be expressed as:

- A unit rotation axis **u**
- A rotation angle **θ**

A vector **v** can be decomposed into:

- Parallel component to the axis  
- Perpendicular component to the axis  

Mathematically:

$$
v = v_{\parallel} + v_{\perp}
$$

where

$$
v_{\parallel} = (u \cdot v)u
$$

$$
v_{\perp} = v - v_{\parallel}
$$

The parallel component remains unchanged,
while the perpendicular component undergoes planar rotation.

---

### Rodrigues Formula (Vector Form)

The rotated vector is:

$$
v' = v\cos\theta + (u \times v)\sin\theta
+ u(u \cdot v)(1 - \cos\theta)
$$

Interpretation:

- \( v\cos\theta \) → original direction component  
- \( (u \times v)\sin\theta \) → 90° rotated component  
- \( u(u \cdot v)(1 - \cos\theta) \) → axis component preservation  

This structure mirrors the 2D rotation formula
extended into 3D using the cross product.

---

### Matrix Form

Define the skew-symmetric matrix of **u**:

$$
[u]_\times =
\begin{bmatrix}
0 & -u_z & u_y \\
u_z & 0 & -u_x \\
-u_y & u_x & 0
\end{bmatrix}
$$

Then Rodrigues’ rotation matrix becomes:

$$
R = I + \sin\theta [u]_\times
+ (1 - \cos\theta)[u]_\times^2
$$

This matrix satisfies:

$$
R^T R = I
$$

$$
\det(R) = 1
$$

Therefore:

$$
R \in SO(3)
$$

---

### Implementation

Implemented:

- `skew(u)`
- `axis_angle_to_R(u, theta)`

Numerically verified:

- \( R^T R \approx I \)
- \( \det(R) \approx 1 \)
- When \( u = [0,0,1] \), the result matches \( R_z(\theta) \)

---

### Insight

Rodrigues' formula provides a geometric construction
of any element in SO(3).

Even if a rotation is formed by multiple Euler rotations,
the final result can always be represented as a single
axis–angle rotation.

This establishes a deeper geometric understanding
of 3D rotations beyond coordinate-based representations.

---

### Next Step

Study quaternion representation and understand
why it is preferred in spacecraft attitude estimation.
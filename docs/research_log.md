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

Understand how any 3D rotation can be represented
as a single rotation axis and angle,
and implement Rodrigues' rotation formula.

---

### Theory Summary

Any rotation in 3D can be expressed using:

- A unit rotation axis u
- A rotation angle theta

A vector v can be decomposed into:

v = v_parallel + v_perp

where

v_parallel = (u · v) u  
v_perp = v - v_parallel

The parallel component remains unchanged.
The perpendicular component undergoes planar rotation.

---

### Rodrigues Formula (Vector Form)

The rotated vector is:

```text
v' = v cos(theta)
     + (u × v) sin(theta)
     + u (u · v) (1 - cos(theta))
```

Interpretation:

- v cos(theta) → original direction component
- (u × v) sin(theta) → 90-degree rotated component
- u (u · v)(1 - cos(theta)) → axis component preservation

This extends the 2D rotation formula into 3D space.

---

### Matrix Form

Define the skew-symmetric matrix of u:

```text
[u]_x =
[  0   -u_z   u_y
   u_z   0   -u_x
  -u_y   u_x    0 ]
```

Rodrigues rotation matrix:

```text
R = I
  + sin(theta) [u]_x
  + (1 - cos(theta)) [u]_x^2
```

Properties:

```text
R^T R = I
det(R) = 1
R ∈ SO(3)
```

---

### Implementation

Implemented:

- skew(u)
- axis_angle_to_R(u, theta)

Numerical verification:

- R^T R ≈ I
- det(R) ≈ 1
- When u = [0,0,1], result matches Rz(theta)

---

### Insight

Rodrigues' formula gives a geometric construction
of any rotation matrix in SO(3).

Even if a rotation is composed from multiple Euler rotations,
the final result can always be expressed
as a single axis–angle rotation.

This provides deeper geometric understanding
of 3D rotations beyond coordinate-based representations.

---

### Next Step

Study quaternion representation
and understand why it is preferred
in spacecraft attitude estimation.
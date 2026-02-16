# star-tracker-attitude
# Star Tracker Based 3-Axis Attitude Estimation

This project aims to implement and analyze attitude determination algorithms
for a star tracker system, starting from fundamental rotation theory.

---

## Day 1 – Rotation Fundamentals

### Objective
Establish a rigorous understanding of 3D rotation matrices and verify their
orthogonality and norm-preserving properties.

### Implemented

- Z-axis rotation matrix
- Orthogonality verification: \( R^T R = I \)
- Norm preservation test for arbitrary vectors
- Basic coordinate transformation: \( v^B = R v^I \)

### Key Mathematical Result

Rotation matrices satisfy:

\[
R^T R = I
\]

which implies:

\[
R^{-1} = R^T
\]

### Status

✔ Orthogonality verified numerically  
✔ Norm preservation verified for random vectors  

---

Next step: Axis–angle representation → quaternion formulation.

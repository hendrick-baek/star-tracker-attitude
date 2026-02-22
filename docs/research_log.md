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

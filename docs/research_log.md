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

---

## Day 3 – Quaternion Rotation and Its Equivalence to Rodrigues and Rotation Matrices

### Goal

Establish a deep understanding of quaternion-based rotation,
verify its equivalence to rotation matrices and Rodrigues’ formula,
and clarify conceptual misunderstandings encountered during implementation.

---

### 1. Fundamental Question

How can quaternion rotation, matrix rotation, and Rodrigues' formula
all represent the same 3D rotation if they seem structurally different?

---

### 2. Quaternion Representation of Rotation

A quaternion is defined as:

q = [w, x, y, z]

where:
- w is the scalar part
- (x, y, z) is the vector part

For rotation, we use **unit quaternions**:

w² + x² + y² + z² = 1

---

### 3. Embedding a 3D Vector

A 3D vector v is embedded into quaternion space as:

p = [0, v]

The zero scalar part is not arbitrary.
It defines the pure quaternion subspace,
which corresponds exactly to ℝ³.

---

### 4. Quaternion Rotation Formula

A vector is rotated using:

p' = q p q*

where:
q* = [w, -x, -y, -z]

For unit quaternions:

q⁻¹ = q*

Thus, quaternion rotation is a conjugation operation:

p' = q p q⁻¹

This structure ensures:
- Norm preservation
- Pure vector result (scalar part returns to zero)
- Proper 3D rotation

---

### 5. Quaternion Multiplication

Given:

q1 = [w1, v1]
q2 = [w2, v2]

Their product is:

q1 ⊗ q2 =
[
  w1w2 − v1·v2,
  w1v2 + w2v1 + v1 × v2
]

Key insight:

Quaternion multiplication naturally contains:
- Dot product
- Cross product

The cross product term explains why quaternion algebra encodes 3D rotational structure.

---

### 6. Quaternion to Rotation Matrix

For a unit quaternion:

q = [w, x, y, z]

The equivalent rotation matrix is:

R(q) =
[ 1 − 2(y² + z²)   2(xy − wz)      2(xz + wy)
  2(xy + wz)       1 − 2(x² + z²)  2(yz − wx)
  2(xz − wy)       2(yz + wx)      1 − 2(x² + y²) ]

Structural form:

Let v = [x, y, z]

R(q) =
(w² − v·v) I
+ 2 v vᵀ
+ 2 w [v]_×

where [v]_× is the skew-symmetric matrix.

---

### 7. Rodrigues’ Formula

Rodrigues’ rotation matrix is given by:

R = I
  + sinθ [u]_×
  + (1 − cosθ)[u]_×²

where:
- u is the unit rotation axis
- θ is the rotation angle

Using:

w = cos(θ/2)
v = u sin(θ/2)

The quaternion-derived matrix reduces exactly to Rodrigues’ formula.

Thus:

Quaternion rotation = Rodrigues rotation = Rotation matrix

They are mathematically equivalent representations of SO(3).

---

### 8. Practical Code Verification

Three independent implementations were tested:

1) Quaternion rotation (q v q*)
2) Quaternion → Rotation matrix → R v
3) Rodrigues formula → R v

For a 45° rotation about the z-axis:

Quaternion rotation:      [0.70710678 0.70710678 0.        ]
Quat->Matrix rotation:    [0.70710678 0.70710678 0.        ]
Rodrigues rotation:       [0.70710678 0.70710678 0.        ]

Differences:
q vs R(q):        0.0
q vs Rodrigues:   1.57e-16

The small numerical discrepancy (~1e-16) is due to floating-point precision.

Conclusion:

All three formulations produce identical 3D rotations.

---

### 9. Clarified Conceptual Confusions

#### Q1. Is Rodrigues 3D?

Yes.

Rodrigues directly constructs a 3×3 rotation matrix in ℝ³.

Quaternion does not replace Rodrigues.
It provides a different algebraic representation of the same 3D rotation group.

---

#### Q2. Why embed vectors into 4D quaternion space?

Quaternion multiplication is defined only between quaternions.

Embedding allows 3D vectors to participate in quaternion algebra.

The scalar zero enforces pure vector structure.

---

#### Q3. Why multiply by q*?

Because conjugation:

q p q⁻¹

is the quaternion analogue of similarity transformation.

It ensures:
- Scalar part vanishes
- Only rotated vector remains

---

#### Q4. Why is q⁻¹ = q*?

For unit quaternion:

q q* = w² + |v|² = 1

Therefore:

q⁻¹ = q*

This guarantees proper rotation behavior.

---

#### Q5. Why use skew matrices?

Because cross products define the rotation plane.

Skew-symmetric matrices allow writing:

u × v = [u]_× v

This connects quaternion algebra to linear matrix form.

---

#### Q6. Why do q and −q represent the same rotation?

Because:

(-q) p (-q)* = q p q*

The negative signs cancel.

Thus S³ is a double cover of SO(3).

---

### 10. Key Insight from Day 3

Quaternion rotation,
Rodrigues’ formula,
and rotation matrices

are not different rotations.

They are different representations of the same mathematical object:

SO(3), the 3D rotation group.

Quaternion uses 4D algebra (S³),
while Rodrigues and matrices operate directly in ℝ³.

All produce identical physical rotations.

---

### Conclusion

Day 3 established:

- Quaternion algebra structure
- Conjugation-based rotation
- Equivalence to Rodrigues
- Equivalence to rotation matrices
- Double-cover property
- Numerical verification through code

This completes the mathematical foundation required
for moving into Wahba’s problem and QUEST implementation.

---

## Day 4 – Wahba’s Problem and Davenport q-Method

### Goal

Understand the full mathematical structure of attitude estimation and implement
a numerically verified solution to Wahba’s problem.

---

### 1. Problem Formulation

Given vector pairs:

- Inertial frame vectors r_i
- Body frame measurements b_i

Ideal relationship:

b_i = R r_i

Due to noise, exact equality does not hold.

Wahba’s problem:

minimize  Σ a_i || b_i - R r_i ||^2
subject to R ∈ SO(3)

---

### 2. From Error Minimization to Alignment Maximization

Expanding the squared norm leads to:

maximize  Σ a_i b_i^T R r_i

Interpretation:

- b_i^T R r_i equals cosine of alignment angle
- The objective becomes total alignment score

Thus:

Wahba = Find rotation that maximizes total vector alignment.

---

### 3. Matrix Reformulation

Define:

B = Σ a_i b_i r_i^T

Then objective becomes:

maximize  trace(R B^T)

Key insight:

- B compresses all measurement information
- All vector pairs are summarized into a single 3×3 matrix

---

### 4. Re-parameterization: From R to Quaternion

Direct optimization over R is difficult because:

- R^T R = I
- det(R) = 1

Instead, use quaternion representation:

R = R(q),  with  ||q|| = 1

Important realization:

The unknown did not change.
Only the parameterization changed to simplify constraints.

---

### 5. Quadratic Form Reduction

Substituting quaternion representation yields:

trace(R(q) B^T) = q^T K q

Where K is defined as:

K =
[  σ        z^T  ]
[  z   S - σ I  ]

with

σ = trace(B)
S = B + B^T
z = skew part extracted from B

This transforms Wahba into:

maximize  q^T K q
subject to  ||q|| = 1

---

### 6. Rayleigh Quotient Interpretation

For symmetric K:

maximize  q^T K q   with  ||q|| = 1

Solution:

The eigenvector corresponding to the largest eigenvalue of K.

Interpretation:

- K encodes measurement geometry
- Largest eigenvector = rotation most strongly supported by data
- Largest eigenvalue = maximum alignment score

---

### 7. Conceptual Insights Gained

#### (1) Meaning of the Score

q^T K q represents total weighted alignment between
rotated inertial vectors and body measurements.

Maximizing eigenvalue = minimizing geometric misalignment.

---

#### (2) Why Quaternion Simplifies Optimization

SO(3) has nonlinear orthogonality constraints.

Quaternion only requires:

||q|| = 1

Thus nonlinear constrained optimization becomes
a unit-sphere eigenvalue problem.

---

#### (3) Frame Convention Issue (Important)

During implementation, transpose ambiguity appeared.

If:

b = R r

versus

r = R b

the estimated rotation may appear as R^T.

Key realization:

R^{-1} = R^T

Transpose does not indicate algorithm failure,
only difference in frame interpretation.

---

#### (4) Rotation Error Metric

Angular difference between two rotations:

θ = arccos( ( trace(R_true^T R_est) - 1 ) / 2 )

This follows from:

trace(R) = 1 + 2 cos(θ)

Thus trace directly encodes rotation angle.

---

### 8. Numerical Verification

Procedure:

1. Generate random unit inertial vectors
2. Apply known rotation
3. Solve Wahba via Davenport q-method
4. Convert quaternion to rotation matrix
5. Compare with ground truth

Result:

|| R_true - R_est || ≈ 1e-16

Confirms correctness in noise-free condition.

---

### 9. Milestones Achieved

- Full understanding of Wahba structure
- Clear interpretation of alignment score
- Connection between geometry and eigenvalue theory
- Clarified frame-direction ambiguity
- Implemented and validated Davenport solution

---

### Next Step

Introduce Gaussian noise and evaluate:

- Angular estimation error
- Sensitivity to number of vectors
- Eigenvalue gap behavior

Transition from theoretical validation to performance analysis.

---
## Day 5 – Noise Robustness Validation of Wahba / QUEST

### Goal

Validate the robustness of the implemented Wahba / Davenport q-method
under realistic noisy measurements and complete Phase 1 verification.

---

### Motivation

Until Day 4, all experiments were performed in a noise-free setting.
In that case, the estimator perfectly recovers the true rotation.

However, real star tracker measurements always contain noise.

Thus, the key question becomes:

How does the estimation error behave under noisy measurements?

This marks the transition from pure mathematical correctness
to practical algorithm robustness.

---

### Noise Model

Given ideal body-frame measurements:

b_i = R_true r_i

Gaussian noise is injected:

b_i_noisy = b_i + σ n_i  
where n_i ~ N(0, I)

Since star tracker measurements represent directions,
all vectors must remain unit vectors.

Therefore normalization is applied:

b_i_noisy ← b_i_noisy / ||b_i_noisy||

This preserves physical consistency of directional measurements.

---

### Rotation Error Definition

To quantify estimation performance,
the angular difference between the true rotation
and the estimated rotation is computed.

Define the relative rotation:

R_err = R_true^T R_est

Using the identity:

trace(R) = 1 + 2 cosθ

The rotation error angle is:

θ = arccos((trace(R_err) - 1) / 2)

The final reported metric is in degrees.

This provides a physically interpretable performance measure.

---

### Monte Carlo Structure

A single trial consists of:

1. Generate N random inertial unit vectors
2. Apply true rotation (30° about z-axis)
3. Inject Gaussian noise
4. Estimate rotation via Wahba / q-method
5. Compute angular error

To obtain statistical performance,
the trial is repeated 500 times.

Performance metrics:

- Mean angular error
- Standard deviation of angular error

---

### Experiment 1 – Sigma Sweep

Vectors fixed at N = 5.

Sigma values tested:

0.001  
0.01  
0.05  

Results:

Sigma = 0.001  
Mean Error ≈ 0.053 deg  
Std  Error ≈ 0.023 deg  

Sigma = 0.01  
Mean Error ≈ 0.536 deg  
Std  Error ≈ 0.253 deg  

Sigma = 0.05  
Mean Error ≈ 2.727 deg  
Std  Error ≈ 1.167 deg  

Observation:

- Estimation error increases with measurement noise.
- Standard deviation also increases.
- Behavior is smooth and physically consistent.

This confirms correct estimator implementation.

---

### Experiment 2 – Vector Count Sweep

Sigma fixed at 0.01.

Vector counts tested:

2  
3  
5  
8  

Results:

N = 2  
Mean Error ≈ 1.245 deg  
Std  Error ≈ 2.120 deg  

N = 3  
Mean Error ≈ 0.755 deg  
Std  Error ≈ 0.401 deg  

N = 5  
Mean Error ≈ 0.534 deg  
Std  Error ≈ 0.236 deg  

N = 8  
Mean Error ≈ 0.403 deg  
Std  Error ≈ 0.168 deg  

Observation:

- Increasing vector count reduces mean error.
- Standard deviation significantly decreases.
- Two-vector case shows instability and high variance.

This confirms the expected averaging effect
of multiple independent measurements.

---

### Critical Debug Insight

During implementation, a frame-convention mismatch was discovered.

Initial experiments yielded ~60° constant error,
indicating reversed argument ordering in Wahba solver.

Correcting the inertial/body vector ordering
resolved the issue and restored near-zero error in the low-noise regime.

This validated correct frame interpretation.

---

### Phase 1 Conclusion

At this stage:

- SO(3) structure understood
- Rodrigues formula implemented
- Quaternion representation verified
- Wahba cost reformulated to eigenvalue problem
- Davenport q-method implemented
- Frame convention validated
- Noise robustness experimentally verified

Phase 1 is complete.

The estimator is mathematically correct,
numerically stable,
and robust under realistic measurement noise.

---

### Next Step

Transition to Phase 2:

Star Tracker Geometry Modeling

- Field-of-view modeling
- Sensor geometry
- Realistic star distribution
- Image-to-vector mapping

Move from abstract vector pairs
to physically modeled sensor measurements.

---
## Day 6 – Star Tracker Field-of-View Geometry and Frame Consistency

### Goal

Establish a geometrically consistent sensor model for the star tracker,
define frame conventions rigorously,
and derive the mathematical structure of the field-of-view (FOV) condition.

This marks the formal beginning of Phase 2:
transitioning from abstract vector pairs to physically modeled measurements.

---

## 1. Frame Convention (Project-Wide Fixation)

To eliminate ambiguity in all subsequent derivations,
the rotation convention is fixed as:

b = R r

where:

- r : inertial-frame unit vector (true star direction)
- b : body/camera-frame unit vector
- R : rotation from inertial frame to body frame

Thus:

- R maps inertial vectors into the camera coordinate system
- R^T maps body vectors back into inertial space

This convention will be maintained throughout Phase 2–6.

---

## 2. Camera Boresight Definition

The camera boresight (optical axis) is defined in body frame as:

c = [0, 0, 1]^T

Interpretation:

- The camera looks along its +z axis
- x and y axes span the image plane
- c is fixed in the body frame

---

## 3. Field-of-View Geometry

A star is visible only if its direction lies inside the FOV cone.

Let θ_fov denote the half-angle of the conical FOV.

In body frame, the visibility condition is:

angle(b, c) ≤ θ_fov

Using the dot product identity for unit vectors:

b · c = cos(angle)

The FOV condition becomes:

b · c ≥ cos(θ_fov)

This converts an angular constraint into a simple inner-product threshold.

---

## 4. Equivalent Inertial-Frame Expression

Since:

b = R r

the FOV condition can be rewritten:

(R r) · c ≥ cos(θ_fov)

Using inner-product symmetry:

r · (R^T c) ≥ cos(θ_fov)

Interpretation:

- R^T c is the boresight direction expressed in inertial frame.
- Thus visibility may equivalently be tested in inertial coordinates.

This confirms complete frame consistency.

---

## 5. Geometric Interpretation

The FOV condition defines a cone in body space.

On the unit sphere of directions,
this corresponds to a **spherical cap** centered at c.

Thus:

- All unit vectors lie on the unit sphere
- The FOV selects a spherical cap of angular radius θ_fov
- The visible star set depends entirely on spacecraft attitude R

---

## 6. Rotation Axis Insight

A critical geometric observation:

If the spacecraft rotates about the boresight axis (z-axis),
the boresight direction remains unchanged.

Therefore:

- The spherical cap does not move in inertial space
- The visible star set remains unchanged
- Only image orientation rotates

However, rotation about any axis perpendicular to the boresight
tilts the cone and changes the visible star set.

This distinction is essential for later sensitivity analysis.

---

## 7. Phase 2 Structural Model (Established)

The complete sensor model structure is now defined:

1. Generate inertial star directions r_i
2. Apply spacecraft attitude: b_i = R_true r_i
3. Apply FOV filter: b_i · c ≥ cos(θ_fov)
4. Add measurement noise and renormalize
5. Output measurement set {r_i, b_i_meas}

Unlike Phase 1, the number of usable vectors
is now determined by FOV geometry,
not arbitrarily fixed.

---

## Day 6 Conclusion

The star tracker sensor model geometry is now fully defined.

Key achievements:

- Frame convention rigorously fixed
- FOV condition derived and interpreted
- Inertial/body equivalence proven
- Spherical cap geometry established
- Rotation-axis effects understood

Phase 2 can now proceed to statistical visibility analysis
and realistic star-density modeling.
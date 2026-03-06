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

---
## Day 7 – Star Density Modeling and Expected Visible Star Count

### Goal

Understand how the star tracker field-of-view (FOV) geometry determines the
expected number of visible stars, and validate this relationship through
simulation.

This step connects the geometric FOV model established in Day 6 with the
statistical properties of the observable star field.

---

## 1. Problem Motivation

The star tracker does not observe the entire sky.

Instead, it observes only a limited conical region defined by the sensor FOV.

Thus the number of observable stars depends on two factors:

1. Total star density in the sky
2. Fraction of the sky covered by the FOV

Understanding this relationship is essential because the number of available
vector measurements directly affects the stability and accuracy of attitude
estimation algorithms such as QUEST.

---

## 2. Isotropic Star Distribution Model

As a first-order approximation, the star field is modeled as an isotropic
distribution on the unit sphere.

This means:

- Star directions are uniformly distributed over the sphere
- Every direction in space has equal probability

Mathematically, this corresponds to sampling random unit vectors:

v ~ Uniform(S²)

where S² denotes the surface of the unit sphere.

This assumption simplifies the analysis and provides a useful baseline model
before introducing realistic star catalog distributions.

---

## 3. Total Surface Area of the Unit Sphere

The surface area of the unit sphere is:

A_sphere = 4π

This represents the total angular domain of all possible star directions.

---

## 4. Spherical Cap Area (Field-of-View Region)

The FOV cone corresponds to a **spherical cap** on the unit sphere.

For an FOV half-angle θ_fov, the spherical cap area is:

A_cap = 2π (1 − cos θ_fov)

This region contains all star directions satisfying:

b · c ≥ cos θ_fov

where:

b = body-frame star direction  
c = camera boresight direction

---

## 5. Fraction of the Sky Visible

The fraction of the sky visible inside the FOV is therefore:

fraction_visible = A_cap / A_sphere

Substituting the sphere and cap areas:

fraction_visible = (1 − cos θ_fov) / 2

This equation directly relates the sensor FOV angle to the probability that a
random star lies inside the visible region.

---

## 6. Expected Number of Visible Stars

If the sky contains N_total stars, the expected number inside the FOV is:

N_visible = N_total * (1 − cos θ_fov) / 2

This equation provides a theoretical prediction that can be verified using
Monte Carlo simulation.

---

## 7. Numerical Simulation of Visible Star Fraction

A Monte Carlo simulation was performed using randomly generated unit vectors
distributed uniformly on the sphere.

The procedure was:

1. Generate a large number of random unit vectors
2. Apply the FOV condition

   b · c ≥ cos θ_fov

3. Count the number of vectors satisfying the condition
4. Compare the observed fraction with the theoretical prediction

Example results:

FOV = 10°  
theory fraction = 0.007596  
observed fraction = 0.007490  

FOV = 20°  
theory fraction = 0.030154  
observed fraction = 0.030320  

FOV = 40°  
theory fraction = 0.116978  
observed fraction = 0.117235  

FOV = 60°  
theory fraction = 0.250000  
observed fraction = 0.248055  

The observed fractions closely match the theoretical values, confirming that
the spherical-cap FOV model has been implemented correctly.

---

## 8. Introducing Sensor Detectability (Magnitude Cut)

In practice, not every star inside the FOV is observable.

Stars must also be bright enough to be detected by the camera sensor.

This introduces a **magnitude threshold**:

m ≤ m_lim

where:

m = star magnitude  
m_lim = sensor detection limit

Stars with magnitude larger than this threshold are too dim to be detected.

---

## 9. Magnitude-Based Filtering Model

Each simulated star was assigned a magnitude sampled from a uniform range.

The visibility pipeline became:

1. Generate isotropic star directions
2. Apply FOV geometric filter
3. Apply magnitude detection threshold

Only stars satisfying both conditions remain in the observable set.

Example results:

FOV = 20°  

m_lim = 2.0 → visible stars ≈ 1470  
m_lim = 4.0 → visible stars ≈ 2940  
m_lim = 6.0 → visible stars ≈ 4451  
m_lim = 8.0 → visible stars ≈ 5997  

As expected, increasing the magnitude limit increases the number of visible
stars.

---

## 10. Key Insights

Several important insights emerged from this analysis.

First, the number of observable stars grows nonlinearly with the FOV angle
because the spherical cap area depends on cos θ.

Second, the magnitude threshold acts as an independent visibility filter,
reducing the effective number of usable vectors.

Finally, the full sensor measurement process can now be modeled as a pipeline:

1. Generate inertial star vectors r_i
2. Apply spacecraft attitude: b_i = R_true r_i
3. Apply FOV constraint
4. Apply magnitude detection threshold
5. Add measurement noise

The resulting vector pairs form the input to the Wahba / QUEST attitude
estimation algorithms.

---

## Day 7 Conclusion

The relationship between FOV geometry and observable star count has been
successfully derived and validated.

Key achievements:

- Derived spherical-cap FOV visibility fraction
- Verified theoretical predictions using Monte Carlo simulation
- Implemented magnitude-based detectability filtering
- Established a complete sensor visibility pipeline

This completes the geometric and statistical foundation required for
realistic star tracker measurement simulation.

---

## Next Step

Extend the sensor model to generate full measurement pairs:

r_i (inertial vectors)  
b_i = R_true r_i (body-frame measurements)

with FOV filtering, magnitude detection, and measurement noise.

This will produce realistic inputs for attitude estimation algorithms such as
Wahba’s problem and QUEST.

---
## Day 8 – Full Star Tracker Measurement Simulation Pipeline

### Goal

Construct a complete simulation pipeline that generates realistic star tracker
measurements for attitude estimation experiments.

This step connects the star field model developed in previous days with the
attitude estimation framework used in Wahba’s problem and QUEST.

---

## 1. Motivation

In real spacecraft systems, star trackers do not directly provide attitude.
Instead, they measure directions of stars in the camera frame.

Attitude estimation algorithms must reconstruct the spacecraft orientation from
these measurements.

Therefore a realistic simulation must generate measurement pairs:

r_i : inertial reference star directions  
b_i : measured star directions in the body frame

These vector pairs form the input to Wahba’s problem.

---

## 2. Measurement Generation Pipeline

The full simulation pipeline consists of the following stages.

1. Generate inertial star directions  
2. Apply spacecraft rotation  
3. Apply camera field-of-view constraint  
4. Apply magnitude detection threshold  
5. Add sensor measurement noise  

This sequence models the complete sensing process of a star tracker.

---

## 3. Inertial Star Vector Generation

Stars are first modeled as random unit vectors distributed uniformly over the
sphere.

Mathematically:

r_i ∈ S²

This represents an isotropic approximation of the star field.

---

## 4. Spacecraft Attitude Transformation

A known spacecraft rotation R_true is applied to transform inertial star
directions into the body frame.

b_i_true = R_true r_i

This represents the ideal noiseless star tracker observation.

---

## 5. Field-of-View Filtering

The star tracker can only observe stars within its camera field-of-view.

Using the camera boresight vector c:

b_i · c ≥ cos(θ_fov)

This condition defines a conical region in the body frame.

Only stars inside this cone remain visible.

---

## 6. Magnitude-Based Detection

Even if a star lies within the FOV, it may still be too dim to detect.

A magnitude threshold is introduced:

m ≤ m_lim

Stars exceeding this threshold are removed from the observable set.

This models the sensitivity limit of the optical sensor.

---

## 7. Measurement Noise Model

Real sensors contain measurement noise.

Noise is modeled as a small Gaussian perturbation applied to the direction
vector.

b_meas = normalize( b_true + noise )

This produces the final measurement vectors used by the estimation algorithm.

---

## 8. Final Output

The simulation outputs vector pairs:

{ r_i , b_i_meas }

These pairs form the direct input to Wahba’s attitude estimation problem.

---

## 9. Key Insight

The simulator now reproduces the full sensing pipeline of a star tracker:

star field  
→ spacecraft rotation  
→ camera field-of-view  
→ brightness detection  
→ sensor noise  

This provides realistic measurement data for evaluating attitude estimation
algorithms such as QUEST.

---

## Next Step

Connect the measurement simulator to the QUEST estimator and evaluate the
attitude estimation error.

---
## Day 9 – Attitude Estimation Using the Davenport q-Method with Simulated Star Tracker Measurements

### Goal

Integrate the star tracker measurement simulator with a Wahba-based
attitude estimation algorithm and evaluate the resulting attitude
estimation error.

This step completes the first fully functional attitude determination pipeline.

---

## 1. Motivation

A star tracker does not directly output spacecraft attitude.

Instead, it measures the directions of stars in the camera frame.
These measurements must be combined with known inertial star directions
to estimate the spacecraft orientation.

This estimation problem is known as **Wahba’s problem**.

The objective is to find the rotation matrix R that best aligns
inertial reference vectors with measured body-frame vectors.

---

## 2. Measurement Inputs

The simulator developed in previous days generates measurement pairs:

r_i : inertial star directions  
b_i : measured body-frame directions

These vectors satisfy the relationship:

b_i ≈ R_true r_i

where R_true represents the true spacecraft attitude.

Due to sensor noise and filtering effects, the relationship is not exact,
making this a least-squares estimation problem.

---

## 3. Wahba’s Problem

The estimation problem can be written as:

minimize

Σ a_i || b_i − R r_i ||²

subject to

R ∈ SO(3)

where a_i are weighting coefficients.

The goal is to find the rotation matrix that minimizes the misalignment
between predicted and measured star directions.

---

## 4. Davenport q-Method

Instead of solving the optimization directly over rotation matrices,
the problem is reformulated using quaternion parameterization.

This leads to the quadratic form:

maximize

qᵀ K q

subject to

||q|| = 1

where K is a symmetric matrix constructed from the vector pairs.

The optimal solution is the eigenvector corresponding to the
largest eigenvalue of K.

This method is known as the **Davenport q-method**, which provides
an efficient closed-form solution to Wahba’s problem.

The QUEST algorithm, introduced later, solves the same Wahba problem
using a different numerical strategy based on Newton iteration
to estimate the maximum eigenvalue.

---

## 5. Attitude Error Metric

To evaluate the estimation accuracy, the angular difference between
the true rotation and the estimated rotation is computed.

Given:

R_true  
R_est

the rotation error angle is defined as:

θ = arccos( ( trace(R_trueᵀ R_est) − 1 ) / 2 )

This value represents the smallest rotation angle required
to align the estimated orientation with the true orientation.

---

## 6. Simulation Procedure

The following simulation pipeline was executed:

1. Generate random inertial star vectors  
2. Apply known spacecraft rotation R_true  
3. Apply FOV filtering  
4. Apply magnitude detection threshold  
5. Add Gaussian measurement noise  
6. Solve Wahba’s problem using the Davenport q-method  
7. Convert quaternion solution to rotation matrix  
8. Compute attitude estimation error

---

## 7. Numerical Result

Example output from the simulation:

Visible stars: 463

Attitude Error ≈ 0.0035 degrees

The estimated rotation matrix closely matches the true rotation matrix.

The difference between elements is on the order of 10⁻⁵,
which is consistent with the injected measurement noise.

---

## 8. Interpretation of Results

The small attitude error confirms that the full pipeline is functioning
correctly.

Key observations:

- The Davenport-based Wahba estimator successfully reconstructs
  spacecraft attitude from noisy star measurements.

- The estimation accuracy depends on the measurement noise level
  and the number of available star vectors.

- The simulator now produces realistic measurement conditions
  similar to those encountered by real star tracker systems.

---

## 9. System Architecture Achieved

At this stage the simulation system contains three main components:

Star field model  
→ Star tracker sensor model  
→ Wahba-based attitude estimation algorithm

This modular structure mirrors the architecture used in
actual spacecraft attitude determination research.

---

## Day 9 Conclusion

The complete star tracker attitude estimation pipeline has been
successfully implemented and validated.

The system now performs:

star field simulation  
→ spacecraft attitude transformation  
→ sensor measurement modeling  
→ Wahba attitude estimation (Davenport q-method)  
→ estimation error evaluation

This marks the completion of the first full attitude determination
simulation framework.

---

## Next Step

Introduce additional attitude estimation algorithms such as
TRIAD and QUEST, and perform Monte Carlo experiments to analyze
the relationship between:

measurement noise  
number of observed stars  
field-of-view size  

and the resulting attitude estimation accuracy.

This will enable systematic comparison between simple geometric
estimators and optimal Wahba-based solutions.

---
## Day 10 – TRIAD Attitude Determination Baseline

### Goal

Implement the TRIAD attitude determination algorithm and integrate it into the existing star tracker simulation pipeline.

The objective of this step is to introduce a simple baseline estimator that uses only two vector observations, and compare its behavior with the existing Wahba/Davenport-based optimal estimator.

This prepares the system for future Monte Carlo performance analysis between simple geometric attitude determination (TRIAD) and optimal Wahba-based solutions.

---

### 1. Motivation

Until Day 9, the complete pipeline consisted of:

1. Star field generation
2. Star tracker measurement simulation
3. Attitude estimation using the Wahba problem solved via the Davenport q-method

This pipeline already demonstrated that the simulated measurements could be used to recover spacecraft attitude with high accuracy.

However, the current estimator uses **all available star observations** and solves a global optimization problem.  
To properly evaluate estimator performance, it is useful to introduce a **simpler baseline algorithm**.

TRIAD is commonly used for this purpose because:

- It requires only **two vector observations**
- It has **very low computational cost**
- It directly constructs the rotation matrix geometrically
- It is widely used as an initialization or baseline method in spacecraft attitude determination

Therefore, TRIAD is implemented as the first comparison estimator before performing Monte Carlo experiments.

---

### 2. TRIAD Algorithm Overview

Assume two corresponding vector observations:

r1, r2 : inertial frame unit vectors  
b1, b2 : body frame unit vectors

The project rotation convention is

b = R r

where R is the rotation from inertial frame to body frame.

The TRIAD algorithm constructs orthonormal bases (triads) in both frames.

#### Inertial Frame Triad

t1_r = r1  
t2_r = normalize(r1 × r2)  
t3_r = t1_r × t2_r

These vectors form an orthonormal basis

T_r = [ t1_r  t2_r  t3_r ]

#### Body Frame Triad

t1_b = b1  
t2_b = normalize(b1 × b2)  
t3_b = t1_b × t2_b

which forms

T_b = [ t1_b  t2_b  t3_b ]

#### Rotation Matrix

The rotation from inertial to body frame is

R = T_b T_r^T

This rotation satisfies the project convention

b = R r

---

### 3. Implementation

A new module was added:

src/triad.py

Core function:

solve_triad(r1, r2, b1, b2)

Input:
- two inertial reference vectors
- two body-frame measurements

Output:
- rotation matrix R (inertial → body)

Important implementation details:

- All vectors are normalized
- Cross product magnitude is checked to avoid nearly parallel vectors
- Triad basis vectors are stacked as matrix columns

---

### 4. Integration with Star Tracker Simulation

The existing star tracker pipeline already outputs:

r_visible : inertial-frame star directions  
b_meas : body-frame measured directions (with noise)

Since TRIAD requires only two vector pairs, the first two visible stars are selected:

r1 = r_visible[0]  
r2 = r_visible[1]

b1 = b_meas[0]  
b2 = b_meas[1]

These vectors are passed to:

solve_triad()

which returns the TRIAD attitude estimate.

---

### 5. Wahba/Davenport Solver Convention Issue

During integration, a frame convention mismatch appeared.

The Wahba solver (`solve_wahba`) returns the optimal quaternion obtained from the Davenport K-matrix eigenvalue solution.

When converted to a rotation matrix using

quat_to_rot(q)

the resulting matrix corresponds to the opposite mapping relative to the project convention.

Therefore the correct inertial → body rotation must be

R = quat_to_rot(q)^T

To prevent this transpose from appearing throughout the codebase, a wrapper function was introduced.

New function:

solve_wahba_rotation(b_vectors, r_vectors)

which performs:

q = solve_wahba(...)  
R = quat_to_rot(q).T

This wrapper ensures all returned rotation matrices satisfy the project convention

b = R r

while preserving the original quaternion-based solver.

---

### 6. Experimental Test

The TRIAD estimator and the Davenport/Wahba estimator were tested using the same simulated measurements.

Example output:

Visible stars: 72

TRIAD Attitude Error ≈ 0.44 deg  
Davenport/Wahba Attitude Error ≈ 0.026 deg

---

### 7. Interpretation

The result matches the expected behavior of the two algorithms.

TRIAD:

- Uses only two vector observations
- Does not average measurement noise
- Therefore produces larger attitude error

Davenport/Wahba:

- Uses all visible stars
- Solves a global optimal alignment problem
- Achieves significantly smaller error

This confirms that the simulation pipeline and both estimators are functioning correctly.

---

### Conclusion

Day 10 successfully introduced a geometric baseline estimator (TRIAD) into the star tracker attitude determination pipeline.

The system now supports two attitude estimation methods:

TRIAD (two-vector geometric solution)  
Davenport/Wahba (optimal multi-vector solution)

This enables meaningful performance comparisons in future experiments.

---

### Next Step

The next phase will perform **Monte Carlo performance analysis** comparing:

TRIAD vs Davenport/Wahba

under varying conditions such as:

- measurement noise level
- number of visible stars

This will provide quantitative insight into the robustness and accuracy differences between simple geometric and optimal attitude estimation methods.

---
## Day 11 – QUEST Algorithm Implementation and Verification

### Goal

Implement the QUEST (QUaternion ESTimator) algorithm and verify that it
produces the same optimal attitude estimate as the previously implemented
Davenport q-method.

This step completes the implementation of two optimal Wahba solvers and
establishes the final estimator set used in subsequent Monte Carlo
performance analysis.

---

## 1. Motivation

By Day 9, the star tracker measurement simulator had been successfully
connected to an attitude estimation algorithm based on Wahba’s problem,
solved using the Davenport q-method.

Although the Davenport approach is mathematically straightforward,
it requires computing the eigenvalues and eigenvectors of a 4×4 matrix.

In practical spacecraft systems, particularly early onboard computers,
full eigenvalue decomposition can be computationally expensive.

The QUEST algorithm was introduced to solve the same Wahba problem
more efficiently by avoiding explicit eigenvalue decomposition.

Instead, QUEST estimates the maximum eigenvalue using a scalar
root-finding method and reconstructs the optimal quaternion afterward.

Thus, QUEST provides a computationally efficient alternative to
Davenport’s method while producing the same optimal attitude solution.

---

## 2. Relationship Between Wahba, Davenport, and QUEST

Both Davenport and QUEST solve the same Wahba optimization problem.

Wahba problem:

minimize

Σ a_i || b_i − R r_i ||²

subject to

R ∈ SO(3)

Using quaternion parameterization, the problem becomes:

maximize

qᵀ K q

subject to

||q|| = 1

where K is the Davenport matrix constructed from measurement vectors.

The optimal quaternion corresponds to the eigenvector associated
with the largest eigenvalue of K.

The key difference between algorithms lies in how this optimal
eigenvector is obtained.

Davenport method:

- Compute eigenvalues and eigenvectors of K directly

QUEST method:

- Estimate the largest eigenvalue λ using Newton iteration
- Reconstruct the quaternion analytically afterward

Thus both algorithms produce the same optimal quaternion.

---

## 3. QUEST Mathematical Structure

The quaternion is partitioned as:

q = [ q0 ]
    [ qv ]

where

q0 : scalar part  
qv : 3×1 vector part

The Davenport matrix has block structure:

K =
[ σ        zᵀ ]
[ z   S − σI ]

with

σ = trace(B)  
S = B + Bᵀ  
z = skew(B)

Expanding the eigenvalue equation

K q = λ q

yields the relation

((σ + λ)I − S) qv = z q0

Define

M(λ) = (σ + λ)I − S

Then

M(λ) qv = z q0

Dividing by q0 (assuming q0 ≠ 0):

qv / q0 = M(λ)⁻¹ z

Let

p = qv / q0

Then

p = M(λ)⁻¹ z

Once the largest eigenvalue λ is known,
the quaternion can be reconstructed as

q ∝ [1 , p]

followed by normalization.

Thus QUEST reduces the eigenvector problem to finding λ.

---

## 4. Eigenvalue Estimation via Newton Iteration

Instead of solving the characteristic equation explicitly,
QUEST estimates the largest eigenvalue using Newton iteration.

Given a scalar function f(λ) derived from the characteristic equation,
the iteration update is

λ_{k+1} = λ_k − f(λ_k) / f′(λ_k)

The initial estimate is typically chosen as

λ₀ = Σ a_i

which corresponds to the total weight of the measurements.

Because the largest eigenvalue lies near this value,
Newton iteration converges rapidly.

In practice only a few iterations are required.

---

## 5. Implementation

A new module was created:

src/quest.py

Main functions:

solve_quest()

Returns the optimal quaternion using the QUEST algorithm.

solve_quest_rotation()

Wrapper function that returns the rotation matrix while preserving
the project rotation convention

b = R r

This function internally performs

q = solve_quest(...)
R = quat_to_rot(q)ᵀ

similar to the previously introduced Davenport wrapper.

---

## 6. Verification Against Davenport q-Method

To validate the implementation,
QUEST results were compared directly with the Davenport solver.

Both algorithms were applied to the same simulated
star tracker measurement set.

Example output:

Visible stars: 72

QUEST Error ≈ 0.0259 deg  
Davenport Error ≈ 0.0259 deg

The errors were numerically identical within floating-point precision.

This confirms that:

- The QUEST implementation is correct
- Both algorithms recover the same optimal Wahba solution

---

## 7. Interpretation

The identical attitude errors demonstrate that
QUEST and Davenport are mathematically equivalent
solvers of Wahba’s problem.

The difference lies only in computational strategy:

Davenport:

- Direct eigenvalue decomposition

QUEST:

- Scalar eigenvalue estimation
- Quaternion reconstruction

Thus QUEST provides the same optimal solution
while potentially reducing computational cost.

---

## 8. Attitude Estimator Set Established

At this stage the simulation framework contains three
attitude estimation algorithms:

TRIAD

A geometric two-vector solution used as a simple baseline estimator.

QUEST

An efficient optimal Wahba solver using Newton iteration.

Davenport q-method

A direct eigenvalue-based Wahba solver used as a reference solution.

This estimator set enables systematic algorithm comparison.

---

## Day 11 Conclusion

The QUEST algorithm has been successfully implemented and validated.

Verification against the Davenport q-method confirms that
both algorithms produce identical optimal attitude estimates.

The star tracker simulation framework now supports multiple
attitude determination methods, enabling comparative analysis
of estimator performance under realistic sensor conditions.

---

## Next Step

Perform Monte Carlo performance analysis comparing
the behavior of TRIAD and QUEST under varying conditions:

measurement noise  
number of observed stars  
field-of-view size

This analysis will produce performance curves that characterize
the robustness and accuracy of each attitude estimation method.

---
## Day 12 – Monte Carlo Performance Analysis of TRIAD vs QUEST

### Goal

Evaluate the statistical performance of the implemented attitude determination algorithms (TRIAD and QUEST) using Monte Carlo simulations.

The objective of this step is to analyze:

- estimation accuracy
- robustness to measurement noise
- statistical distribution of attitude errors
- the effect of the number of observed stars

This marks the transition from algorithm implementation to quantitative performance evaluation.

---

### 1. Motivation

In previous stages, the star tracker simulation pipeline and the attitude estimation algorithms were successfully implemented and verified through individual simulation runs.

However, a single simulation run cannot reliably characterize the performance of an estimator.

In practice, star tracker measurements vary due to several stochastic factors:

- random star positions
- visible star selection by the field-of-view
- measurement noise

Because these conditions change for every observation, the resulting attitude estimation error also varies.

Therefore, performance must be evaluated statistically.

Monte Carlo simulation provides a systematic method for this by repeating the same experiment many times under different random conditions.

---

### 2. Monte Carlo Simulation Structure

Each Monte Carlo trial follows the complete star tracker measurement pipeline developed in previous days.

The simulation procedure is:

1. Generate random inertial star vectors  
2. Apply spacecraft attitude rotation  
3. Apply field-of-view filtering  
4. Apply magnitude detection threshold  
5. Add Gaussian measurement noise  
6. Estimate spacecraft attitude using TRIAD and QUEST  
7. Compute attitude estimation error  

The attitude error is calculated using the relative rotation:

R_err = R_true^T R_est

and the corresponding angular difference:

θ = arccos((trace(R_err) − 1) / 2)

This angle represents the smallest rotation required to align the estimated attitude with the true spacecraft orientation.

---

### 3. Noise Sensitivity Experiment

A Monte Carlo experiment was conducted to analyze the effect of measurement noise.

The simulation parameters were:

Noise sigma values tested:

0.001  
0.005  
0.01  
0.05  

For each noise level, 100 Monte Carlo trials were performed.

The following statistics were recorded:

- mean attitude error
- standard deviation of the error
- mean number of visible stars

---

### 4. Results – Noise vs Attitude Error

The results show that increasing measurement noise leads to larger attitude estimation errors for both algorithms.

However, a clear performance difference is observed.

QUEST consistently produces significantly smaller errors than TRIAD.

Example results:

σ = 0.001  
TRIAD mean error ≈ 0.36 deg  
QUEST mean error ≈ 0.028 deg  

σ = 0.05  
TRIAD mean error ≈ 17.36 deg  
QUEST mean error ≈ 1.27 deg  

This difference arises from the number of vectors used by the algorithms.

TRIAD determines attitude using only two vector observations.

QUEST solves the Wahba optimization problem using all available star measurements.

As a result, QUEST benefits from averaging effects that reduce the influence of measurement noise.

---

### 5. Error Standard Deviation Analysis

The standard deviation of the attitude error provides information about estimator stability.

The Monte Carlo results show that TRIAD has a significantly larger standard deviation than QUEST.

For large noise levels, the TRIAD standard deviation becomes extremely large.

This indicates that TRIAD occasionally produces very large errors.

These failures occur when the two vectors used by TRIAD become nearly collinear under noisy measurements, causing geometric instability in the cross-product construction.

QUEST avoids this issue because it uses multiple vector observations and solves a global optimization problem.

---

### 6. Error Distribution Analysis

To further analyze estimator robustness, the distribution of estimation errors was examined using:

- error histograms
- cumulative distribution functions (CDF)

The histogram shows that QUEST errors are tightly concentrated near zero degrees.

In contrast, TRIAD errors are spread over a much wider range and occasionally produce large outliers.

The CDF analysis confirms this behavior.

QUEST reaches high cumulative probability at very small error thresholds, indicating that most trials produce accurate estimates.

TRIAD reaches the same probability level only at much larger error thresholds.

This demonstrates that QUEST is significantly more reliable under measurement noise.

---

### 7. Effect of Star Count

Additional Monte Carlo experiments were performed by varying the total number of stars in the simulated sky.

Results show that increasing the number of stars improves QUEST estimation accuracy.

As more stars become visible within the field of view, the Wahba optimization uses more vector observations, reducing estimation error.

In contrast, TRIAD does not significantly benefit from additional stars because it always uses only two vectors.

---

### Conclusion

The Monte Carlo experiments demonstrate several important characteristics of the implemented algorithms.

First, QUEST significantly outperforms TRIAD in terms of estimation accuracy under noisy measurements.

Second, QUEST exhibits much smaller error variance, indicating more stable estimation performance.

Third, increasing the number of available star observations improves QUEST accuracy, consistent with the Wahba problem formulation.

Overall, the results confirm that QUEST provides both higher accuracy and greater robustness than TRIAD for star tracker attitude determination.

---

### Next Step

Extend the Monte Carlo analysis by investigating additional factors influencing estimation performance:

- field-of-view size
- magnitude detection threshold
- eigenvalue gap analysis

These experiments will provide deeper insight into the relationship between sensor configuration and attitude estimation accuracy.
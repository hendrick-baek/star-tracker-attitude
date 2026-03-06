# Code Guide – Star Tracker Attitude Determination Project

This document summarizes the structure of the project codebase, the development timeline of each module, and the purpose, inputs, outputs, and usage of the main functions.

The goal of this guide is to make the codebase easy to understand, maintain, and explain during capstone presentation and report writing.

---

# 1. Project Overview

This project implements a complete simulation and evaluation pipeline for star-tracker-based spacecraft attitude determination.

The project includes:

- rotation mathematics
- quaternion algebra
- Wahba attitude estimation
- Davenport q-method
- TRIAD algorithm
- QUEST algorithm
- star field simulation
- sensor field-of-view modeling
- magnitude filtering
- measurement noise modeling
- Monte Carlo performance analysis
- visualization and plotting

The project rotation convention is fixed as:

b = R r

where:

r : inertial frame unit vector  
b : body / camera frame unit vector  
R : rotation matrix (inertial → body)

All modules follow this convention.

---

# 2. Project Directory Structure

project/

├── src/  
│  
├── rotations.py  
├── quaternion.py  
├── wahba.py  
├── triad.py  
├── quest.py  

│  
├── star_field.py  
├── star_tracker_sensor.py  
├── star_tracker_simulator.py  

│  
├── phase1_noise_validation.py  

│  
├── monte_carlo.py  
├── monte_carlo_extended.py  

│  
├── plot_day12_noise_sweep.py  
├── plot_day12_extended.py  

│  
├── test_day7_visible_count.py  
├── test_day7_magnitude_cut.py  
├── test_day8_pipeline.py  
├── test_day9_attitude_estimation.py  
├── test_day10_triad.py  
├── test_day11_quest.py  
├── test_day12_monte_carlo.py  

│  
├── test_quaternion.py  
├── test_rotation.py  
├── test_wahba.py  



---

# 3. Development Timeline

## Day 1
Rotation matrix validation

Implemented:
- rotation orthogonality checks
- determinant validation
- vector norm preservation

Files:
rotations.py  
notebooks/day1_rotation_check.ipynb

---

## Day 2
Rodrigues rotation and axis-angle mathematics.

File:
rotations.py

---

## Day 3
Quaternion algebra implementation.

File:
quaternion.py

Functions implemented:

normalize(q)  
conjugate(q)  
multiply(q1,q2)  
rotate_vector(q,v)  
quat_to_rot(q)

Purpose:
Provide quaternion attitude representation and vector rotation.

---

## Day 4
Wahba problem solver using Davenport q-method.

File:
wahba.py

Functions implemented:

build_B(b_vectors, r_vectors, weights)

Input

b_vectors : (N,3) body vectors  
r_vectors : (N,3) inertial vectors  

Output

B : (3,3)

Purpose

Construct Wahba alignment matrix

B = Σ aᵢ bᵢ rᵢᵀ

---

build_K(B)

Input

B : (3,3)

Output

K : (4,4)

Purpose

Construct Davenport K matrix used for eigenvalue optimization.

---

solve_wahba(b_vectors, r_vectors)

Input

b_vectors : (N,3)  
r_vectors : (N,3)

Output

q_opt : (4,)

Purpose

Compute optimal quaternion solution to Wahba problem.

Method

1 construct B matrix  
2 construct K matrix  
3 compute eigenvalues  
4 return eigenvector with largest eigenvalue  

---

solve_wahba_rotation(...)

Wrapper function returning rotation matrix directly.

Implementation

q = solve_wahba(...)  
R = quat_to_rot(q).T

Transpose ensures project convention

b = R r

---

## Day 5
Noise validation experiment for Wahba estimator.

File

phase1_noise_validation.py

Purpose

Evaluate estimator error under varying noise levels.

---

## Day 6
Star tracker sensor model design.

Concept development for

star field generation  
sensor FOV filtering  
magnitude thresholding

---

## Day 7
Star field generation and visibility modeling.

File

star_field.py

Functions

random_unit_vectors(N)

Input

N : number of stars

Output

(N,3) unit vectors

Purpose

Generate isotropic star directions.

---

spherical_cap_fraction(theta)

Input

theta : FOV half angle

Output

visible fraction

Purpose

Compute theoretical visible fraction of sky.

---

filter_fov_body(vectors, boresight, fov_deg)

Input

vectors : (N,3)  
boresight : (3,)  
fov_deg : float

Output

visible vectors

Purpose

Apply sensor field-of-view constraint.

---

## Day 7 Sensor Model

File

star_tracker_sensor.py

Functions

assign_magnitude_uniform(N)

Assign synthetic star magnitudes.

---

apply_magnitude_cut(r_vectors, mags, m_lim)

Input

r_vectors : star directions  
mags : magnitudes  
m_lim : detection threshold

Output

filtered stars

Purpose

Remove stars dimmer than detection limit.

---

## Day 8
Full star tracker measurement simulator.

File

star_tracker_simulator.py

Main function

simulate_star_tracker_measurements

Input

N_total : total stars  
R_true : true spacecraft rotation  
fov_deg : sensor field of view  
m_lim : magnitude limit  
noise_sigma : measurement noise

Output

r_visible : inertial vectors  
b_measured : body frame vectors

Pipeline

1 generate star field  
2 rotate stars using true attitude  
3 apply FOV filter  
4 apply magnitude filter  
5 add measurement noise  

---

## Day 9
Full pipeline attitude estimation.

Test file

test_day9_attitude_estimation.py

Pipeline

star simulation  
→ Wahba estimation  
→ attitude error calculation

---

## Day 10
TRIAD algorithm implementation.

File

triad.py

Function

solve_triad(r1,r2,b1,b2)

Input

two inertial vectors  
two body vectors

Output

rotation matrix

Algorithm

1 build inertial orthonormal basis  
2 build body orthonormal basis  
3 compute rotation

R = T_b T_rᵀ

Limitation

Uses only two vectors and is noise sensitive.

---

## Day 11
QUEST algorithm implementation.

File

quest.py

Function

solve_quest(b_vectors,r_vectors)

Input

vector pairs

Output

quaternion

Purpose

Efficient Wahba solution using Newton iteration.

---

solve_quest_rotation(...)

Wrapper returning rotation matrix.

R = quat_to_rot(q).T

---

## Day 12
Monte Carlo performance analysis.

Files

monte_carlo.py  
monte_carlo_extended.py  

Purpose

Evaluate estimator performance statistically.

Experiments include

noise sweep  
error distribution  
star count sweep  

Metrics

mean error  
standard deviation  
error CDF  
histogram  

---

# 4. Monte Carlo Functions

File

monte_carlo.py

Functions

attitude_error_deg(R_true,R_est)

Compute angular error between rotations.

---

run_single_trial(...)

Runs one simulation trial.

Output

number of visible stars  
TRIAD error  
QUEST error  

---

run_monte_carlo_noise_sweep(...)

Runs many trials and computes statistics.

Output

mean error  
std error  
visible star statistics

---

# 5. Plotting Modules

plot_day12_noise_sweep.py

Generates plots

noise vs mean error  
noise vs std error  
noise vs visible stars  

---

plot_day12_extended.py

Generates additional plots

error histogram  
error CDF  
star count vs error  
star count vs std  
star count vs visible stars  

---

# 6. Test Scripts

test_day7_visible_count.py

Validates FOV theory vs simulation.

---

test_day8_pipeline.py

Checks measurement simulator pipeline.

---

test_day9_attitude_estimation.py

End-to-end estimator validation.

---

test_day10_triad.py

TRIAD vs Wahba comparison.

---

test_day11_quest.py

QUEST vs Davenport validation.

---

test_day12_monte_carlo.py

Monte Carlo noise sweep experiment.

---

# 7. Execution Guide

Run attitude estimation pipeline

python src/test_day9_attitude_estimation.py

---

Run TRIAD comparison

python src/test_day10_triad.py

---

Run QUEST verification

python src/test_day11_quest.py

---

Run Monte Carlo experiment

python src/test_day12_monte_carlo.py

---

Generate noise plots

python src/plot_day12_noise_sweep.py

---

Generate extended plots

python src/plot_day12_extended.py

---

# 8. Summary

This project implements a complete research-grade simulation framework for star tracker attitude determination.

Implemented capabilities include:

- star field simulation
- star tracker sensor modeling
- Wahba optimal estimation
- TRIAD baseline estimation
- QUEST algorithm
- Monte Carlo statistical analysis
- performance visualization

The modular structure allows future extensions such as:

sensor calibration  
magnetic navigation fusion  
EKF attitude filtering  
hardware-in-the-loop testing
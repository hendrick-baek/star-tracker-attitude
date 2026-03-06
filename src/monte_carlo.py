import numpy as np

from quaternion import quat_to_rot
from triad import solve_triad
from quest import solve_quest_rotation
from star_tracker_simulator import simulate_star_tracker_measurements


def attitude_error_deg(R_true, R_est):
    """
    Compute principal rotation angle error in degrees.
    """
    R_err = R_est @ R_true.T
    trace_val = np.trace(R_err)
    cos_angle = 0.5 * (trace_val - 1.0)
    cos_angle = np.clip(cos_angle, -1.0, 1.0)
    angle_rad = np.arccos(cos_angle)
    return np.degrees(angle_rad)


def run_single_trial(
    R_true,
    N_total=10000,
    fov_deg=20.0,
    m_lim=2.0,
    noise_sigma=0.001,
):
    """
    Run one simulated star tracker trial and return TRIAD / QUEST errors.

    Returns
    -------
    result : dict
        {
            "num_visible": int,
            "triad_error_deg": float or None,
            "quest_error_deg": float or None
        }
    """
    r_visible, b_meas = simulate_star_tracker_measurements(
        N_total=N_total,
        R_true=R_true,
        fov_deg=fov_deg,
        m_lim=m_lim,
        noise_sigma=noise_sigma
    )

    num_visible = len(r_visible)

    triad_error = None
    quest_error = None

    # QUEST requires enough visible stars for Wahba solve
    if num_visible >= 2:
        R_est_quest = solve_quest_rotation(b_meas, r_visible)
        quest_error = attitude_error_deg(R_true, R_est_quest)

        # TRIAD uses first two visible stars
        r1 = r_visible[0]
        r2 = r_visible[1]
        b1 = b_meas[0]
        b2 = b_meas[1]

        R_est_triad = solve_triad(r1, r2, b1, b2)
        triad_error = attitude_error_deg(R_true, R_est_triad)

    return {
        "num_visible": num_visible,
        "triad_error_deg": triad_error,
        "quest_error_deg": quest_error,
    }


def run_monte_carlo_noise_sweep(
    sigmas,
    num_trials=100,
    N_total=10000,
    fov_deg=20.0,
    m_lim=2.0,
    seed=42,
):
    """
    Monte Carlo experiment for noise sweep.

    Parameters
    ----------
    sigmas : list[float]
        Noise sigma values to test
    num_trials : int
        Number of trials per sigma
    N_total : int
        Total number of stars in simulated sky
    fov_deg : float
        Sensor field of view half-angle
    m_lim : float
        Magnitude cutoff
    seed : int
        Random seed

    Returns
    -------
    results : list of dict
    """
    np.random.seed(seed)

    # Fixed true rotation
    q_true = np.array([0.9659258, 0.0, 0.2588190, 0.0])
    q_true = q_true / np.linalg.norm(q_true)
    R_true = quat_to_rot(q_true)

    results = []

    for sigma in sigmas:
        triad_errors = []
        quest_errors = []
        visible_counts = []

        for _ in range(num_trials):
            trial = run_single_trial(
                R_true=R_true,
                N_total=N_total,
                fov_deg=fov_deg,
                m_lim=m_lim,
                noise_sigma=sigma,
            )

            visible_counts.append(trial["num_visible"])

            if trial["triad_error_deg"] is not None:
                triad_errors.append(trial["triad_error_deg"])

            if trial["quest_error_deg"] is not None:
                quest_errors.append(trial["quest_error_deg"])

        result = {
            "sigma": sigma,
            "num_trials": num_trials,
            "mean_visible": float(np.mean(visible_counts)),
            "triad_mean_deg": float(np.mean(triad_errors)) if len(triad_errors) > 0 else None,
            "triad_std_deg": float(np.std(triad_errors)) if len(triad_errors) > 0 else None,
            "quest_mean_deg": float(np.mean(quest_errors)) if len(quest_errors) > 0 else None,
            "quest_std_deg": float(np.std(quest_errors)) if len(quest_errors) > 0 else None,
        }

        results.append(result)

    return results
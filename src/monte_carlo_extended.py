import numpy as np

from quaternion import quat_to_rot
from triad import solve_triad
from quest import solve_quest_rotation
from star_tracker_simulator import simulate_star_tracker_measurements


def attitude_error_deg(R_true, R_est):
    R_err = R_est @ R_true.T
    trace_val = np.trace(R_err)
    cos_angle = 0.5 * (trace_val - 1.0)
    cos_angle = np.clip(cos_angle, -1.0, 1.0)
    angle_rad = np.arccos(cos_angle)
    return np.degrees(angle_rad)


def get_fixed_true_rotation():
    q_true = np.array([0.9659258, 0.0, 0.2588190, 0.0])
    q_true = q_true / np.linalg.norm(q_true)
    return quat_to_rot(q_true)


def run_single_trial(
    R_true,
    N_total=10000,
    fov_deg=20.0,
    m_lim=2.0,
    noise_sigma=0.001,
):
    r_visible, b_meas = simulate_star_tracker_measurements(
        N_total=N_total,
        R_true=R_true,
        fov_deg=fov_deg,
        m_lim=m_lim,
        noise_sigma=noise_sigma,
    )

    num_visible = len(r_visible)

    triad_error = None
    quest_error = None

    if num_visible >= 2:
        # QUEST
        R_est_quest = solve_quest_rotation(b_meas, r_visible)
        quest_error = attitude_error_deg(R_true, R_est_quest)

        # TRIAD
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


def run_error_distribution_trials(
    num_trials=500,
    N_total=10000,
    fov_deg=20.0,
    m_lim=2.0,
    noise_sigma=0.01,
    seed=42,
):
    """
    Collect raw TRIAD / QUEST error samples for histogram and CDF plotting.
    """
    np.random.seed(seed)
    R_true = get_fixed_true_rotation()

    triad_errors = []
    quest_errors = []
    visible_counts = []

    for _ in range(num_trials):
        trial = run_single_trial(
            R_true=R_true,
            N_total=N_total,
            fov_deg=fov_deg,
            m_lim=m_lim,
            noise_sigma=noise_sigma,
        )

        visible_counts.append(trial["num_visible"])

        if trial["triad_error_deg"] is not None:
            triad_errors.append(trial["triad_error_deg"])

        if trial["quest_error_deg"] is not None:
            quest_errors.append(trial["quest_error_deg"])

    return {
        "triad_errors": np.array(triad_errors, dtype=float),
        "quest_errors": np.array(quest_errors, dtype=float),
        "visible_counts": np.array(visible_counts, dtype=float),
        "noise_sigma": noise_sigma,
    }


def run_star_count_sweep(
    N_total_list,
    num_trials=100,
    fov_deg=20.0,
    m_lim=2.0,
    noise_sigma=0.01,
    seed=42,
):
    """
    Sweep total number of stars in the simulated sky and compare
    TRIAD / QUEST performance.
    """
    np.random.seed(seed)
    R_true = get_fixed_true_rotation()

    results = []

    for N_total in N_total_list:
        triad_errors = []
        quest_errors = []
        visible_counts = []

        for _ in range(num_trials):
            trial = run_single_trial(
                R_true=R_true,
                N_total=N_total,
                fov_deg=fov_deg,
                m_lim=m_lim,
                noise_sigma=noise_sigma,
            )

            visible_counts.append(trial["num_visible"])

            if trial["triad_error_deg"] is not None:
                triad_errors.append(trial["triad_error_deg"])

            if trial["quest_error_deg"] is not None:
                quest_errors.append(trial["quest_error_deg"])

        results.append({
            "N_total": N_total,
            "mean_visible": float(np.mean(visible_counts)),
            "triad_mean_deg": float(np.mean(triad_errors)) if len(triad_errors) > 0 else None,
            "triad_std_deg": float(np.std(triad_errors)) if len(triad_errors) > 0 else None,
            "quest_mean_deg": float(np.mean(quest_errors)) if len(quest_errors) > 0 else None,
            "quest_std_deg": float(np.std(quest_errors)) if len(quest_errors) > 0 else None,
        })

    return results
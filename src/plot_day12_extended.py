import os
import numpy as np
import matplotlib.pyplot as plt

from monte_carlo_extended import (
    run_error_distribution_trials,
    run_star_count_sweep,
)


def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def save_histogram(triad_errors, quest_errors, outdir, noise_sigma):
    plt.figure(figsize=(8, 5))
    plt.hist(triad_errors, bins=30, alpha=0.6, label="TRIAD")
    plt.hist(quest_errors, bins=30, alpha=0.6, label="QUEST")
    plt.xlabel("Attitude error (deg)")
    plt.ylabel("Frequency")
    plt.title(f"Error Histogram (sigma={noise_sigma})")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(outdir, "error_histogram.png"), dpi=300)
    plt.close()


def empirical_cdf(x):
    x_sorted = np.sort(x)
    y = np.arange(1, len(x_sorted) + 1) / len(x_sorted)
    return x_sorted, y


def save_cdf(triad_errors, quest_errors, outdir, noise_sigma):
    triad_x, triad_y = empirical_cdf(triad_errors)
    quest_x, quest_y = empirical_cdf(quest_errors)

    plt.figure(figsize=(8, 5))
    plt.plot(triad_x, triad_y, label="TRIAD")
    plt.plot(quest_x, quest_y, label="QUEST")
    plt.xlabel("Attitude error (deg)")
    plt.ylabel("CDF")
    plt.title(f"Error CDF (sigma={noise_sigma})")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(outdir, "error_cdf.png"), dpi=300)
    plt.close()


def extract_star_count_arrays(results):
    N_total = np.array([r["N_total"] for r in results], dtype=float)
    mean_visible = np.array([r["mean_visible"] for r in results], dtype=float)

    triad_mean = np.array([r["triad_mean_deg"] for r in results], dtype=float)
    triad_std = np.array([r["triad_std_deg"] for r in results], dtype=float)

    quest_mean = np.array([r["quest_mean_deg"] for r in results], dtype=float)
    quest_std = np.array([r["quest_std_deg"] for r in results], dtype=float)

    return N_total, mean_visible, triad_mean, triad_std, quest_mean, quest_std


def save_star_count_vs_error(N_total, triad_mean, quest_mean, outdir):
    plt.figure(figsize=(8, 5))
    plt.plot(N_total, triad_mean, marker="o", label="TRIAD")
    plt.plot(N_total, quest_mean, marker="s", label="QUEST")
    plt.xlabel("Total simulated stars")
    plt.ylabel("Mean attitude error (deg)")
    plt.title("Star Count vs Mean Attitude Error")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(outdir, "star_count_vs_mean_error.png"), dpi=300)
    plt.close()


def save_star_count_vs_std(N_total, triad_std, quest_std, outdir):
    plt.figure(figsize=(8, 5))
    plt.plot(N_total, triad_std, marker="o", label="TRIAD")
    plt.plot(N_total, quest_std, marker="s", label="QUEST")
    plt.xlabel("Total simulated stars")
    plt.ylabel("Std of attitude error (deg)")
    plt.title("Star Count vs Error Standard Deviation")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(outdir, "star_count_vs_std_error.png"), dpi=300)
    plt.close()


def save_star_count_vs_visible(N_total, mean_visible, outdir):
    plt.figure(figsize=(8, 5))
    plt.plot(N_total, mean_visible, marker="o")
    plt.xlabel("Total simulated stars")
    plt.ylabel("Mean visible stars")
    plt.title("Star Count vs Mean Visible Stars")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(outdir, "star_count_vs_visible_stars.png"), dpi=300)
    plt.close()


def print_star_count_results(results):
    print("\n=== Star Count Sweep Summary ===\n")
    for r in results:
        print(f"N_total: {r['N_total']}")
        print(f"  Mean Visible Stars : {r['mean_visible']:.2f}")
        print(f"  TRIAD Mean Error   : {r['triad_mean_deg']:.6f} deg")
        print(f"  TRIAD Std Error    : {r['triad_std_deg']:.6f} deg")
        print(f"  QUEST Mean Error   : {r['quest_mean_deg']:.6f} deg")
        print(f"  QUEST Std Error    : {r['quest_std_deg']:.6f} deg")
        print()


def main():
    # Output folder
    outdir = os.path.join("figures", "day12_extended")
    ensure_dir(outdir)

    # -------------------------------------------------
    # 1) Histogram + CDF at a representative noise level
    # -------------------------------------------------
    dist = run_error_distribution_trials(
        num_trials=500,
        N_total=10000,
        fov_deg=20.0,
        m_lim=2.0,
        noise_sigma=0.01,
        seed=42,
    )

    triad_errors = dist["triad_errors"]
    quest_errors = dist["quest_errors"]
    noise_sigma = dist["noise_sigma"]

    save_histogram(triad_errors, quest_errors, outdir, noise_sigma)
    save_cdf(triad_errors, quest_errors, outdir, noise_sigma)

    print("Saved:")
    print("  error_histogram.png")
    print("  error_cdf.png")

    # -------------------------------------------------
    # 2) Star count sweep
    # -------------------------------------------------
    N_total_list = [1000, 3000, 5000, 10000, 20000, 50000]

    results = run_star_count_sweep(
        N_total_list=N_total_list,
        num_trials=100,
        fov_deg=20.0,
        m_lim=2.0,
        noise_sigma=0.01,
        seed=42,
    )

    print_star_count_results(results)

    N_total, mean_visible, triad_mean, triad_std, quest_mean, quest_std = extract_star_count_arrays(results)

    save_star_count_vs_error(N_total, triad_mean, quest_mean, outdir)
    save_star_count_vs_std(N_total, triad_std, quest_std, outdir)
    save_star_count_vs_visible(N_total, mean_visible, outdir)

    print("Saved:")
    print("  star_count_vs_mean_error.png")
    print("  star_count_vs_std_error.png")
    print("  star_count_vs_visible_stars.png")
    print(f"\nAll figures saved to: {outdir}")


if __name__ == "__main__":
    main()
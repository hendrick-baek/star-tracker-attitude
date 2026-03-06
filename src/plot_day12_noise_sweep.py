import os
import numpy as np
import matplotlib.pyplot as plt

from monte_carlo import run_monte_carlo_noise_sweep


def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def extract_arrays(results):
    sigmas = np.array([r["sigma"] for r in results], dtype=float)
    mean_visible = np.array([r["mean_visible"] for r in results], dtype=float)

    triad_mean = np.array([r["triad_mean_deg"] for r in results], dtype=float)
    triad_std = np.array([r["triad_std_deg"] for r in results], dtype=float)

    quest_mean = np.array([r["quest_mean_deg"] for r in results], dtype=float)
    quest_std = np.array([r["quest_std_deg"] for r in results], dtype=float)

    return sigmas, mean_visible, triad_mean, triad_std, quest_mean, quest_std


def save_noise_vs_mean_error(sigmas, triad_mean, quest_mean, outdir):
    plt.figure(figsize=(8, 5))
    plt.plot(sigmas, triad_mean, marker="o", label="TRIAD")
    plt.plot(sigmas, quest_mean, marker="s", label="QUEST")
    plt.xlabel("Noise sigma")
    plt.ylabel("Mean attitude error (deg)")
    plt.title("Noise vs Mean Attitude Error")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(outdir, "noise_vs_mean_error.png"), dpi=300)
    plt.close()


def save_noise_vs_std_error(sigmas, triad_std, quest_std, outdir):
    plt.figure(figsize=(8, 5))
    plt.plot(sigmas, triad_std, marker="o", label="TRIAD")
    plt.plot(sigmas, quest_std, marker="s", label="QUEST")
    plt.xlabel("Noise sigma")
    plt.ylabel("Std of attitude error (deg)")
    plt.title("Noise vs Error Standard Deviation")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(outdir, "noise_vs_std_error.png"), dpi=300)
    plt.close()


def save_noise_vs_mean_error_logx(sigmas, triad_mean, quest_mean, outdir):
    plt.figure(figsize=(8, 5))
    plt.plot(sigmas, triad_mean, marker="o", label="TRIAD")
    plt.plot(sigmas, quest_mean, marker="s", label="QUEST")
    plt.xscale("log")
    plt.xlabel("Noise sigma (log scale)")
    plt.ylabel("Mean attitude error (deg)")
    plt.title("Noise vs Mean Attitude Error (Log X)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(outdir, "noise_vs_mean_error_logx.png"), dpi=300)
    plt.close()


def save_noise_vs_visible_stars(sigmas, mean_visible, outdir):
    plt.figure(figsize=(8, 5))
    plt.plot(sigmas, mean_visible, marker="o")
    plt.xlabel("Noise sigma")
    plt.ylabel("Mean visible stars")
    plt.title("Noise vs Mean Visible Star Count")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(outdir, "noise_vs_visible_stars.png"), dpi=300)
    plt.close()


def print_results_table(results):
    print("\n=== Noise Sweep Summary ===\n")
    for r in results:
        print(f"Sigma: {r['sigma']}")
        print(f"  Mean Visible Stars : {r['mean_visible']:.2f}")
        print(f"  TRIAD Mean Error   : {r['triad_mean_deg']:.6f} deg")
        print(f"  TRIAD Std Error    : {r['triad_std_deg']:.6f} deg")
        print(f"  QUEST Mean Error   : {r['quest_mean_deg']:.6f} deg")
        print(f"  QUEST Std Error    : {r['quest_std_deg']:.6f} deg")
        print()


def main():
    outdir = os.path.join("figures", "day12_noise_sweep")
    ensure_dir(outdir)

    sigmas = [0.001, 0.005, 0.01, 0.05]

    results = run_monte_carlo_noise_sweep(
        sigmas=sigmas,
        num_trials=100,
        N_total=10000,
        fov_deg=20.0,
        m_lim=2.0,
        seed=42,
    )

    print_results_table(results)

    sigmas, mean_visible, triad_mean, triad_std, quest_mean, quest_std = extract_arrays(results)

    save_noise_vs_mean_error(sigmas, triad_mean, quest_mean, outdir)
    save_noise_vs_std_error(sigmas, triad_std, quest_std, outdir)
    save_noise_vs_mean_error_logx(sigmas, triad_mean, quest_mean, outdir)
    save_noise_vs_visible_stars(sigmas, mean_visible, outdir)

    print(f"Saved figures to: {outdir}")


if __name__ == "__main__":
    main()
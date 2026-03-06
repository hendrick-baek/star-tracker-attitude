from monte_carlo import run_monte_carlo_noise_sweep


def main():
    sigmas = [0.001, 0.005, 0.01, 0.05]

    results = run_monte_carlo_noise_sweep(
        sigmas=sigmas,
        num_trials=1000,
        N_total=10000,
        fov_deg=20.0,
        m_lim=2.0,
        seed=42,
    )

    print("\n=== Monte Carlo Noise Sweep Results ===\n")

    for r in results:
        print(f"Sigma: {r['sigma']}")
        print(f"  Mean Visible Stars : {r['mean_visible']:.2f}")
        print(f"  TRIAD Mean Error   : {r['triad_mean_deg']:.6f} deg")
        print(f"  TRIAD Std Error    : {r['triad_std_deg']:.6f} deg")
        print(f"  QUEST Mean Error   : {r['quest_mean_deg']:.6f} deg")
        print(f"  QUEST Std Error    : {r['quest_std_deg']:.6f} deg")
        print()


if __name__ == "__main__":
    main()
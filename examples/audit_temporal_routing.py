from adaptive_gain.temporal_routing import temporal_routing_receipt


if __name__ == "__main__":
    print("rho\tphi\tfixed\tadaptive\tgain\trule")
    for rho in (0.0, 0.25, 0.5, 0.75, 1.0):
        receipt = temporal_routing_receipt(rho)
        print(
            f"{receipt.rho:.2f}\t"
            f"{receipt.temporal_autocorrelation:.2f}\t"
            f"{receipt.fixed_two_query_accuracy:.3f}\t"
            f"{receipt.optimal_adaptive_accuracy:.3f}\t"
            f"{receipt.adaptive_accuracy_gain:.3f}\t"
            f"{receipt.optimal_rule}"
        )

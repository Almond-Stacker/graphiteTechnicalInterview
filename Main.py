from Analysis import PricingAnalysis


def main():
    analysis = PricingAnalysis()

    results = analysis.compare_pricers()

    print("\n--- Pricing Comparison ---")

    for method, result in results.items():
        print(f"\n{method}")
        print("Price per mile:", result["price"])
        print("Profit:", result["profit"])
        print("Spillover:", result["spillover"])


if __name__ == "__main__":
    main()
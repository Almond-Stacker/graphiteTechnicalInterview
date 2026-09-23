import RideShareOptimizer 

# Sample usage and testing
if __name__ == "__main__":
    optimizer = RideShareOptimizer.RidePricingOptimizer()
    
    # Sample demand pattern: morning, lunch, evening, night
    base_demands = [30, 20, 50, 25]  # Small example for testing
    
    # print(f"Base demands: {base_demands}")
    # print(f"Available prices: {optimizer.price_options}")
    # print(f"Cost per ride: ${optimizer.cost_per_ride}\n")
    
    # Test simulation
    # test_prices = [8, 10, 12, 8]
    # test_profit = optimizer.simulate_day(base_demands, test_prices)
    # print(f"Test prices {test_prices} -> Profit: ${test_profit:.2f}\n")
    
    # Run your optimization
    prices = optimizer.optimize_prices(base_demands)
    results = optimizer.simulate_day(base_demands, prices)
    
    # for algorithm, result in results.items():
    #     print(f"{algorithm}:")
    print(f"  Prices: {prices}")
    print(f"  Profit: {results}")

import RideShareOptimizer 
import RideShareOptimizerAdvanced

# Sample usage and testing
if __name__ == "__main__":
    optimizer = RideShareOptimizerAdvanced.RidePricingOptimizer()
    
    # Sample demand pattern: morning, lunch, evening, night
    demand_data = {
        8:  {"demand": 40, "drivers": 30, "spillover_rate": 0.05},
        9:  {"demand": 55, "drivers": 35, "spillover_rate": 0.05},
        10: {"demand": 70, "drivers": 45, "spillover_rate": 0.10},
        11: {"demand": 90, "drivers": 50, "spillover_rate": 0.10},
    }

    # Run your optimization
    optimizer.compareAlgorithms(demand_data)
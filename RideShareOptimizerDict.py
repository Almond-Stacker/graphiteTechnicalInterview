import itertools

class RidePricingOptimizer:
    def __init__(self):
        self.cost_per_ride = 3.0
        self.price_options = [x for x in range(30)]  
        self.time_spillover_factor = {
            0: 0.3, 1: 0.3, 2: 0.3, 3: 0.3,
            4: 0.3, 5: 0.4, 6: 0.6, 7: 0.8,
            8: 0.9, 9: 0.8, 10: 0.6, 11: 0.6,
            12: 0.6, 13: 0.6, 14: 0.7, 15: 1.0,
            16: 1.0, 17: 1.0, 18: 1.0, 19: 0.9,
            20: 0.8, 21: 0.7, 22: 0.5, 23: 0.4
        }



    def compareAlgorithms(self, demand_data):
        performance = {}

        # Greedy optimizer
        greedy_prices = self.greedy_optimizer(demand_data)
        performance["Greedy Optimizer"] = greedy_prices

        # Brute force optimizer
        # Computationally heavy 
        brute_force_prices = self.brute_force_optimzier(demand_data)
        performance["Brute Force Optimizer"] = brute_force_prices

        # Dynamic optimizer
        # Reaches local minimum basically get stuck 
        dynamic_prices = self.dynamic_optimizer(demand_data)
        performance["Dynamic Optimizer"] = dynamic_prices

        for algo, prices in performance.items():
            profit = self.simulate_day(demand_data, prices)
            print(f"{algo}: {prices}")
            print(f"Profit: ${profit:.2f}\n")

        return performance
    

    def greedy_optimizer(self, demand_data):
        prices = []

        for hour, data in demand_data.items():
            demand = data["demand"]
            drivers = data["drivers"]

            best_profit = 0
            best_price = self.price_options[0]

            for price in self.price_options:
                (customers, spillover) = self.calculate_demand_and_spillover(demand, price, hour)
                
                profit = customers * price
                
                if profit > best_profit:
                    best_price = price
                    best_profit = profit

            prices.append(best_price)

        return prices


    def brute_force_optimzier(self, demand_data):
        # (best profit, best combination of prices)
        best_price = (0, [])

        # Generate every possible combination of prices
        # and find the combination that returns the most profit
        for prices in itertools.product(
            self.price_options, repeat=len(demand_data)
        ):
            profit = self.simulate_day(demand_data, prices)

            if profit > best_price[0]:
                best_price = (profit, prices)

        return best_price[1]

    
    # Gets stuck in a local minimum
    def dynamic_optimizer(self, demand_data):
        prices = [10] * len(demand_data)
        step = 0.5

        while True:
            improved = False

            current_profit = self.simulate_day(demand_data, prices)

            for i in range(len(prices)):
                print(prices)

                # Try increasing this time period's price
                test_prices = prices.copy()
                test_prices[i] += step

                higher_profit = self.simulate_day(demand_data, test_prices)

                # Try decreasing this time period's price
                test_prices = prices.copy()
                test_prices[i] -= step

                lower_profit = self.simulate_day(demand_data, test_prices)

                if higher_profit > current_profit:
                    prices[i] += step
                    improved = True

                elif lower_profit > current_profit:
                    prices[i] -= step
                    improved = True

            if not improved:
                break

        return prices

    
    def simulate_day(self, demand_data, prices):
        """
        Simulate one full day with the given prices and return total profit.
        """

        if len(demand_data) != len(prices):
            raise ValueError("demand_data and prices must have same length")

        total_profit = 0
        deferred_customers = 0

        for i, (hour, data) in enumerate(demand_data.items()):
            demand = data["demand"]
            drivers = data["drivers"]

            # Add customers who spilled over from the previous period
            total_demand = demand + deferred_customers

            actual_customers, new_deferred = self.calculate_demand_and_spillover(
                total_demand, prices[i], hour
            )

            # Calculate profit for this period
            period_profit = (prices[i] - self.cost_per_ride) * actual_customers
            total_profit += period_profit

            # Carry spillover into the next period
            deferred_customers = new_deferred

        return total_profit
    

    def calculate_demand_and_spillover(self, total_demand, price, hour):
        if price <= 10:
            price_spillover_rate = 0
        else:
            price_spillover_rate = (price - 10) * 0.05

        time_factor = self.time_spillover_factor[hour]

        spillover_rate = price_spillover_rate * time_factor

        spillover = int(total_demand * spillover_rate)
        customers = total_demand - spillover

        return customers, spillover
    

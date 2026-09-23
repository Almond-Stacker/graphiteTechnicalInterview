import itertools

class RidePricingOptimizer:
    def __init__(self):
        self.cost_per_ride = 3.0
        self.price_options = [7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 21]  
        self.driversAvailable = []

   
    def compareAlgorithms(self, base_demands):
        # {Algo name: performance}
        performance = {}

        prices = []

        # Run greedy optimizer
        for demand in base_demands:
            prices.append(self.greedy_optimizer(demand))

        performance["Greedy Optimizer"] = prices
        # performance["Brute Force Optimizer"] = self.brute_force_optimzier(base_demands)
        performance["Dynamic Optimizer"] = self.dynamic_optimizer(base_demands)

        for algo, results in performance.items():
            print(f"{algo}: {self.simulate_day(base_demands, results)} ")
        return performance



    def optimize_prices(self, base_demands):
        """
        Main optimization function - implement your algorithm here!
        
        Args:
            base_demands: Expected number of ride requests for each time period
                         Example: [20, 50, 80, 60, 40] for 5 periods
        
        Returns:
            List of optimal prices for each period
            Example: [8, 12, 15, 10, 7] 
        
        prices = []
        return prices
        """

        prices = []
        for demand in base_demands:
            prices.append(self.greedy_optimizer(demand))

        return prices


    def greedy_optimizer(self, hour_demand):
        # (total profit, price point)
        greatestProfit = (0, 0)
        
        for price in self.price_options:
            (customers, spill_over) = self.calculate_demand_and_spillover(hour_demand, price)
            profit = customers * price - self.cost_per_ride * spill_over
            if profit > greatestProfit[0]:
                greatestProfit = (profit, price)

        # Return most optimal price point for the hour 
        return greatestProfit[1]


    def brute_force_optimzier(self, base_demands):
        # (best proft, best combination of prices)
        best_price = (0, [])

        # Generate every combination for the prices possible and then find the one that returns 
        # The largest amount of profit 

        for prices in itertools.product(self.price_options, repeat=len(base_demands)):
            profit = self.simulate_day(base_demands, prices)

            if best_price[0] < profit:
                best_price = (profit, prices)

        return best_price[1]
    
    
    def dynamic_optimizer(self, demands):
        prices = [10] * len(demands)
        step = 1

        while True:
            improved = False

            current_revenue = self.simulate_day(demands, prices)

            for i in range(len(prices)):
                print(prices)
                # Try increasing this time period's price
                test_prices = prices.copy()
                test_prices[i] += step

                higher_revenue = self.simulate_day(demands, test_prices)

                # Try decreasing this time period's price
                test_prices = prices.copy()
                test_prices[i] -= step

                lower_revenue = self.simulate_day(demands, test_prices)

                if higher_revenue > current_revenue:
                    prices[i] += step
                    improved = True

                elif lower_revenue > current_revenue:
                    prices[i] -= step
                    improved = True

            if not improved:
                break

        return prices


    def simulate_day(self, base_demands, prices):
        """
        Simulate one full day with the given prices and return total profit.
        Make sure to handle spillover effects and demand calculations.
        Use this to evaluate your pricing strategy.
        
        Args:
            base_demands: Base demand for each period
            prices: Price in each period
            
        Returns:
            Total profit for the day
        """

        if len(base_demands) != len(prices):
            raise ValueError("base_demands and prices must have same length")
        
        total_profit = 0
        deferred_customers = 0  # Number of spillover customers
        
        for period in range(len(base_demands)):
            # Total demand = base demand + spillover
            total_demand = base_demands[period] + deferred_customers
            
            actual_customers, new_deferred = self.calculate_demand_and_spillover(total_demand, prices[period])
            
            # Calculate profit for this period
            period_profit = (prices[period] - self.cost_per_ride) * actual_customers
            total_profit += period_profit
            
            # Update spillover customers for next period
            deferred_customers = new_deferred
       
        return total_profit



    def calculate_demand_and_spillover(self, total_demand, price):
        """
        Calculate actual ridership and spillover based on price.

        The percentage of customers who defer increases linearly
        as the price increases.

        $10 -> 0% deferred
        $20 -> 10% deferred
        $30 -> 20% deferred
        $40 -> 30% deferred
        """

        if price <= 10:
            deferred_rate = 0
        else:
            deferred_rate = (price - 10) * 0.01

        deferred = int(total_demand * deferred_rate)
        actual = total_demand - deferred

        return actual, deferred
import itertools

class RidePricingOptimizer:
    def __init__(self):
        self.cost_per_ride = 3.0
        self.price_options = [7, 8, 10, 12, 15]  

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

        prices = self.brute_force_optimzer(base_demands)

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


    def brute_force_optimzer(self, base_demands):
        # (best proft, best combination of prices)
        best_price = (0, [])

        # Generate every combination for the prices possible and then find the one that returns 
        # The largest amount of profit 
        print(base_demands)
        print(self.price_options)

        for prices in itertools.product(self.price_options, repeat=len(base_demands)):
            profit = self.simulate_day(base_demands, prices)

            if best_price[0] < profit:
                best_price = (profit, prices)

        return best_price[1]


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
        - Low prices (<$10): Everyone rides, no deferrals
        - Medium prices ($10-$19): 10% of customers defer to next period  
        - High prices ($20+): 30% of customers defer to next period
        
        Args:
            total_demand: Total customers wanting rides this period
            price: Price being charged
            
        Returns:
            (actual_customers_this_period, customers_deferred_to_next_period)
        """

        if price <= 10:
            return total_demand, 0
        elif price <= 20:
            deferred = int(total_demand * 0.1)
            actual = total_demand - deferred
            return actual, deferred
        else:  # price >= 21:
            deferred = int(total_demand * 0.3)
            actual = total_demand - deferred
            return actual, deferred
 
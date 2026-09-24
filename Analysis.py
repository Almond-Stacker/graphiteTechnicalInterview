from Simulation import Simulator, DynamicPricer, BruteForcePricer, GreedyPricer


class PricingAnalysis:

    def __init__(self):
        self.sim = Simulator("riders.csv", "drivers.csv")

    def compare_pricers(self):
        riders = self.sim.riders

        # Dynamic
        dynamic_pricer = DynamicPricer(3)
        dynamic_price = dynamic_pricer.dynamically_price(riders)

        dynamic_profit, dynamic_spillover = self.sim.simulate_hour(
            riders,
            dynamic_price
        )

        # Brute Force
        brute_pricer = BruteForcePricer()
        brute_price = brute_pricer.brute_force_price(riders)

        brute_profit, brute_spillover = self.sim.simulate_hour(
            riders,
            brute_price
        )

        # Greedy
        greedy_pricer = GreedyPricer()
        greedy_price = greedy_pricer.greedy_price(riders)

        greedy_profit, greedy_spillover = self.sim.simulate_hour(
            riders,
            greedy_price
        )

        return {
            "Dynamic": {
                "price": dynamic_price,
                "profit": dynamic_profit,
                "spillover": len(dynamic_spillover)
            },

            "Brute Force": {
                "price": brute_price,
                "profit": brute_profit,
                "spillover": len(brute_spillover)
            },

            "Greedy": {
                "price": greedy_price,
                "profit": greedy_profit,
                "spillover": len(greedy_spillover)
            }
        }
import csv
import Drivers
import random 

class Simulator:

    def __init__(self, riders_path, drivers_path):
        self.riders = self.import_data(riders_path)
        self.drivers = self.import_data(drivers_path)
        self.cost_per_mile = 0.5

        self.driver_tree = Drivers.DriverKDTree(self.drivers)

    
    def import_data(self, csv_path):
        with open(csv_path, "r") as file:
            reader = csv.DictReader(file)
            data = list(reader)

        return data
    
    def simulate_hour(self, riders, price):
        matches = {}
        drivers_taken = set()

        customers, spillover = self.calculate_spillover(
            riders,
            price
        )

        for rider in customers:
            drivers = self.driver_tree.find_nearest_driver(rider, 0)

            matched = False

            for driver in drivers:
                if driver["id"] in drivers_taken:
                    continue

                matches[driver["id"]] = rider
                drivers_taken.add(driver["id"])
                matched = True
                break

            if not matched:
                spillover.append(rider)

        profit = self.calculate_profit(
            customers=matches.values(),
            price=price
        )

        return profit, spillover


    def calculate_profit(self, customers, price):
        total_profit = 0
            
        for customer in customers:
            distance = float(customer["distance"])

            revenue = distance * price
            cost = distance * self.cost_per_mile

            profit = revenue - cost
            total_profit += profit

        return total_profit


    def calculate_spillover(self, riders, price):
        if price <= 2:
            spillover_rate = 0
        else:
            spillover_rate = (price - 2) * 0.10

        spillover_count = int(len(riders) * spillover_rate)

        spillover_riders = riders[:spillover_count]
        remaining_riders = riders[spillover_count:]

        return remaining_riders, spillover_riders
        

class BruteForcePricer:
    def __init__(self):
        self.sim = Simulator("riders.csv", "drivers.csv")
        self.price_options = range(1, 11)

    def brute_force_price(self, riders):
        best_price = 0
        best_profit = float("-inf")

        for price in self.price_options:
            profit, spillover = self.sim.simulate_hour(
                riders,
                price
            )

            if profit > best_profit:
                best_profit = profit
                best_price = price

        return best_price

class GreedyPricer:
    def __init__(self):
        self.sim = Simulator("riders.csv", "drivers.csv")
        self.price_options = range(1, 11)

    def greedy_price(self, riders):
        best_price = self.price_options[0]
        best_profit = float("-inf")

        for price in self.price_options:
            profit, spillover = self.sim.simulate_hour(
                riders,
                price
            )

            if profit > best_profit:
                best_profit = profit
                best_price = price

        return best_price



class DynamicPricer:
    def __init__(self, price_per_mile):
        self.price_per_mile = price_per_mile
        self.sim = Simulator('riders.csv', 'drivers.csv')

    def calculate_price(self, rider):
        return self.price_per_mile * rider["distance"]
    
    def dynamically_price(self, riders):
        price = self.price_per_mile
        step = 0.1

        while True:
            print(price)
            current_profit = self.sim.simulate_hour(riders, price)[0]
            improved = False

            # Try increasing price per mile
            higher_price = price + step
            higher_profit = self.sim.simulate_hour(riders, higher_price)[0]

            # Try decreasing price per mile
            lower_price = price - step
            lower_profit = self.sim.simulate_hour(riders, lower_price)[0]

            if higher_profit > current_profit:
                price = higher_price
                improved = True

            elif lower_profit > current_profit:
                price = lower_price
                improved = True
        
            if not improved:
                break


        return price 
    


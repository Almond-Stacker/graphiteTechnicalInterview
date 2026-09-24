import random
import math
import csv


class DataGenerator:
    def __init__(self, map_size):
        self.map_size = map_size


    def generate_riders(self, num_riders):
        riders = []

        for i in range(num_riders):

            # More requests during morning and evening rush hour
            hour = random.choices(
                range(24),
                weights=[
                    1, 1, 1, 1, 1, 2,
                    4, 6, 7, 4, 3, 3,
                    3, 3, 3, 4,
                    6, 8, 8, 6, 4, 3,
                    2, 1
                ]
            )[0]

            origin = (
                random.randint(0, self.map_size),
                random.randint(0, self.map_size)
            )

            destination = (
                random.randint(0, self.map_size),
                random.randint(0, self.map_size)
            )

            distance = math.sqrt(
                (destination[0] - origin[0]) ** 2 +
                (destination[1] - origin[1]) ** 2
            )

            # Traffic makes trips take longer
            traffic_factor = random.uniform(2.5, 4.0)
            trip_duration = distance * traffic_factor

            # # Riders are slightly more willing to pay during rush hour
            # if 7 <= hour <= 9 or 17 <= hour <= 19:
            #     max_price = random.uniform(12, 25)
            # else:
            #     max_price = random.uniform(8, 20)

            rider = {
                "id": i,
                "request_time": hour,
                "origin_x": origin[0],
                "origin_y": origin[1],
                "destination_x": destination[0],
                "destination_y": destination[1],
                "distance": round(distance, 2),
                "trip_duration": round(trip_duration, 2),
                # "max_price": round(max_price, 2)
            } 

            riders.append(rider)

        return riders


    def generate_drivers(self, num_drivers):
        drivers = []

        for i in range(num_drivers):

            location = (
                random.randint(0, self.map_size),
                random.randint(0, self.map_size)
            )

            driver = {
                "id": i,
                "location_x": location[0],
                "location_y": location[1],
                # "available_time": round(random.uniform(0, 24), 2)
            }

            drivers.append(driver)

        return drivers


    def save_to_csv(self, data, filename):
        if not data:
            return

        with open(filename, "w", newline="") as file:
            writer = csv.DictWriter(
                file,
                fieldnames=data[0].keys()
            )

            writer.writeheader()
            writer.writerows(data)


    def generate_data(self, num_riders, num_drivers):
        riders = self.generate_riders(num_riders)
        drivers = self.generate_drivers(num_drivers)

        self.save_to_csv(riders, "riders.csv")
        self.save_to_csv(drivers, "drivers.csv")

        return riders, drivers
    

test = DataGenerator(100)
test.generate_data(100, 100)
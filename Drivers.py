from scipy.spatial import KDTree


class DriverKDTree:
    def __init__(self, drivers):
        self.drivers = drivers
        self.tree = None
        self.build_tree()

    def build_tree(self):
        locations = [
            (driver["location_x"], driver["location_y"])
            for driver in self.drivers
        ]

        self.tree = KDTree(locations)

    def find_nearest_driver(self, rider, current_time):        
        rider_location = (
            rider["origin_x"],
            rider["origin_y"]
        )

        distances, indexes = self.tree.query(
            rider_location,
            k=len(self.drivers)
        )

        # for distance, index in zip(distances, indexes):
        #     driver = self.drivers[index]

        #     if driver["available_time"] <= current_time:
        #         return driver

        drivers = []

        for index in indexes:
            drivers.append(self.drivers[index])

        return drivers


    def move_driver(self, driver, rider):
        driver["location_x"] = rider["destination_x"]
        driver["location_y"] = rider["destination_y"]

        self.build_tree()
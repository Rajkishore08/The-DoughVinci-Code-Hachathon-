import math
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

class Order:
    STATUS_CREATED = "created"
    STATUS_ASSIGNED = "assigned"
    STATUS_WAITING_PICKUP = "waiting to pickup"
    STATUS_DELIVERED = "delivered"

    def __init__(self, order_id, kitchen_id, customer_id, ready_time, kitchen_location):
        self.order_id = order_id
        self.kitchen_id = kitchen_id
        self.customer_id = customer_id
        self.ready_time = ready_time
        self.kitchen_location = kitchen_location
        self.assigned_to_rider = None
        self.status = self.STATUS_CREATED

    def assign_to_rider(self, rider_id):
        self.assigned_to_rider = rider_id
        self.status = self.STATUS_ASSIGNED

    def set_waiting_pickup(self):
        self.status = self.STATUS_WAITING_PICKUP

    def set_delivered(self):
        self.status = self.STATUS_DELIVERED

class Rider:
    def __init__(self, rider_id, location):
        self.rider_id = rider_id
        self.location = location
        self.assigned_orders = []
        self.order_count = 0

class DeliveryBatcher:
    def __init__(self):
        self.orders = []
        self.riders = []

    def add_order(self, order):
        self.orders.append(order)

    def add_rider(self, rider):
        self.riders.append(rider)

    def distance_between_locations(self, location1, location2):
        return math.sqrt((location1[0] - location2[0])**2 + (location1[1] - location2[1])**2)

    def assign_order_to_rider(self, order, rider):
        order.assign_to_rider(rider.rider_id)
        rider.assigned_orders.append(order)
        rider.order_count += 1
        print(f"Order {order.order_id} assigned to Rider {rider.rider_id}")
        print(f"Order Status: {order.status}")
        print(f"Order Details:")
        print(f" - Order ID: {order.order_id}")
        print(f" - Kitchen ID: {order.kitchen_id}")
        print(f" - Customer ID: {order.customer_id}")
        print(f" - Ready Time: {order.ready_time}")
        print(f" - Kitchen Location: {order.kitchen_location}")
        print(f"Rider {rider.rider_id} assigned {rider.order_count} orders:")
        for assigned_order in rider.assigned_orders:
            print(f" - Order {assigned_order.order_id}")

    def find_closest_rider(self, order):
        closest_rider = None
        min_distance = float('inf')

        for rider in self.riders:
            distance = self.distance_between_locations(order.kitchen_location, rider.location)
            if distance < min_distance:
                closest_rider = rider
                min_distance = distance

        return closest_rider

    def apply_rule(self, order):
        matching_order = None
        switch_rule = {
            1: self.rule_1,
            2: self.rule_2,
            3: self.rule_3,
            4: self.rule_4,
            5: self.rule_5,
            6: self.rule_6
        }
        
        for rule_number, rule_func in switch_rule.items():
            matching_order = rule_func(order)
            if matching_order:
                break

        return matching_order

    def rule_1(self, order):
        for existing_order in self.orders:
            if (existing_order.kitchen_id == order.kitchen_id and
                existing_order.customer_id == order.customer_id and
                abs(existing_order.ready_time - order.ready_time) <= 10):
                return existing_order
        return None

    def rule_2(self, order):
        for existing_order in self.orders:
            if (existing_order.customer_id == order.customer_id and
                abs(existing_order.ready_time - order.ready_time) <= 10 and
                existing_order.kitchen_id != order.kitchen_id):
                return existing_order
        return None

    def rule_3(self, order):
        for existing_order in self.orders:
            if (existing_order.kitchen_id == order.kitchen_id and
                existing_order.customer_id != order.customer_id and
                abs(existing_order.ready_time - order.ready_time) <= 10):
                return existing_order
        return None

    def rule_4(self, order):
        for existing_order in self.orders:
            if (existing_order.customer_id == order.customer_id and
                abs(existing_order.ready_time - order.ready_time) <= 10):
                return existing_order
        return None

    def rule_5(self, order):
        for existing_order in self.orders:
            if (self.distance_between_locations(existing_order.kitchen_location, order.kitchen_location) <= 1 and
                abs(existing_order.ready_time - order.ready_time) <= 10):
                return existing_order
        return None

    def rule_6(self, order):
        for existing_order in self.orders:
            if (existing_order.kitchen_id == order.kitchen_id and
                abs(existing_order.ready_time - order.ready_time) <= 10):
                return existing_order
        return None

    def visualize(self):
        plt.figure(figsize=(8, 8))

        # Load the image as background
        img = mpimg.imread('WebProject/python/map.png')
        plt.imshow(img, extent=[-10, 10, -10, 10])  # Set the extent to match your image dimensions
        
        for order in self.orders:
            plt.plot(order.kitchen_location[0], order.kitchen_location[1], 'bo', label='Kitchen')
            if order.assigned_to_rider:
                plt.plot(order.kitchen_location[0], order.kitchen_location[1], 'go', label=f'Assigned Order to Rider {order.assigned_to_rider}')
        for rider in self.riders:
            plt.plot(rider.location[0], rider.location[1], 'ro', label=f'Rider {rider.rider_id}')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title('Order Allocation Visualization')
        plt.legend()
        plt.grid(True)
        plt.show()

    def process_order(self):
        order_id = int(input("Enter Order ID: "))
        kitchen_id = int(input("Enter Kitchen ID: "))
        customer_id = int(input("Enter Customer ID: "))
        ready_time = int(input("Enter Ready Time: "))
        kitchen_location_x = float(input("Enter Kitchen Location X coordinate: "))
        kitchen_location_y = float(input("Enter Kitchen Location Y coordinate: "))
        kitchen_location = (kitchen_location_x, kitchen_location_y)

        new_order = Order(order_id, kitchen_id, customer_id, ready_time, kitchen_location)
        self.add_order(new_order)

        matching_order = self.apply_rule(new_order)
        if matching_order:
            closest_rider = self.find_closest_rider(matching_order)
            if closest_rider:
                self.assign_order_to_rider(matching_order, closest_rider)
                matching_order.set_waiting_pickup()  # Update status to waiting for pickup
            else:
                print("No available rider found.")
        else:
            print(f"No matching rule found for Order {order_id}")

# Example usage:
def main():
    batcher = DeliveryBatcher()

    # Add riders
    rider1 = Rider(rider_id=1, location=(0, 0))
    rider2 = Rider(rider_id=2, location=(1, 1))
    rider3 = Rider(rider_id=3, location=(-1, -1))
    rider4 = Rider(rider_id=4, location=(3, 3))
    rider5 = Rider(rider_id=5, location=(-4, -4))

    riders = [rider1, rider2, rider3, rider4, rider5]
    for rider in riders:
        batcher.add_rider(rider)

    while True:
        batcher.process_order()
        next_order = input("Do you want to add another order? (yes/no): ")
        if next_order.lower() != 'yes':
            break

    # Visualize the order allocation process
    batcher.visualize()

if __name__ == "__main__":
    main()

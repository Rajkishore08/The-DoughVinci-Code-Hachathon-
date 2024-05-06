import math

class Order:
    def __init__(self, order_id, kitchen_id, customer_id, ready_time, kitchen_location):
        self.order_id = order_id
        self.kitchen_id = kitchen_id
        self.customer_id = customer_id
        self.ready_time = ready_time
        self.kitchen_location = kitchen_location
        self.assigned_to_rider = False

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
        order.assigned_to_rider = True
        rider.assigned_orders.append(order)
        rider.order_count += 1
        print(f"\033[1;32mOrder {order.order_id} assigned to Rider {rider.rider_id}\033[0m")
        print(f"Rider {rider.rider_id} assigned {rider.order_count} orders:")
        for assigned_order in rider.assigned_orders:
            print(f" - Order {assigned_order.order_id}: Kitchen ID - {assigned_order.kitchen_id}, Customer ID - {assigned_order.customer_id}, Ready Time - {assigned_order.ready_time}, Kitchen Location - {assigned_order.kitchen_location}")

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
        if abs(self.orders[0].ready_time - order.ready_time) <= 10:
            return self.orders[0]
        return None

    def rule_6(self, order):
        if (self.orders[0].kitchen_id == order.kitchen_id and
            abs(self.orders[0].ready_time - order.ready_time) <= 10):
            return self.orders[0]
        return None

# Example usage:
batcher = DeliveryBatcher()

# Add riders
rider1 = Rider(rider_id=1, location=(0, 0))
rider2 = Rider(rider_id=2, location=(1, 1))
rider3 = Rider(rider_id=3, location=(2, 2))
rider4 = Rider(rider_id=4, location=(3, 3))
rider5 = Rider(rider_id=5, location=(4, 4))
rider6 = Rider(rider_id=6, location=(5, 5))
rider7 = Rider(rider_id=7, location=(6, 6))
rider8 = Rider(rider_id=8, location=(7, 7))

riders = [rider1, rider2, rider3, rider4, rider5, rider6, rider7, rider8]
for rider in riders:
    batcher.add_rider(rider)

# Add orders
orders_data = [
    [1, 1, 1, 10],  # rule 1
    [2, 1, 1, 28],
    [3, 2, 2, 10],  # rule 2
    [4, 3, 2, 14],
    [5, 4, 3, 10],  # rule 3
    [6, 4, 4, 14],
    [7, 5, 5, 10],  # rule 4
]

for order_data in orders_data:
    new_order = Order(*order_data)
    batcher.add_order(new_order)

    matching_order = batcher.apply_rule(new_order)
    if matching_order:
        closest_rider = batcher.find_closest_rider(matching_order)
        batcher.assign_order_to_rider(matching_order, closest_rider)
    else:
        print(f"\033[1;31mNo matching rule found for Order {order_data[0]}\033[0m")

# Print order details with separation
print("\n\033[1;34mOrder details:\033[0m")
for order in batcher.orders:
    print("=" * 30)
    print(f"Order ID: {order.order_id}")
    print(f"Kitchen ID: {order.kitchen_id}")
    print(f"Customer ID: {order.customer_id}")
    print(f"Ready Time: {order.ready_time}")
    print(f"Kitchen Location: {order.kitchen_location}")
    if order.assigned_to_rider:
        print(f"Assigned to Rider: \033[1;32mYes\033[0m")
    else:
        print(f"Assigned to Rider: \033[1;31mNo\033[0m")

# Print summary
print("=" * 60)
print("\n\033[1;34mSummary:\033[0m")
for rider in batcher.riders:
    print("=" * 30)
    print(f"Rider ID: {rider.rider_id}")
    print(f"Location: {rider.location}")
    print(f"Number of orders assigned: {rider.order_count}")
    print("\033[1;32mAssigned Orders:\033[0m")
    if rider.order_count == 0:
        print("\033[1;31mNone\033[0m")
    else:
        for assigned_order in rider.assigned_orders:
            print(f" - Order ID: {assigned_order.order_id}, Kitchen ID: {assigned_order.kitchen_id}, Customer ID: {assigned_order.customer_id}, Ready Time: {assigned_order.ready_time}, Kitchen Location: {assigned_order.kitchen_location}")

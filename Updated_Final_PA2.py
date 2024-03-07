import random
from Queue_for_ALGO import Queue


SECONDS_PER_ITEM = 4
OVERHEAD_SECONDS = 45
SIMULATION_DURATION = 7200
CUSTOMER_ITEM_RANGE = (6, 20)
UPDATE_INTERVAL = 50
NUM_REG = 3


class Customer:
    def __init__(self, item):
        self.item = item
        self.enqueue_time = None

    def checkout_time(self):
        return self.item * SECONDS_PER_ITEM + OVERHEAD_SECONDS


class Register:
    def __init__(self, is_express=False):
        self.is_express = is_express
        self.queue = Queue()
        self.total_customers_served = 0
        self.total_items_processed = 0
        self.total_idle_time = 0
        self.total_wait_time = 0
        self.current_customer_end_time = None
        self.idle_start_time = 0

    def add_customer(self, customer, current_time):
        was_idle = self.queue.isEmpty()
        customer.enqueue_time = current_time
        self.queue.enqueue(customer)

        if was_idle:
            self.current_customer_end_time = current_time + customer.checkout_time()
            if self.idle_start_time is not None:
                self.total_idle_time += current_time - self.idle_start_time
                self.idle_start_time = None

    def process_next_customer(self, current_time):
        if not self.queue.isEmpty():
            customer = self.queue.dequeue()
            self.total_customers_served += 1
            self.total_items_processed += customer.item
            wait_time = current_time - customer.enqueue_time
            self.total_wait_time += wait_time

            if self.queue.isEmpty():
                self.idle_start_time = current_time
            else:
                next_customer = self.queue.items[0]
                self.current_customer_end_time = current_time + next_customer.checkout_time()

    def is_busy(self):
        return not self.queue.isEmpty()

    def queue_length(self):
        return self.queue.size()


def generate_customer():
    item = random.randint(*CUSTOMER_ITEM_RANGE)
    return Customer(item)


def choose_register(customer, registers):
    all_registers = registers
    best_register = None
    min_estimated_wait = float('inf')

    for register in all_registers:
        estimated_wait = sum(c.checkout_time(
        ) for c in register.queue.items) + (register.queue.size() * OVERHEAD_SECONDS)
        if estimated_wait < min_estimated_wait:
            min_estimated_wait = estimated_wait
            best_register = register

    return best_register


def simulate_shift(registers):
    simulation_time = 0
    next_customer_arrival = simulation_time + random.randint(20, 40)

    while simulation_time < SIMULATION_DURATION:
        if simulation_time >= next_customer_arrival:
            customer = generate_customer()
            chosen_register = choose_register(customer, registers)
            chosen_register.add_customer(customer, simulation_time)
            next_customer_arrival = simulation_time + random.randint(20, 40)

        for register in registers:
            if register.is_busy() and (register.current_customer_end_time is None or simulation_time >= register.current_customer_end_time):
                register.process_next_customer(simulation_time)

        simulation_time += 1

        if simulation_time % UPDATE_INTERVAL == 0:
            display_status(registers, simulation_time)


def display_status(registers, elapsed_time):
    print(f"\nStatus at {elapsed_time} seconds:")
    print(f"{'Register':<10}{'Serving':<10}{'Queue':<30}")
    print("-" * 50)

    for i, register in enumerate(registers, start=1):
        serving = "--"

        if register.is_busy():
            serving = f"{register.queue.items[-1].item} items" if not register.queue.isEmpty(
            ) else "--"

        queue_display = "| " + \
            ", ".join(
                f"{customer.item} items" for customer in register.queue.items[:-1]) if register.queue.size() > 1 else ""

        register_type = "Express " if register.is_express else "Register"
        print(f"{register_type} {i:<5} {serving:<10} {queue_display:<30}")


def display_final_statistics(registers):
    print("\nRegister total     customers total     items total     idle time (min)    average wait time (sec)")

    total_customers = 0
    total_items = 0
    total_idle_time = 0
    total_wait_time = 0

    for i, register in enumerate(registers, start=1):
        if register.is_express:
            register_name = "Express"
        else:
            register_name = str(i)
        avg_wait_time = register.total_wait_time / \
            register.total_customers_served if register.total_customers_served > 0 else 0
        print(f" Register {register_name:<15} {register.total_customers_served:<17} {register.total_items_processed:<14} {register.total_idle_time / 60 :<19.2f} {avg_wait_time:.2f}")

        total_customers += register.total_customers_served
        total_items += register.total_items_processed
        total_idle_time += register.total_idle_time
        total_wait_time += register.total_wait_time

    overall_avg_wait_time = total_wait_time / \
        total_customers if total_customers > 0 else 0
    print("-" * 95)
    print(
        f"TOTAL:                    {total_customers:<17} {total_items:<14} {total_idle_time / 60:<19.2f} {overall_avg_wait_time:.2f}")


def main():
    cumulative_customers = 0
    cumulative_items = 0
    cumulative_idle_time = 0
    cumulative_wait_time = 0

    num_runs = 12

    for run in range(num_runs):
        registers = [Register(is_express=True) for _ in range(
            1)] + [Register() for _ in range(NUM_REG)]
        simulate_shift(registers)

        print(f"\nStatistics for Shift {run + 1}:")
        display_final_statistics(registers)

        for register in registers:
            cumulative_customers += register.total_customers_served
            cumulative_items += register.total_items_processed
            cumulative_idle_time += register.total_idle_time
            cumulative_wait_time += register.total_wait_time

    average_idle_time = cumulative_idle_time / num_runs / 60
    average_wait_time = cumulative_wait_time / \
        cumulative_customers if cumulative_customers > 0 else 0

    print("\nCumulative Final Statistics after 12 runs:")
    print(f"{'Total Customers Served:':<25} {cumulative_customers}")
    print(f"{'Total Items Processed:':<25} {cumulative_items}")
    print(f"{'Total Idle Time (min):':<25} {average_idle_time*12:.2f}")
    print(f"{'Average Wait Time (sec):':<25} {average_wait_time:.2f}")


main()
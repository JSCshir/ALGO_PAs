import random
from tabulate import tabulate
import timeit


def main():
    # Hardcoded values
    step_count = [20, 200, 2000, 20000, 200000, 2000000]
    d = 3
    # Function dim

    def dim(steps, dimension):
        move = [-1, 1]
        count = [0 for i in range(dimension)]
        for i in range(steps):
            dtm = random.randint(0, dimension - 1)
            count[dtm] += move[random.randint(0, 1)]
            if all(x == 0 for x in count):
                return 1
        return 0
    # Function Prob

    def prob(steps, dimension):
        count = 0
        for i in range(100):
            count += dim(steps, dimension)
        return count / 100
    # First table
    results = []
    for d in range(1, d+1):
        row = [d]
        row.extend(prob(steps, d) for steps in step_count)
        results.append(row)
    headers = ["Dimension"]
    for i in step_count:
        headers.append(str(i))
    prob_table = tabulate(results, headers, tablefmt="grid")
    print("Probability Table:\n", prob_table)
    # Function run_time_test
    run_time_results = [d]
    for step in step_count:
        def run_time_test(): return prob(step, d)

        time = timeit.timeit(run_time_test, number=1)
        run_time_results.append(time)
        # Second table
    run_time_headers = ["Dimension"]
    for i in step_count:
        run_time_headers.append(str(i))
    run_time_table = tabulate(
        [run_time_results], headers=run_time_headers, tablefmt="grid")
    print("\nRun Time (seconds) for 3D:\n", run_time_table)


main()

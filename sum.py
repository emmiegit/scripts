#!/usr/bin/env python

if __name__ == "__main__":
    numbers = []

    def totals_and_reset():
        if not numbers:
            return

        print("Sum: {}".format(sum(numbers)))
        print("Count: {}".format(len(numbers)))
        print("Mean: {}".format(sum(numbers) / len(numbers)))
        print("Smallest: {}".format(min(numbers)))
        print("Largest: {}".format(max(numbers)))
        numbers.clear()

    while True:
        try:
            numbers.append(float(input("> ")))
        except ValueError:
            totals_and_reset()
        except EOFError:
            totals_and_reset()
            exit()

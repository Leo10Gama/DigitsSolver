"""Solve a given 'Digits' puzzle."""


from functools import lru_cache
from random import choice
from typing import List, Optional, Tuple
from ops import Operator


@lru_cache(maxsize=None)
def solve_digits(target: int, nums: Tuple[int]) -> Optional[List[List[Tuple[int, Operator, int]]]]:
    """Given a target number and list (tuple) of numbers, solve the Digits puzzle.
    
    The process used is recursive and exhaustive, where all operations are
    attempted on all numbers over a given puzzle.

    Returns
    -------
    Optional[List[List[int U operator]]]
        The returned list contains various lists of tuples, where each Tuple
        represents one operation to perform between two existing numbers. If
        the number cannot be made, None is returned.
    """

    # Base case 0: We have one number
    if len(nums) == 1 and nums[0] != target:
        if nums[0] == target:
            return [None]
        else:
            return [-1]

    # Base case 1: The number exists in our list of nums
    if target in nums:
        return [None]

    valid_paths = []
    # Recursive step: perform all ops on all nums
    for num1 in nums:
        temp_nums = [x for x in nums]
        temp_nums.remove(num1)
        for num2 in temp_nums:
            for operator in Operator:
                new_nums = [x for x in temp_nums]
                new_nums.remove(num2)
                if operator == Operator.PLUS:
                    new_nums.append(num1 + num2)
                elif operator == Operator.MINUS:
                    if num1 < num2: continue  # cannot create negative number
                    new_nums.append(num1 - num2)
                elif operator == Operator.MULTIPLY:
                    new_nums.append(num1 * num2)
                elif operator == Operator.DIVIDE:
                    if num2 == 0: continue  # prevent divide-by-zero
                    quotient, remainder = divmod(num1, num2)
                    if remainder: continue  # cannot evenly divide
                    new_nums.append(quotient)
                steps = [(num1, operator, num2)]
                next_steps = solve_digits(target, tuple(new_nums))
                if next_steps[-1] == -1: continue  # cannot reach result from this operation
                else:
                    if next_steps[-1] != None:
                        temp_steps = steps
                        for next_step in next_steps:
                            temp_steps = [x for x in steps]
                            temp_steps.extend(next_step)
                            valid_paths.append(temp_steps)
                    else:
                        valid_paths.append(steps)  # last item will be either None or -1
    if not valid_paths:  # cannot reach number
        return [-1]
    return valid_paths


def print_digits_solution(solution: List[Tuple[int, Operator, int]]):
    """Given a Digits solution, print it properly."""
    for step in solution:
        print(f"{step[0]} {step[1]} {step[2]}")


if __name__=='__main__':
    target = int(input("Enter target num: "))
    nums = [int(num) for num in input("Enter available numbers, separated by a comma (e.g. '2,3,5,...)\n").split(',')]

    print("Generating solutions...", end="", flush=True)
    solutions = solve_digits(target, tuple(nums))
    print("Done!\n")

    print(f"{len(solutions)} solutions.\n")

    shortest_solution = solutions[0]
    for solution in solutions:
        if len(solution) <= len(shortest_solution):
            shortest_solution = solution
    print(f"Shortest solution is {len(shortest_solution)} steps:")
    print_digits_solution(shortest_solution)
    print()

    print("Here are 5 other solutions, chosen at random (press enter):")
    input()

    for _ in range(10):
        solution = choice(solutions)
        print_digits_solution(solution)
        print()

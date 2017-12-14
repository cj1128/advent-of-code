input = "0  5 10  0 11  14  13  4 11  8 8 7 1 4 12  11"

def rebalance(bank):
  bank = list(bank)
  length = len(bank)
  max_value = max(bank)
  max_value_index = bank.index(max_value)
  index = max_value_index
  bank[index] = 0
  for _ in range(max_value):
    index = (index + 1) % length
    bank[index] += 1
  return tuple(bank)

def solve_part1(input):
  cur = tuple(int(s) for s in input.strip().split())
  cycle = 0
  seen = set()
  while cur not in seen:
    cycle += 1
    seen.add(cur)
    cur = rebalance(cur)
  return cycle

# print(solve_part1(input))

def solve_part2(input):
  cur = tuple(int(s) for s in input.strip().split())
  cycle = 0
  seen = set()
  step_mapping = dict()
  while cur not in seen:
    seen.add(cur)
    step_mapping[cur] = cycle
    cycle += 1
    cur = rebalance(cur)
  return cycle - step_mapping[cur]

print(solve_part2(input))

input = 382
part1_test = (3, 638)

def solve_part1(input):
  state = [0]
  pos = 0
  for i in range(2017):
    next_pos = (pos + input) % len(state)
    state.insert(next_pos + 1, i + 1)
    pos = next_pos + 1
  return state[pos + 1]

# print(solve_part1(part1_test[0]) == part1_test[1])
# print(solve_part1(input))
# 1561

def solve_part2(input):
  current_length = 1
  pos = 0
  value_after_zero = None
  for i in range(50_000_000):
    next_pos = (pos + input) % current_length
    if next_pos == 0:
      value_after_zero = i + 1
    pos = next_pos + 1
    current_length += 1
  return value_after_zero

print(solve_part2(input))


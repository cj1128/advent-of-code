part1_test = (65, 8921, 588)
input = (516, 190)

def get_a_seq(start):
  value = start
  while True:
    value = (value * 16807) % 2147483647
    yield value

def get_b_seq(start):
  value = start
  while True:
    value = (value * 48271) % 2147483647
    yield value

def solve_part1(a_start, b_start):
  seq_a = get_a_seq(a_start)
  seq_b = get_b_seq(b_start)
  score = 0
  for _ in range(40_000_000):
    if (next(seq_a) ^ next(seq_b)) & 0xffff == 0:
      score += 1
  return score

# print(solve_part1(part1_test[0], part1_test[1]) == part1_test[2])
# print(solve_part1(input[0], input[1]))
# 597

part2_test = (65, 8921, 309)

def new_a_seq(a_start):
  seq = get_a_seq(a_start)
  for n in seq:
    if n % 4 == 0:
      yield n

def new_b_seq(b_start):
  seq = get_b_seq(b_start)
  for n in seq:
    if n % 8 == 0:
      yield n

def solve_part2(a_start, b_start):
  seq_a = new_a_seq(a_start)
  seq_b = new_b_seq(b_start)
  score = 0
  for _ in range(5_000_000):
    if (next(seq_a) ^ next(seq_b)) & 0xffff == 0:
      score += 1
  return score

# print(solve_part2(part2_test[0], part2_test[1]) == part2_test[2])
print(solve_part2(input[0], input[1]))


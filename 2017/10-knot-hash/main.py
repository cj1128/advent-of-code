from functools import reduce
from operator import xor

input = (list(range(256)), "129,154,49,198,200,133,97,254,41,6,2,1,255,0,191,108")
part1_test = (list(range(5)), "3,4,1,5", 12)

# reverse list[start:end], if end <= start,
# the range is circular
def reverse(l, start, length):
  if length <= 1:
    return
  end = (start + length) % len(l)
  if end > start:
    l[start:end] = list(reversed(l[start:end]))
  else:
    sub = list(reversed(l[start:] + l[:end]))
    l[start:] = sub[:len(l) - start]
    l[:end] = sub[len(sub) - end:]

def solve_part1(l, lengths):
  lengths = [int(s) for s in lengths.split(",")]
  pos = 0
  skip = 0
  list_length = len(l)
  for length in lengths:
    reverse(l, pos, length)
    pos = (pos + length + skip) % list_length
    skip += 1
  return l[0] * l[1]

# print(solve_part1(part1_test[0], part1_test[1]) == part1_test[2])
# print(solve_part1(input[0], input[1]))
# 19591

part2_tests = [
  ("", "a2582a3a0e66e6e86e3812dcb672a272"),
  ("AoC 2017", "33efeb34ea91902bb2f59c9920caa6cd"),
  ("1,2,3", "3efbe78a8d82f29979031a4aa0b16a9d"),
  ("1,2,4", "63960835bcdc130f0b66d7ff4f6a5a8e"),
]

def round(l, lengths):
  while True:
    for length in lengths:
      reverse(l, pos, length)
      pos = (pos + length + skip) % list_length
      skip += 1
    yield l

def solve_part2(input):
  lengths = [ord(c) for c in input.strip()] + [17, 31, 73, 47, 23]
  pos = 0
  skip = 0
  l = list(range(256))
  list_length = len(l)
  for _ in range(64):
    for length in lengths:
      reverse(l, pos, length)
      pos = (pos + length + skip) % list_length
      skip += 1
  hash = [reduce(xor, l[i:i+16]) for i in range(0, 256, 16)]
  return "".join(format(n, "02x") for n in hash)

# for t in part2_tests:
  # print(solve_part2(t[0]) == t[1])
print(solve_part2(input[1]))
# 62e2204d2ca4f4924f6e7a80f1288786

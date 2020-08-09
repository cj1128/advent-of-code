import binascii
import numpy
import sys
sys.path.append("..")

from utils import know_hash

input = "hwlqcszp"
part1_test = ("flqrgnkx", 8108)

def solve_part1(input):
  used = 0
  for i in range(128):
    hash = know_hash(f"{input}-{i}")
    bits = format(int(hash, 16), "08b")
    used += bits.count("1")
  return used

# print(solve_part1(part1_test[0]) == part1_test[1])
# print(solve_part1(input))
# 8304

part2_test = ("flqrgnkx", 1242)

def get_adjacent(row, col, dimension):
  result = []
  # top
  if row > 0:
    result.append((row - 1, col))
  # down
  if row < dimension - 1:
    result.append((row + 1, col))
  # left
  if col > 0:
    result.append((row, col - 1))
  # right
  if col < dimension - 1:
    result.append((row, col + 1))
  return result

def mark_group(row, col, result, disk, group):
  result[(row, col)] = group
  for row, col in get_adjacent(row, col, 128):
    if disk[row][col] == 1 and (row, col) not in result:
      mark_group(row, col, result, disk, group)

def solve_part2(input):
  disk = []
  for i in range(128):
    hash = know_hash(f"{input}-{i}")
    bits = "".join([format(b, "08b") for b in binascii.unhexlify(hash)])
    disk.append([int(b) for b in bits])
  result = dict()
  group = 1
  for row in range(128):
    for col in range(128):
      if disk[row][col] == 0:
        continue
      if (row, col) in result:
        continue
      mark_group(row, col, result, disk, group)
      group += 1
  return max(result.values())

# print(solve_part2(part2_test[0]) == part2_test[1])
print(solve_part2(input))

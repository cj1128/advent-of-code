from collections import defaultdict

with open("test.txt") as f:
  test_str = f.read()
with open("input.txt") as f:
  input_str = f.read()

part1_test = (test_str, "ABCDEF")

up, down, left, right = (0, 1, 2, 3)

def parse_diagram(input):
  result = defaultdict(lambda: " ")
  start_x = 0
  for y, line in enumerate(input.split("\n")):
    for x, char in enumerate(list(line)):
      result[(x, y)] = char
      if y == 0 and char != " ":
        start_x = x
  return result, (start_x, 0)

def get_next_pos(pos, dir):
  x, y = pos
  if dir == up:
    return (x, y - 1)
  if dir == down:
    return (x, y + 1)
  if dir == left:
    return (x - 1, y)
  if dir == right:
    return (x + 1, y)

def get_next_dir(diagram, pos, dir):
  if dir == up or dir == down:
    candidates = [left, right]
  if dir == left or dir == right:
    candidates = [up, down]
  for d in candidates:
    pos = get_next_pos(pos, d)
    if diagram[pos] != " ":
      return d

def walk_diagram(diagram, start_pos):
  current_pos = start_pos
  current_char = "|"
  dir = down
  while True:
    next_pos = get_next_pos(current_pos, dir)
    next_char = diagram[next_pos]
    if next_char == " ":
      if current_char == "+":
        dir = get_next_dir(diagram, current_pos, dir)
      else:
        break
    else:
      if next_char.isalpha():
        yield next_char
      current_char = next_char
      current_pos = next_pos

def solve_part1(str):
  result = ""
  diagram, start_pos = parse_diagram(str)
  for char in walk_diagram(diagram, start_pos):
    result += char
  return result

# print(solve_part1(part1_test[0]) == part1_test[1])
# print(solve_part1(input_str))
# SXPZDFJNRL

part2_test = (test_str, 38)

def solve_part2(str):
  diagram, start_pos = parse_diagram(str)
  current_pos = start_pos
  current_char = "|"
  dir = down
  steps = 1
  while True:
    next_pos = get_next_pos(current_pos, dir)
    next_char = diagram[next_pos]
    if next_char == " ":
      if current_char == "+":
        dir = get_next_dir(diagram, current_pos, dir)
      else:
        break
    else:
      steps += 1
      current_char = next_char
      current_pos = next_pos
  return steps

# print(solve_part2(part2_test[0]), part2_test[1])
print(solve_part2(input_str))
# 18126

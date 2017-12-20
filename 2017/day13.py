input = """
0: 4
1: 2
2: 3
4: 4
6: 6
8: 5
10: 6
12: 6
14: 6
16: 8
18: 8
20: 9
22: 12
24: 8
26: 8
28: 8
30: 12
32: 12
34: 8
36: 12
38: 10
40: 12
42: 12
44: 10
46: 12
48: 14
50: 12
52: 14
54: 14
56: 12
58: 14
60: 12
62: 14
64: 18
66: 14
68: 14
72: 14
76: 14
82: 14
86: 14
88: 18
90: 14
92: 17
"""

part1_test = ("""
0: 3
1: 2
4: 4
6: 4
""", 24)

# > depth means go back
def move_scanner(scanner, firewall, steps=1):
  for layer in scanner:
    pos = scanner[layer]
    depth = firewall[layer]
    pos = (pos + steps) % ((depth - 1) * 2)
    scanner[layer] = pos

def init_scanner(firewall):
  scanner = dict()
  for layer in firewall:
    scanner[layer] = 0
  return scanner

def parse_input(input):
  firewall = dict()
  for line in input.strip().split("\n"):
    parts = line.split(": ")
    layer = int(parts[0])
    depth = int(parts[1])
    firewall[layer] = depth
  return firewall

def get_caughts(firewall, scanner):
  caught = []
  scanner = scanner.copy()
  max_layer = max(firewall.keys())
  for layer in range(max_layer+1):
    if layer in firewall:
      if scanner[layer] == 0:
        caught.append(layer)
    move_scanner(scanner, firewall)
  return caught

def will_be_caught(firewall, scanner):
  scanner = dict(scanner)
  for layer in range(max(firewall.keys()) + 1):
    if scanner.get(layer) == 0:
      return True
    move_scanner(scanner, firewall)
  return False

def solve_part1(input):
  firewall = parse_input(input)
  scanner = init_scanner(firewall)
  caughts = get_caughts(firewall, scanner)
  sum = 0
  for layer in caughts:
    sum += layer * firewall[layer]
  return sum

# print(solve_part1(part1_test[0]) == part1_test[1])
# print(solve_part1(input))
# 1316

part2_test = ("""
0: 3
1: 2
4: 4
6: 4
""", 10)

def solve_part2(input):
  firewall = parse_input(input)
  scanner = init_scanner(firewall)
  delay = 0
  while True:
    if not will_be_caught(firewall, scanner):
      return delay
    delay += 1
    move_scanner(scanner, firewall)

print(solve_part2(part2_test[0]) == part2_test[1])
# print(solve_part2(input))
# 3840052, finished in 118.2s

from collections import defaultdict

test = """
..#
#..
...
"""

input = """
...#.##.#.#.#.#..##.###.#
......##.....#####..#.#.#
#..####.######.#.#.##...#
...##..####........#.#.#.
.#.#####..#.....#######..
.#...#.#.##.#.#.....#....
.#.#.#.#.#####.#.#..#...#
###..##.###.#.....#...#.#
#####..#.....###.....####
#.##............###.#.###
#...###.....#.#.##.#..#.#
.#.###.##..#####.....####
.#...#..#..###.##..#....#
##.##...###....##.###.##.
#.##.###.#.#........#.#..
##......#..###.#######.##
.#####.##..#..#....##.##.
###..#...#..#.##..#.....#
##..#.###.###.#...##...#.
##..##..##.###..#.##..#..
...#.#.###..#....##.##.#.
##.##..####..##.##.##.##.
#...####.######.#...##...
.###..##.##..##.####....#
#.##....#.#.#..#.###..##.
"""

class VirusCarrier:
  def __init__(self, str):
    lines = str.strip().split()
    self.dimension = len(lines)
    self.infected = set()
    self.x = self.dimension // 2
    self.y = self.x
    self.dir = "up"
    self.make_node_infected_count = 0
    for y, line in enumerate(lines):
      for x, c in enumerate(line):
        if c == "#":
          self.infected.add((x, y))

  def turn_right(self):
    if self.dir == "up":
      self.dir = "right"
    elif self.dir == "down":
      self.dir = "left"
    elif self.dir == "left":
      self.dir = "up"
    else:
      self.dir = "down"

  def turn_left(self):
    if self.dir == "up":
      self.dir = "left"
    elif self.dir == "down":
      self.dir = "right"
    elif self.dir == "left":
      self.dir = "down"
    else:
      self.dir = "up"

  def move(self):
    if self.dir == "up":
      self.y -= 1
    elif self.dir == "down":
      self.y += 1
    elif self.dir == "left":
      self.x -= 1
    else:
      self.x += 1

  def burst(self):
    pos = (self.x, self.y)
    if pos in self.infected:
      self.turn_right()
      self.infected.remove(pos)
    else:
      self.turn_left()
      self.infected.add(pos)
      self.make_node_infected_count += 1
    self.move()

def solve_part1(input):
  vc = VirusCarrier(input)
  for i in range(10000):
    vc.burst()
  return vc.make_node_infected_count

# print(solve_part1(test) == 5587)

# print(solve_part1(input))
# 5406

class VirusCarrierEvolved(VirusCarrier):
  def __init__(self, str):
    lines = str.strip().split()
    self.dimension = len(lines)
    self.map = defaultdict(lambda: "clean")
    self.x = self.dimension // 2
    self.y = self.x
    self.dir = "up"
    self.make_node_infected_count = 0
    for y, line in enumerate(lines):
      for x, c in enumerate(line):
        if c == "#":
          self.map[(x, y)] = "infected"

  def reverse_dir(self):
    if self.dir == "up":
      self.dir = "down"
    elif self.dir == "down":
      self.dir = "up"
    elif self.dir == "left":
      self.dir = "right"
    else:
      self.dir = "left"

  def burst(self):
    pos = (self.x, self.y)
    status = self.map[pos]
    if status == "clean":
      self.turn_left()
      self.map[pos] = "weakened"
    elif status == "weakened":
      self.map[pos] = "infected"
      self.make_node_infected_count += 1
    elif status == "infected":
      self.turn_right()
      self.map[pos] = "flagged"
    elif status == "flagged":
      self.reverse_dir()
      self.map[pos] = "clean"
    self.move()

def solve_part2(input):
  vce = VirusCarrierEvolved(input)
  for i in range(10000000):
    vce.burst()
  return vce.make_node_infected_count

# print(solve_part2(test) == 2511944)

# print(solve_part2(input))
# 2511640


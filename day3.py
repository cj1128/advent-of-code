from math import sqrt, ceil

# 以`square 1`为原点，计算数字的坐标
# 比如，2的坐标为(1, 0)，12的坐标为(1, 1)
# 这里的算法采用折叠法，对于任意一个数字，从原点出发，先全部向右，第一圈半径为1
# 比如9，初始坐标为(8, 0)
# 因为比半径大，所以将其折叠，向上，坐标变为(1, 7)
# 再向左折叠，坐标变为(-5, 1)
# 再向下折叠，坐标变为(-1, -3)
# 再向右折叠，坐标变为(1, -1)，此时坐标在半径内，为合法坐标，因此这就是最终坐标
# 如果还不行，增大半径，再折叠，重复这个过程
def get_num_coor(num):
  def is_valid(s, x, y):
    return -s <= x <= s and -s <= y <= s

  max_r = ceil(sqrt(num)) // 2
  x = num -1
  y = 0
  for r in range(1, max_r+1):
    # up
    y = (x - r) + y
    x = r
    if is_valid(r, x, y):
      break

    # left
    x = x - (y - r)
    y = r
    if is_valid(r, x, y):
      break

    # down
    y = y - (-r - x)
    x = -r
    if is_valid(r, x, y):
      break

    # right
    x = x + (-r - y)
    y = -r
    if is_valid(r, x, y):
      break

  return (x, y)

def solve_part1(num):
  x, y = get_num_coor(num)
  return abs(x) + abs(y)

# print(solve_part1(289326))

def squre_coor_seq(num):
  if num <= 0:
    return

  x = 0
  y = 0
  r = 1
  direction = "right"

  for _ in range(num):
    yield (x, y)

    if direction == "right":
      x += 1
    elif direction == "up":
      y += 1
    elif direction == "left":
      x -= 1
    elif direction == "down":
      y -= 1

    if direction == "right" and x > r:
      x -= 1
      y += 1
      direction = "up"
      continue

    if direction == "up" and y > r:
      y -= 1
      x -= 1
      direction = "left"
      continue

    if direction == "left" and x < -r:
      x += 1
      y -= 1
      direction = "down"
      continue

    if direction == "down" and y < -r:
      y += 1
      x += 1
      r += 1
      direction = "right"
      continue

def squre_value_seq(num):
  if num <= 0:
    return

  yield 1
  # map coor to value
  coor_value = {(0, 0): 1}
  coor_seq = squre_coor_seq(num)
  next(coor_seq)
  for i in range(2, num+1):
    x, y = next(coor_seq)
    v = 0
    for nx, ny in [(x - dx, y - dy) for dx in [-1, 0, 1] for dy in [-1, 0, 1]]:
      if coor_value.get((nx, ny)):
        v += coor_value.get((nx, ny))
    coor_value[(x, y)] = v
    yield v

def solve_part2(num):
  for x in squre_value_seq(num):
    if x >= num:
      return x

print(solve_part2(289326))

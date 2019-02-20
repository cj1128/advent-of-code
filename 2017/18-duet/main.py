import re
from collections import defaultdict
from queue import Queue, Empty
from threading import Thread

input = """
set i 31
set a 1
mul p 17
jgz p p
mul a 2
add i -1
jgz i -2
add a -1
set i 127
set p 680
mul p 8505
mod p a
mul p 129749
add p 12345
mod p a
set b p
mod b 10000
snd b
add i -1
jgz i -9
jgz a 3
rcv b
jgz b -1
set f 0
set i 126
rcv a
rcv b
set p a
mul p -1
add p b
jgz p 4
snd a
set a b
jgz 1 3
snd b
set f 1
add i -1
jgz i -11
snd a
jgz f -16
jgz a -19
"""

part1_test = ("""
set a 1
add a 2
mul a a
mod a 5
snd a
set a 0
rcv a
jgz a -1
set a 1
jgz a -2
""", 4)

def parse_ins(ins):
  operation, left, right, *_ = ins.split(" ") + [None]
  try:
    left = int(left)
  except ValueError:
    pass
  if right is not None:
    try:
      right = int(right)
    except ValueError:
      pass
  return operation, left, right

def get_value(regs, value_or_reg):
  if isinstance(value_or_reg, int):
    return value_or_reg
  return regs[value_or_reg]

def solve_part1(input):
  instructions = input.strip().split("\n")
  pc = 0
  regs = defaultdict(lambda: 0)
  frequency = None
  while pc >=0 and pc < len(instructions):
    ins = instructions[pc]
    if pc < 0 or pc >= len(instructions):
      break
    operation, left, right = parse_ins(ins)
    if operation == "set":
      regs[left] = get_value(regs, right)
    elif operation == "snd":
      frequency = get_value(regs, left)
    elif operation == "add":
      regs[left] = regs[left] + get_value(regs, right)
    elif operation == "mul":
      regs[left] = regs[left] * get_value(regs, right)
    elif operation == "mod":
      regs[left] = regs[left] % get_value(regs, right)
    elif operation == "rcv":
      if get_value(regs, left) != 0:
        return frequency
    elif operation == "jgz":
      if get_value(regs, left) > 0:
        pc += get_value(regs, right)
        continue
    pc += 1

# print(solve_part1(part1_test[0]) == part1_test[1])
# print(solve_part1(input))
# 3188

def meta_worker(q0, q1, meta_queue):
  d = {0: 0, 1: 0}
  while True:
    num, status = meta_queue.get()
    if status == "rcv":
      d[num] += 1
    if status == "snd":
      d[1-num] -= 1
    # dead lock
    if d[0] >0 and d[1] > 0:
      q0.put(None)
      q1.put(None)
      break

def solve_part2(input):
  instructions = input.strip().split("\n")
  q0 = Queue()
  q1 = Queue()
  meta_queue = Queue()
  result = 0
  def worker(num, input_queue, output_queue, meta_queue):
    nonlocal result
    pc = 0
    regs = defaultdict(lambda: 0)
    regs["p"] = num
    while pc >=0 and pc < len(instructions):
      ins = instructions[pc]
      if pc < 0 or pc >= len(instructions):
        break
      operation, left, right = parse_ins(ins)
      if operation == "set":
        regs[left] = get_value(regs, right)
      elif operation == "snd":
        meta_queue.put((num, "snd"))
        output_queue.put_nowait(get_value(regs, left))
        if num == 1:
          result = result + 1
      elif operation == "add":
        regs[left] = regs[left] + get_value(regs, right)
      elif operation == "mul":
        regs[left] = regs[left] * get_value(regs, right)
      elif operation == "mod":
        regs[left] = regs[left] % get_value(regs, right)
      elif operation == "rcv":
        meta_queue.put((num, "rcv"))
        value = input_queue.get()
        if value is None:
          break
        else:
          regs[left] = value
      elif operation == "jgz":
        if get_value(regs, left) > 0:
          pc += get_value(regs, right)
          continue
      pc += 1

  p0 = Thread(target=worker, args=(0, q1, q0, meta_queue))
  p1 = Thread(target=worker, args=(1, q0, q1, meta_queue))
  p_meta = Thread(target=meta_worker, args=(q0, q1, meta_queue))
  p0.start()
  p1.start()
  p_meta.start()
  p0.join()
  p1.join()
  p_meta.join()
  return result

part2_test = ("""
snd 1
snd 2
snd p
rcv a
rcv b
rcv c
rcv d
""", 3)

# print(solve_part2(part2_test[0]) == part2_test[1])
print(solve_part2(input))
# 7112

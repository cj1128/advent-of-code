from collections import defaultdict

input = """
set b 67
set c b
jnz a 2
jnz 1 5
mul b 100
sub b -100000
set c b
sub c -17000
set f 1
set d 2
set e 2
set g d
mul g e
sub g b
jnz g 2
set f 0
sub e -1
set g e
sub g b
jnz g -8
sub d -1
set g d
sub g b
jnz g -13
jnz f 2
sub h -1
set g b
sub g c
jnz g 2
jnz 1 3
sub b -17
jnz 1 -23
"""

def parse_ins(ins):
  operation, left, right = ins.split(" ")
  try:
    left = int(left)
  except ValueError:
    pass
  try:
    right = int(right)
  except ValueError:
    pass
  return operation, left, right

def get_value(regs, value_or_reg):
  if isinstance(value_or_reg, int):
    return value_or_reg
  return regs[value_or_reg]

def solve_part1():
  instructions = [parse_ins(ins) for ins in input.strip().split("\n")]
  length = len(instructions)
  pc = 0
  mul_invoked = 0
  regs = defaultdict(lambda: 0)
  while pc >=0 and pc < length:
    ins = instructions[pc]
    operation, left, right = ins
    if operation == "set":
      regs[left] = get_value(regs, right)
    elif operation == "sub":
      regs[left] -= get_value(regs, right)
    elif operation == "mul":
      mul_invoked += 1
      regs[left] *= get_value(regs, right)
    elif operation == "jnz":
      if get_value(regs, left) != 0:
        pc += get_value(regs, right)
        continue
    pc += 1

  print(mul_invoked)

# solve_part1()
# 4225

def solve_part2():
  instructions = [parse_ins(ins) for ins in input.strip().split("\n")]
  length = len(instructions)
  pc = 0
  regs = defaultdict(lambda: 0)
  regs["a"] = 1
  while pc >=0 and pc < length:
    print(pc, regs["d"], regs["g"], regs["b"], regs["c"], regs["f"], regs["h"])
    ins = instructions[pc]
    operation, left, right = ins
    if operation == "set":
      regs[left] = get_value(regs, right)
    elif operation == "sub":
      regs[left] -= get_value(regs, right)
    elif operation == "mul":
      regs[left] *= get_value(regs, right)
    elif operation == "jnz":
      if get_value(regs, left) != 0:
        pc += get_value(regs, right)
        continue
    pc += 1

  print(regs["h"])

# 通过打印发现，一开始程序在`jnz g -8`这里来回跳转
# 打印寄存器变量发现`g`的值从-106697开始慢慢增加，因此这个需要跳转很多次
# 我们可以手动优化掉
# `jnz g -8`指令后面的指令用到的寄存器是`d`, `g`, `b`, `c`, `f`
# 因此我们可以将以上寄存器设置好初始值，直接从`jnz g -8`后面开始执行
# solve_part2()

def solve_part2_optimized():
  instructions = [parse_ins(ins) for ins in input.strip().split("\n")]
  length = len(instructions)
  regs = defaultdict(lambda: 0)
  regs["a"] = 1
  regs["d"] = 2
  regs["g"] = 0
  regs["b"] = 106734
  regs["c"] = 123700
  regs["f"] = 1
  pc = 19
  while pc >=0 and pc < length:
    print(pc, regs["d"], regs["g"], regs["b"], regs["c"], regs["f"], regs["h"])
    ins = instructions[pc]
    operation, left, right = ins
    if operation == "set":
      regs[left] = get_value(regs, right)
    elif operation == "sub":
      regs[left] -= get_value(regs, right)
    elif operation == "mul":
      regs[left] *= get_value(regs, right)
    elif operation == "jnz":
      if get_value(regs, left) != 0:
        pc += get_value(regs, right)
        continue
    pc += 1

  print(regs["h"])

# 发现程序又开始了一个大循环，跳转从`jnz g -13`开始
# 这次`d`寄存器的值改了
# 所以很容易猜到这是一个嵌套循环
# 观察可以发现其他的类似规律
# solve_part2_optimized()

def solve_part2_final():
  instructions = [parse_ins(ins) for ins in input.strip().split("\n")]
  length = len(instructions)
  regs = defaultdict(lambda: 0)
  regs["a"] = 1
  regs["d"] = 106784
  regs["g"] = 0
  regs["b"] = 106785
  regs["c"] = 123700
  regs["f"] = 1
  pc = 19
  while pc >=0 and pc < length:
    print(pc, regs["d"], regs["g"], regs["b"], regs["c"], regs["f"], regs["h"])
    ins = instructions[pc]
    operation, left, right = ins
    if operation == "set":
      regs[left] = get_value(regs, right)
    elif operation == "sub":
      regs[left] -= get_value(regs, right)
    elif operation == "mul":
      regs[left] *= get_value(regs, right)
    elif operation == "jnz":
      if get_value(regs, left) != 0:
        pc += get_value(regs, right)
        continue
    pc += 1

  print(regs["h"])

solve_part2_final()

from functools import reduce
from operator import xor

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

def know_hash(str):
  lengths = [ord(c) for c in str] + [17, 31, 73, 47, 23]
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

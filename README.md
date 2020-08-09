<div align="center">
  <h1>
    <a href="http://adventofcode.com/">
      Advent of Code
    </a>
  </h1>
</div>

> Advent of Code is a series of small programming puzzles for a variety of skill levels. They are self-contained and are just as appropriate for an expert who wants to stay sharp as they are for a beginner who is just learning to code. Each puzzle calls upon different skills and has two parts that build on a theme.

Representation of difficulty:

- 😄 : a piece of cake, so straightforward.
- 😞 : need some time, maybe 30 minutes.
- 😭 : kind of hard, need 1 \~ 2 hours.
- 😈 : god damn it, this is so hard!

## TOC

<!-- MarkdownTOC -->

- [2018](#2018)
  - [😄 01](#%F0%9F%98%84-01)
  - [😞 02](#%F0%9F%98%9E-02)
  - [😞 03](#%F0%9F%98%9E-03)
  - [😭 04](#%F0%9F%98%AD-04)
  - [😞 05](#%F0%9F%98%9E-05)

<!-- /MarkdownTOC -->

## 2018

The rust version is heavily based on **the awesome [work](https://github.com/BurntSushi/advent-of-code) of BurntSushi**, who is the author of the awesome tool [ripgrep](https://github.com/BurntSushi/ripgrep), which is the best search tool IMHO.

### 😄 [01](https://adventofcode.com/2018/day/1)

Part 1:

```
sum = 0
for line in input:
  sum += parse(line)

result = sum
```

Part 2:

```
seen = Set<int>
freq = 0
loop
  for line in input:
    freq += parse(line)
    if seen.has(freq):
      result = freq
      return

    seen.insert(freq)
```

### 😞 [02](https://adventofcode.com/2018/day/2)

Part 1:

```text
freq = [0; 256]
twos = 0
thress = 0

for line in input:
  clear_to_zero(freq)

  for byte in line:
    freq[byte] += 1

  if freq.any(x => x == 2):
    twos += 1

  if freq.any(x => x == 3):
    thress += 1

result = twos * threes
```

Part 2, I don't even bother to think a fancy algorithm, maybe there is one there.

> When in doubt, use brute force. - Ken Thompson

```
lines = input.split()
for i in 0 .. lines.len():
  for j in i + 1 .. lines.len():
    if differ_by_exactly_one_char(lines[i], lines[j]):
      result = get_common_part(lines[i], lines[j])
      return
```

### 😞 [03](https://adventofcode.com/2018/day/3)

Preparation:

```
grid = Hash<point, int>

for line in input:
  x, y, width, height = parse(line)
  for point in rect defined by {x, y, width, height}:
    grid[point] += 1
```

Part 1:

```
count = 0
for point, value in grid:
  if value > 1:
    count++

result = count
```

Part 2:

```
for line in input:
  id, x, y, width, height = parse(line)

  if grid[point] == 1 for all pint in rect defined by {x, y, width, height}:
    result = id
    return
```

### 😭 [04](https://adventofcode.com/2018/day/4)

Preparation:

```
events = [Event]
for line in input:
  events.push(parse(line))

events.sort(by datetime)
events_by_guard = Hash<GuardID, [Event]>

cur_id = null
for event in events:
  if event.type == "start shift":
    cur_id = event.id
  else:
    events_by_guard[cur_id].push(event)

sleep_frequency = Hash<GuradID, [0; 60]>
for id, events in events_by_guard:
  freq = [0; 60]

  for range in parse(events):
    for minute in range:
      freq[minute] += 1

  sleep_frequency[id] = freq
```

Part 1:

```
(sleepiest_guard, _) = sleep_frequency
  .iter()
  .max_by((id, freq) => sum(freq))

(sleepiest_minute, _) = sleep_frequency[sleepiest_guard]
  .iter_with_index()
  .max_by((minute, value) => value)

result = sleepiest_guard * sleepiest_minute
```

Part 2:

```
sleepiest_minutes = Hash<GuardID, (u32, u32)>
for id, freq in sleep_frequency:
  sleepiest_minute = find sleepiest minute in freq like part 1
  sleepiest_minutes[id] = (minute, freq[minute])

(guard_id, (minute, value)) = sleepiest_minutes
  .iter()
  .max_by((id, (minute, value)) => value)

result = guard_id * minute
```

### 😞 [05](https://adventofcode.com/2018/day/5)

Part 1:

```text
reacted_string = ""

loop:
  reacted = false

  i = 0

  while i < input.len() - 1:
    if can_react(input[index], input[index+1]):
      reacted = true
      i += 2
    else:
      reacted_string.push(input[index])
      i += 1

  // do not forget the last char
  if i == input.len() - 1:
    reacted_string.push(input[i])

  swap(input, reacted_string)
  reacted_string = ""

  if !reacted:
    break

result = reacted_string.len()
```

Part 2:

```text
best = input.len()

for c in 'a'..'z':
  test_input = input.remove(c).remove(c.upper())
  reacted = react test_input like part 1
  if reacted.len() < best:
    best = reacted.len()

result = best
```

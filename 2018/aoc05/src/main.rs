use std::io::{self, Read};
use std::mem;

type Result<T> = std::result::Result<T, Box<dyn std::error::Error>>;

fn main() -> Result<()> {
  let mut input = String::new();
  io::stdin().read_to_string(&mut input)?;

  // Remove trailing newline
  let input_trimed = input.trim_end();

  part1(&input_trimed)?;

  part2(&input_trimed)?;

  Ok(())
}

fn part1(polymer: &str) -> Result<()> {
  println!("part 1: {}", react(polymer).len());
  Ok(())
}

fn part2(polymer: &str) -> Result<()> {
  let mut best = polymer.len();

  for c in b'A'..b'Z' {
    let unit1 = c as char;
    let unit2 = (c + 32) as char;
    let reduced_polymer = polymer.replace(unit1, "").replace(unit2, "");
    let reacted = react(&reduced_polymer);
    if reacted.len() < best {
      best = reacted.len();
    }
  }

  println!("part 2: {}", best);
  Ok(())
}

fn react(polymer_str: &str) -> String {
  let mut polymer = polymer_str.as_bytes().to_vec();
  let mut reacted_polyer = vec![];

  loop {
    let mut reacted = false;
    let mut i = 0;

    while i < polymer.len() - 1 {
      if reacts(polymer[i], polymer[i + 1]) {
        reacted = true;
        i += 2;
        continue;
      }

      reacted_polyer.push(polymer[i]);
      i += 1;
    }

    if i == polymer.len() - 1 {
      reacted_polyer.push(polymer[i]);
    }

    mem::swap(&mut polymer, &mut reacted_polyer);
    reacted_polyer.clear();

    if !reacted {
      break;
    }
  }

  // We only remove ASCII bytes, which is guaranteed to preserve
  // the UTF-8 validity
  return String::from_utf8(polymer).unwrap();
}

fn reacts(a: u8, b: u8) -> bool {
  if (a >= b'A' && a <= b'z') && (b >= b'A' && b <= b'z') {
    if a >= b {
      a - b == 32
    } else {
      b - a == 32
    }
  } else {
    false
  }
}

use std::io::{self, Read};

type Result<T> = ::std::result::Result<T, Box<dyn ::std::error::Error>>;

fn main() -> Result<()> {
  let mut input = String::new();
  io::stdin().read_to_string(&mut input)?;

  part1(&input)?;
  part2(&input)?;

  Ok(())
}

fn part1(input: &str) -> Result<()> {
  let mut frequency = [0u8; 256];
  let mut twos = 0;
  let mut threes = 0;

  for line in input.lines() {
    if !line.is_ascii() {
      return Err(From::from("part 1 only supports ascii input"));
    }

    for f in frequency.iter_mut() {
      *f = 0;
    }

    for b in line.as_bytes().iter().map(|&x| x as usize) {
      frequency[b] = frequency[b].saturating_add(1);
    }

    if frequency.iter().any(|&x| x == 2) {
      twos += 1;
    }

    if frequency.iter().any(|&x| x == 3) {
      threes += 1;
    }
  }

  println!("part 1: {}", twos * threes);

  Ok(())
}

fn part2(input: &str) -> Result<()> {
  let ids: Vec<&str> = input.lines().collect();

  for i in 0..ids.len() {
    for j in i + 1..ids.len() {
      if let Some(common) = common_correct_chars(ids[i], ids[j]) {
        println!("part 2: {}", common);
        return Ok(());
      }
    }
  }

  Err(From::from("part 2: could not find correct ids"))
}

fn common_correct_chars(id1: &str, id2: &str) -> Option<String> {
  if id1.len() != id2.len() {
    return None;
  }

  let mut found_one_wrong = false;

  for (c1, c2) in id1.chars().zip(id2.chars()) {
    if c1 != c2 {
      if found_one_wrong {
        return None;
      }

      found_one_wrong = true;
    }
  }

  Some(
    id1
      .chars()
      .zip(id2.chars())
      .filter(|&(c1, c2)| c1 == c2)
      .map(|(c, _)| c)
      .collect(),
  )
}

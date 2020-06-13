#[macro_use]
extern crate lazy_static;
extern crate regex;

use regex::Regex;
use std::collections::HashMap;
use std::error::Error;
use std::io::{self, Read};
use std::str::FromStr;

type Result<T> = ::std::result::Result<T, Box<dyn Error>>;
type Grid = HashMap<(u32, u32), u32>;

macro_rules! err {
  ($($tt:tt)*) => { Err(Box::<dyn Error>::from(format!($($tt)*))) }
}

fn main() -> Result<()> {
  let mut input = String::new();
  io::stdin().read_to_string(&mut input)?;

  let mut claims: Vec<Claim> = vec![];
  for line in input.lines() {
    let claim = line
      .parse()
      .or_else(|err| err!("failed to parse '{:?}': {}", line, err))?;
    claims.push(claim);
  }

  let mut grid = Grid::new();

  for claim in &claims {
    for (x, y) in claim.iter_points() {
      *grid.entry((x, y)).or_default() += 1;
    }
  }

  part1(&grid)?;
  part2(&claims, &grid)?;

  Ok(())
}

fn part1(grid: &Grid) -> Result<()> {
  let count = grid.values().filter(|&&count| count > 1).count();
  println!("part 1: {}", count);
  Ok(())
}

fn part2(claims: &[Claim], grid: &Grid) -> Result<()> {
  for claim in claims {
    if claim.iter_points().all(|p| grid[&p] == 1) {
      println!("part 2: {}", claim.id);
      return Ok(());
    }
  }

  err!("no solution found for part 2")
}

#[derive(Debug)]
struct Claim {
  id: u32,
  x: u32,
  y: u32,
  width: u32,
  height: u32,
}

struct IterPoints<'c> {
  claim: &'c Claim,
  px: u32,
  py: u32,
}

impl<'c> Iterator for IterPoints<'c> {
  type Item = (u32, u32);

  fn next(&mut self) -> Option<(u32, u32)> {
    if self.py >= self.claim.y + self.claim.height {
      self.py = self.claim.y;
      self.px += 1;
    }

    if self.px >= self.claim.x + self.claim.width {
      return None;
    }

    let (px, py) = (self.px, self.py);
    self.py += 1;
    Some((px, py))
  }
}

impl Claim {
  fn iter_points(&self) -> IterPoints {
    IterPoints {
      claim: self,
      px: self.x,
      py: self.y,
    }
  }
}

impl FromStr for Claim {
  type Err = Box<dyn Error>;

  fn from_str(s: &str) -> Result<Claim> {
    // #1 @ 555,891: 18x12
    lazy_static! {
      static ref RE: Regex = Regex::new(
        r"(?x)
          \#
          (?P<id>\d+)
          \s+@\s+
          (?P<x>\d+),(?P<y>\d+):
          \s+
          (?P<width>\d+)x(?P<height>\d+)
        "
      )
      .unwrap();
    }

    let caps = match RE.captures(s) {
      None => return err!("unrecognized claim"),
      Some(caps) => caps,
    };

    Ok(Claim {
      id: caps["id"].parse()?,
      x: caps["x"].parse()?,
      y: caps["y"].parse()?,
      width: caps["width"].parse()?,
      height: caps["height"].parse()?,
    })
  }
}

#[macro_use]
extern crate lazy_static;
extern crate regex;

use regex::Regex;
use std::error::Error;
use std::collections::HashMap;
use std::str::{FromStr};
use std::slice;
use std::io::{self, Read};
use std::ops::Range;

type Result<T> = std::result::Result<T, Box<dyn Error>>;

macro_rules! err {
  ($($tt:tt)*) => { Err(Box::<dyn Error>::from(format!($($tt)*))) }
}

fn main() -> Result<()> {
  let mut input = String::new();
  io::stdin().read_to_string(&mut input)?;

  let mut events: Vec<Event> = vec![];
  for line in input.lines() {
    let event = line
      .parse()
      .or_else(|err| err!("failed to parse '{:?}': {}", line, err))?;
    events.push(event);
  }

  if events.is_empty() {
    return err!("found no events");
  }

  // sort events by time and group them by guard
  events.sort_by(|e1, e2| e1.datetime.cmp(&e2.datetime));

  let mut events_by_guard = HashMap::<GuardID, Vec<Event>>::new();
  let mut cur_guard_id = None;

  for evt in events {
    if let EventKind::StartShift { guard_id } = evt.kind {
      cur_guard_id = Some(guard_id);
      continue;
    }

    if let Some(id) = cur_guard_id {
      events_by_guard.entry(id).or_default().push(evt);
    } else {
      return err!("no guard id set for the event");
    }
  }

  let mut sleep_frequency = GuardSleepFrequency::new();
  for (&guard_id, events) in events_by_guard.iter() {
    let mut frequency: [u32; 60] = [0; 60];

    for range in MinutesAsleepIter::new(events) {
      for minute in range? {
        frequency[minute as usize] += 1;
      }
    }

    sleep_frequency.insert(guard_id, frequency);
  }

  part1(&sleep_frequency)?;
  part2(&sleep_frequency)?;

  Ok(())
}

fn part1(sleep_frequency: &GuardSleepFrequency) -> Result<()> {
  let (&sleepiest, _) = sleep_frequency
    .iter()
    .max_by_key(|(_, ref freqs)| -> u32 { freqs.iter().sum() })
    // unwrap is ok since we are guaranteed to have at least one event
    .unwrap();

  let minute = sleepiest_minute(sleep_frequency, sleepiest);

  println!(
    "part 1: guard id: {}, minute: {}, result: {}",
    sleepiest,
    minute,
    sleepiest * minute as u32
  );

  Ok(())
}

fn part2(sleep_frequency: &GuardSleepFrequency) -> Result<()> {
  let mut sleepiest_minutes: HashMap<GuardID, (u32, u32)> = HashMap::new();

  for (&guard_id, freqs) in sleep_frequency {
    let minute = sleepiest_minute(sleep_frequency, guard_id);

    let count = freqs[minute as usize];

    sleepiest_minutes.insert(guard_id, (minute, count));
  }

  let (sleepiest_guard_id, (minute, value)) = sleepiest_minutes
    .iter()
    .max_by_key(|(_, &(_, count))| -> u32 { count })
    // unwrap is ok since sleepiest_minutes is not empty
    .unwrap();

  println!(
    "part 2: guard id: {}, minute: {}, value: {}, result: {}",
    sleepiest_guard_id,
    minute,
    value,
    sleepiest_guard_id * minute,
  );

  Ok(())
}

fn sleepiest_minute(sleep_frequency: &GuardSleepFrequency, guard_id: GuardID) -> u32 {
  let (minute, _) = sleep_frequency[&guard_id]
    .iter()
    .enumerate()
    .max_by_key(|(_, val)| -> u32 { **val })
    .unwrap();

  minute as u32
}

type GuardSleepFrequency = HashMap<GuardID, [u32; 60]>;

#[derive(Debug)]
struct Event {
  datetime: DateTime,
  kind: EventKind,
}

#[derive(Debug, PartialEq, Eq, PartialOrd, Ord)]
struct DateTime {
  year: u32,
  month: u32,
  day: u32,
  hour: u32,
  minute: u32,
}

type GuardID = u32;

#[derive(Debug)]
enum EventKind {
  StartShift { guard_id: GuardID },
  FallAsleep,
  WakeUp,
}

struct MinutesAsleepIter<'a> {
  events: slice::Iter<'a, Event>,
  fell_asleep: Option<u32>,
}

impl<'a> MinutesAsleepIter<'a> {
  fn new(events: &'a [Event]) -> MinutesAsleepIter<'a> {
    MinutesAsleepIter {
      events: events.iter(),
      fell_asleep: None,
    }
  }
}

impl<'a> Iterator for MinutesAsleepIter<'a> {
  type Item = Result<Range<u32>>;

  fn next(&mut self) -> Option<Result<Range<u32>>> {
    loop {
      let evt = match self.events.next() {
        Some(evt) => evt,
        None => {
          if self.fell_asleep.is_some() {
            return Some(err!("found sleep event without wake up"));
          }

          return None;
        }
      };

      match evt.kind {
        EventKind::StartShift { .. } => panic!("should never happen"),

        EventKind::FallAsleep => {
          if self.fell_asleep.is_some() {
            return Some(err!("found continuous asleep event"));
          }

          self.fell_asleep = Some(evt.datetime.minute);
        }

        EventKind::WakeUp => {
          let fell_asleep = match self.fell_asleep.take() {
            Some(minute) => minute,
            None => {
              return Some(err!("found wakeup without sleep"));
            }
          };

          if evt.datetime.minute < fell_asleep {
            return Some(err!("found wakeup before sleep"));
          }

          return Some(Ok(fell_asleep..evt.datetime.minute));
        }
      }
    }
  }
}

impl FromStr for Event {
  type Err = Box<dyn Error>;

  fn from_str(s: &str) -> Result<Event> {
    lazy_static! {
      // [1518-11-01 00:00] Guard #10 begins shift
      // [1518-11-01 00:05] falls asleep
      // [1518-11-01 00:25] wakes up
      static ref RE: Regex = Regex::new(
        r"(?x)
          \[(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})\ (?P<hour>\d{2}):(?P<minute>\d{2})\]
          \s+
          (Guard\ \#(?P<guard_id>\d+)\ begins\ shift|(?P<sleep>.+))
        "
      ).unwrap();
    }

    let caps = match RE.captures(s) {
      None => return err!("unrecognized event"),
      Some(caps) => caps,
    };

    let datetime = DateTime {
      year: caps["year"].parse()?,
      month: caps["month"].parse()?,
      day: caps["day"].parse()?,
      hour: caps["hour"].parse()?,
      minute: caps["minute"].parse()?,
    };

    let kind = if let Some(m) = caps.name("guard_id") {
      EventKind::StartShift {
        guard_id: m.as_str().parse()?,
      }
    } else if &caps["sleep"] == "falls asleep" {
      EventKind::FallAsleep
    } else if &caps["sleep"] == "wakes up" {
      EventKind::WakeUp
    } else {
      return err!("could not determine event kind");
    };

    Ok(Event { datetime, kind })
  }
}

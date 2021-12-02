/*
 * day2part2.rs - Solution for Advent of Code 2021 Day 2 part 2

 * See Python solution for more "why" explanations; this is mostly a "how" exercise.
 *
 * The problem is so simple today that it's not really worth decomposing except for practical
 * matters....
 */
use std::{
  fs::File,
  io::{prelude::*, BufReader},
  path::Path,
};

// ----------------------------------------------------------------
fn main() {
    //let fpath = Path::new("data/day2test.txt");
    let fpath = Path::new("data/day2part1.txt");

    let file = match File::open(&fpath) {
        Err(why) => panic!("couldn't open {}: {}", fpath.display(), why),
        Ok(file) => file,
    };

    let mut good_cmds: usize = 0;
    let mut horizontal: usize = 0;
    let mut aim: usize = 0;
    let mut depth: usize = 0;

    let commands = BufReader::new(file);
    for command in commands.lines() {
        let command = command.expect("Unable to read line from file");
        //Split into pieces by space, parse out the command and the size with appropriate types
        let part: Vec<&str> = command.split(" ").collect();
        let cmd: &str = part[0];
        let size: usize = part[1].parse().unwrap();
        good_cmds += 1;
        match cmd{
            "forward" => {
                horizontal += size;
                depth += aim * size;
            },
            "down" => aim += size,
            "up"   => aim -= size,
            _ => good_cmds -= 1,
        }
    }
    let position_product: usize = horizontal * depth;
    println!("Final position after {} valid commands is horizontal = {}, depth = {}",good_cmds,horizontal,depth);
    println!("Position Product is therefore: {}",position_product);

}

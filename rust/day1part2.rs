/*
 * day1part2.rs - Solution for Advent of Code 2021 Day 1 part 2
 *
 * Why? Because I can.
 */

 use std::{
     fs::File,
     io::{prelude::*, BufReader},
     path::Path,
 };

 // ----------------------------------------------------------------
 fn read_file_of_sonar_readings_to_array(f_name : impl AsRef<Path>) -> Vec<i32> {
     let file = File::open(f_name).expect("Unable to open file");
     let b = BufReader::new(file);
     let mut readings: Vec<i32> = Vec::new();
     for line in b.lines() {
         let line = line.expect("Unable to read line");
         let num: i32 = line.parse().unwrap();
         if num > 0 {
             readings.push(num)
         }
     }
     return readings;
}

// ----------------------------------------------------------------
fn coalesce_readings_to_windows(readings: &Vec<i32>, windowsize: usize) -> Vec<i32> {
    let mut windows: Vec<i32> = Vec::new();

    for i in 0..readings.len() {
        windows.push(readings[i]);
        if i < windowsize {
            for j in 0..(windows.len()-1) {
                windows[j] = windows[j] + readings[i];
            }
        } else {
            for j in (windows.len() - windowsize)..(windows.len()-1) {
                windows[j] = windows[j] + readings[i];
            }
        }
    }

    //TODO truncate windowsize-1 entries from end.
    return windows[0..(windows.len() - windowsize + 1)].to_vec();
}

// ----------------------------------------------------------------
fn calculate_increases_in_windows(windows: &Vec<i32>) -> i32 {
    let mut increases: i32 = 0;
    for i in 0..windows.len() {
        if i>0 {
            if windows[i] > windows[i-1] {
                increases = increases+1;
            }
        }
    }
    return increases;
}

// ----------------------------------------------------------------
// ----------------------------------------------------------------
// ----------------------------------------------------------------
fn main() {
     //let readings: Vec<i32> = read_file_of_sonar_readings_to_array("data/day1test.txt");
     let readings: Vec<i32> = read_file_of_sonar_readings_to_array("data/day1part1.txt");
     let windows:  Vec<i32> = coalesce_readings_to_windows(&readings,3);
     //println!("{:?}",readings);
     //println!("{:?}",windows);
     //println!("File contained {} entries, coalesced to {} windows", readings.len(), windows.len());
     println!("Over {} measurement windows, found {} reading increases", windows.len(), calculate_increases_in_windows(&windows));
}

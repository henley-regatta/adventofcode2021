#!/usr/bin/env node
/*
 * A Javascript / NodeJS implementation of AOC 2021 Day 1 Part 2
 * with sliding windows and everything.
 *
 * Mainly to prove I can.
 */

fs = require('fs');

//const inputfile = "data/day1test.txt";
const inputfile = "data/day1part1.txt";

const readings = fs.readFileSync(inputfile,'UTF-8').split(/\r?\n/);

const windows = [];
const winsize = 3;

readings.forEach(reading => {
  const ping = Number(reading);
  //dummy out if NaN/zero
  if(ping==0) { return }
  windows.push(ping);
  ptr = windows.length;
  if(ptr < winsize) {
    i=0;
    while(i<(ptr-1)) {
      windows[i] = windows[i] + ping;
      i++;
    }
  } else {
    m=ptr-winsize;
    while(m<(ptr-1)) {
      windows[m] = windows[m] + ping;
      m++;
    }
  }
});
//Last winsize-1 entries are incomplete and should be removed
const compWindows = windows.slice(0,(windows.length - winsize + 1))

//And for the comparison we just need to iterate over the elements comparing
//to last:
increases = 0;
for(var i = 0; i<=compWindows.length; i++) {
  if(i==0) { continue } //can't do anything with first entry
  if(compWindows[i] > compWindows[i-1]) { increases++; }
}
console.log("Over " + compWindows.length + " measurement windows, found " + increases + " reading increases.")

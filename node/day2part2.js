#!/usr/bin/env node
/*
 * A Javascript / NodeJS implementation of AOC 2021 Day 2 Part 2
 *
 * Mainly to prove I can.
 *
 * Algorithm is a direct clone of that used in python/day2part2.py so for
 * explanations see there.
 */

fs = require('fs');

//const inputfile = "data/day2test.txt";
const inputfile = "data/day2part1.txt";

const commands  = fs.readFileSync(inputfile,'UTF-8').split(/\r?\n/);

cmdCount = 0;
horizontal = 0;
aim = 0;
depth = 0;

commands.forEach(command => {
  cmdCount++;
  const cmd = command.split(" ",2);
  const size = Number(cmd[1]);
  switch(cmd[0].toLowerCase()) {
    case "forward" :
      horizontal += size;
      depth += (aim * size);
      if(depth < 0) { depth = 0};
      break;
    case "down" :
      aim += size;
      break;
    case "up" :
      aim -= size;
      break;
    default :
      //console.log("Unable to parse command " + command + " -  I got cmd=" + cmd[0] + ", size=" + size);
      cmdCount -= 1;
  }
});

const positionProduct = horizontal * depth;
console.log("Final position after " + cmdCount + " valid commands is horizontal = " + horizontal + ", depth = " + depth);
console.log("Position Product is therefore: " + positionProduct);

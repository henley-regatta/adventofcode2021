#!/usr/bin/env node
/*
 * A Javascript / NodeJS implementation of AOC 2021 Day 3 Part 2
 *
 * Mainly to prove I can.
 *
 * Trying to be a bit more node-y this time.
 */

fs = require('fs');

//const inputfile = "data/day3test.txt";
const inputfile = "data/day3part1.txt";

// ----------------------------------------------------------------------------
function readFileToBinaryArray(inputfile) {
  const strnumbers = fs.readFileSync(inputfile,'UTF-8').split(/\r?\n/);
  var binNumArray = new Array();
  strnumbers.forEach(strnum => {
    if( strnum.length > 0) {
      var numArray = new Array();
      for(var i=0; i<strnum.length; i++) {
        if(strnum.charAt(i)=='1') { numArray.push(1); }
        else { numArray.push(0);}
      }
      binNumArray.push(numArray);
    }
  })
  return binNumArray;
}

// ----------------------------------------------------------------------------
function getMostPopularValAt(inputNumbers,ndx) {
  var bitsum = 0;
  inputNumbers.forEach(binNum => {
    bitsum += binNum[ndx]
  })
  const threshold = inputNumbers.length / 2
  if(bitsum >= threshold ) { return 1 }
  return 0;
}

// ----------------------------------------------------------------------------
function filterArrayByVal(inputNumbers,ndx,val) {
  var filteredNumbers = new Array();
  inputNumbers.forEach(number => {
    if(number[ndx] == val) { filteredNumbers.push(number)}
  })
  return filteredNumbers;
}

// ----------------------------------------------------------------------------
// Attempt to "optimize" by recursing once instead of twice. Honestly I don't
// think the efficiency gain is worth the function complexity, but hey-ho.
function findCompRatings(oxyNumbers,co2Numbers,ndx) {
  const oxyfilterval=getMostPopularValAt(oxyNumbers,ndx);
  const co2filterval=Math.abs(getMostPopularValAt(co2Numbers,ndx)-1);
  var newOxyNumbers = new Array();
  var newCO2Numbers = new Array();
  if(oxyNumbers.length>1) { newOxyNumbers = filterArrayByVal(oxyNumbers,ndx,oxyfilterval); }
  else { newOxyNumbers = oxyNumbers; }
  if(co2Numbers.length>1) { newCO2Numbers = filterArrayByVal(co2Numbers,ndx,co2filterval); }
  else { newCO2Numbers = co2Numbers; }
  //Termination criteria:
  if(newOxyNumbers.length>1 || newCO2Numbers.length>1) {
    if(ndx > oxyNumbers[0].length) {
      console.log("ERROR recursing, exceeded length of number but elements remain:\noxy:"+newOxyNumbers+"\nco2:"+newCO2Numbers);
    } else {
      return findCompRatings(newOxyNumbers,newCO2Numbers,ndx+1);
    }
  } else {
    //We have a winner!
    return [newOxyNumbers[0], newCO2Numbers[0]];
  }
}

// ----------------------------------------------------------------------------
function binArrayToDecimal(binArray) {
  var decimal = 0;
  for(var i=0;i<binArray.length;i++) {
    const pow = binArray.length - i -1;
    decimal += 2**pow * binArray[i]
  }
  return decimal;
}

// ----------------------------------------------------------------------------
// MAIN
// ----------------------------------------------------------------------------
const numberList = readFileToBinaryArray(inputfile);
const solNums = findCompRatings(numberList,numberList,0);
const o2GenVal = binArrayToDecimal(solNums[0]);
const co2GenVal = binArrayToDecimal(solNums[1]);

console.log(["Oxygen Generator Rating:",o2GenVal,solNums[0],
             "CO2 Scrubber Rating:",co2GenVal,solNums[1],
             "\nLIFE SUPPORT RATING:",co2GenVal*o2GenVal].join(" "));

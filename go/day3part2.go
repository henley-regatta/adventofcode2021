package main
/*
 * day1part2.go - AOC 2021 Day 3 Part 2 in Go.
 * Implements same basic algorithm as Python version, see there for
 * explanations.
 */

import(
  "fmt"
  "os"
  "log"
  "bufio"
  "strconv"
)

// ---------------------------------------------------------------------------
func readFileToBinaryArray(filename string) [][]int {
  var binNums [][]int

  fh,err := os.Open(filename)
  if err != nil {
    log.Fatal(err)
  }
  defer fh.Close()

  s := bufio.NewScanner(fh)
  for s.Scan() {
    t := s.Text()
    var numArray []int
    for _,v := range(t) {
      n,_ := strconv.Atoi(string(v))
      numArray = append(numArray,n)
    }
    binNums = append(binNums, numArray)
  }
  return binNums
}
// -------------------------------------------------------------------------
func getMostPopularValAt(inList [][]int, ndx int) int {
  bitSum := 0
  cutoff := len(inList) / 2
  //Go integer division truncates, not rounds.
  if cutoff * 2 < len(inList) {
    cutoff += 1
  }
  for _,v := range(inList) {
    bitSum += v[ndx]
  }

  if bitSum >= cutoff {
    return 1
  } else {
    return 0
  }
}

// --------------------------------------------------------------------------
func filterArrayByVal(inNumbers [][]int, ndx int, val int) [][]int {
  var outNumbers [][]int
  for _,num := range(inNumbers) {
    if(num[ndx] == val) {
      outNumbers = append(outNumbers,num)
    }
  }
  return outNumbers
}

// -------------------------------------------------------------------------
// do this per-number; technically less efficient (more func calls)
// but the code's easier to write
func calcOxyRating(inNumbers [][]int, pos int) []int {
    selectNum := getMostPopularValAt(inNumbers,pos)

    outNumbers := filterArrayByVal(inNumbers,pos,selectNum)
    if(pos > len(inNumbers[0])) {
      log.Fatal("Failed to determine single filter value after iterating over all positions")
    }
    if(len(outNumbers)==1) {
      return outNumbers[0]
    } else {
      return calcOxyRating(outNumbers,pos+1)
    }
}
// -------------------------------------------------------------------------
func calcCO2Rating(inNumbers [][]int, pos int) []int {
    selectNum := getMostPopularValAt(inNumbers,pos) - 1
    if(selectNum < 0) {
      selectNum = 1
    }
    outNumbers := filterArrayByVal(inNumbers,pos,selectNum)
    if(pos > len(inNumbers[0])) {
      log.Fatal("Failed to determine single filter value after iterating over all positions")
    }
    if(len(outNumbers)==1) {
      return outNumbers[0]
    } else {
      return calcCO2Rating(outNumbers,pos+1)
    }
}

// -------------------------------------------------------------------------
func binArrayToDecimal(binArray []int) int {
  decimal := 0
  for i,v := range(binArray) {
    pow := len(binArray) - i -1;
    decimal += calc2Power(2,pow) * v
  }
  return decimal
}

// -------------------------------------------------------------------------
// there is math.Pow() but that involves float64 conversions....
func calc2Power(base int, exponent int) int {
  result := 1
  for exponent > 0 {
    result *= base
    exponent -= 1
  }
  return result
}

// ---------------------------------------------------------------------------
// ---------------------------------------------------------------------------
// ---------------------------------------------------------------------------
func main() {
  //var inputfile = "data/day3test.txt"
  var inputfile = "data/day3part1.txt"
  inputNumbers := readFileToBinaryArray(inputfile)

  oxyRating := calcOxyRating(inputNumbers,0)
  co2Rating := calcCO2Rating(inputNumbers,0)
  oxyNum := binArrayToDecimal(oxyRating)
  co2Num := binArrayToDecimal(co2Rating)
  fmt.Printf("Oxygen Generator Rating: %d %v CO2 Scrubber Rating: %d %v\n",oxyNum,oxyRating,co2Num,co2Rating)
  fmt.Printf("LIFE SUPPORT RATING: %d\n", oxyNum * co2Num)
}

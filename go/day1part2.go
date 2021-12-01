package main

/*
 * day1part2.go - AOC 2021 Day 1 Part 2 in Go.
 */

import(
  "fmt"
  "os"
  "log"
  "bufio"
  "strconv"
)

// -------------------------------------------------------------------------
func readFileOfSonarReadings(filename string) []int {
  var readings []int

  fh,err := os.Open(filename)
  if err != nil {
    log.Fatal(err)
  }
  defer fh.Close()

  s := bufio.NewScanner(fh)
  for s.Scan() {
    t := s.Text()
    num, _ := strconv.Atoi(t)
    readings = append(readings,num)
  }

  return readings
}

// -------------------------------------------------------------------------
func makeWindowsFromReadings(readings []int, windowsize int) []int {
  var windows []int
  for i,v := range readings {
    windows = append(windows,v)
    if(i < windowsize) {
      for j := 0; j < (len(windows)-1) ; j++ {
        windows[j] = windows[j] + v
      }
    } else {
      for j := (len(windows)-windowsize); j < (len(windows)-1); j++ {
        windows[j] = windows[j] + v
      }
    }
  }

  //Last windowsize-1 entries are incomplete and should not be returned
  return windows[0:(len(windows) - windowsize + 1)]
}

// -------------------------------------------------------------------------
func calcIncreasesInWindow(windows []int) int {
  var increases = 0
  for i,v := range windows {
    if i == 0 { continue }
    if v > windows[i-1] { increases++}
  }
  return increases
}

// -------------------------------------------------------------------------
// -------------------------------------------------------------------------
// -------------------------------------------------------------------------

func main() {
  //var readings = readFileOfSonarReadings("data/day1test.txt")
  var readings = readFileOfSonarReadings("data/day1part1.txt")
  //Part 1 output can be had by making windowsize = 1
  var windows = makeWindowsFromReadings(readings, 3)
  var increases = calcIncreasesInWindow(windows)
  //fmt.Printf("Readings: %v\nWindows: %v\n",readings,windows)
  fmt.Printf("Over %d measurement windows, found %d reading increases\n",len(windows),increases)
}

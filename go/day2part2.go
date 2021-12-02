package main
/*
 * day2part2.go - AOC 2021 Day 2 Part 2 in Go.
 * Implements same basic algorithm as Python version, see there for
 * explanations.
 */

import(
  "fmt"
  "os"
  "log"
  "bufio"
  "strconv"
  "strings"
)

// ----------------------------------------------------------------------------
func main() {

  //file IO fluster:
  //fh,err := os.Open("data/day2test.txt")
  fh,err := os.Open("data/day2part1.txt")
  if err != nil {
    log.Fatal(err)
  }
  defer fh.Close()

  var cmdCount = 0
  var horizontal = 0
  var aim = 0
  var depth = 0

  cList := bufio.NewScanner(fh)
  for cList.Scan() {
    //split line into a command & size
    fullCommand := cList.Text()
    cmd := strings.Split(fullCommand," ")
    size,_ := strconv.Atoi(cmd[1])
    cmdCount++
    switch cmd[0] {
      case "forward" : {
        horizontal += size
        depth += (aim * size)
        if depth < 0 { depth = 0}
      }
      case "down" : { aim += size }
      case "up"   : { aim -= size }
      default : { cmdCount-- }
    }
  }
  var positionProduct = horizontal * depth
  fmt.Printf("Final position after %d valid commands is horizontal = %d, depth = %d\n", cmdCount,horizontal,depth)
  fmt.Printf("Position Product is therefore: %d\n", positionProduct)

}

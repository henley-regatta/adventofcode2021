# adventofcode2021

These are my answers for the [2021 Advent of Code](https://adventofcode.com/2021)

I wasn't intending to take part in this after the time I wasted last year, but...
I quite like programming. I'm not good at it, but I enjoy it. So we'll see how we go.

Answers are structured by language (Python, Go, Rust) and named by day. I'm
expecting there to be 2 parts per day (most days) as there was last year. I could
of course be wrong.

## Python
  * `python/day1part1.py` - simple, incremental-from-read answer.
  * `python/day1part2.py` - I'm embarrassed how long it took me to come up with a
  way to do sliding-window addition but I did at least make my solution scalable
  to any window size. Always with the off-by-one errors...
  * `python/day2part1.py` - Very simple algorithm but that was all that was required.
  Actually I implement an unused instruction - `back` to go backwards. Ho hum.
  * `python/day2part2.py` - Only really a minor elaboration of the part 1 solution
  although I removed the redundant instruction, and added an unasked-for guard
  condition to prevent the submarine breaching.
  * `python/day3part1.py` - Journeyman bit-bashing, not very elegant but does the
  job. Interesting fact: Comes up with complete garbage if you feed it the day 2
  input...
  * `python/day3part2.py` - First occurrence of recursion this year. Spent way too
  long bit-bashing binary to decimal and the final solution is both ugly and inefficient.
  (first optimisation: 1 set of recursion to find both values.)

## NodeJS / JavaScript
  * `node/day1part2.js` - Look, this is a straightforward non-idiomatic translation.
  (but it does work)
  * `node/day2part2.js` - Another transliteration of the python solution but I did
  make use of a `switch{}` statement (python's most obvious lacking feature)

## Go
  * `go/day1part2.go` - It's not exactly idiomatic but it is better structured and
  (by virtue of parameters) it can solve both part 1 and part 2 in a single program.
  * `go/day2part2.go` - More boilerplate conversion from the python version.

## Rust
  * `rust/day1part2.rs` - Again, this is a whatever-works answer. Rust's compiler
  is quite handy for suggesting work-arounds though. Very similar implementation
  and capabilities to the Go version, simpel testing suggests it's 3x faster
  to run, though...
  * `rust/day2part2.rs` - Same as Go,Javascript versions - a transliteration of
  the rather simple Python algorithm to it-compiles-it-must-be-valid Rust. There's
  more cargo-cult statements in this (copied off t'web) than I'm happy with.

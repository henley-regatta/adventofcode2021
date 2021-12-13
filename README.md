# adventofcode2021

These are my answers for the [2021 Advent of Code](https://adventofcode.com/2021)

I wasn't intending to take part in this after the time I wasted last year, but...
I quite like programming. I'm not good at it, but I enjoy it. So we'll see how we go.

Answers are structured by language (Python, Go, Rust) and named by day. I'm
expecting there to be 2 parts per day (most days) as there was last year. I could
of course be wrong.

If I find the problem itself interesting or if I run out of time, I'm less likely
to tackle it in other languages. This ought to be obvious from the listing below....

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
  * `python/day4part1.py` - As much an exercise in parsing as anything else, although
  there's quite a lot of bookkeeping done too. Solutions fairly mechanical but it
  does work. Couple of list comprehensions in there to make it look vaguely on-brand.
  * `python/day4part2.py` - You've tried Bingo, now try Anti-Bingo. A fairly simple
  inversion of the completion criteria from part1 made this a quick (if still horribly
  ugly) answer.
  * `python/day5part1.py` - Anticipation of a Part-2 extension means my line-drawing
  algorithm is more complete than needed to get the right answer for part 1.
  * `python/day5part2.py` - YES, finally I predict the part2 problem correctly.
  Differs from part 1 by a single IF clause to now plot diagonals.
    * Extra Credit - `python/day5part2_extracredit.py` produces visualisations
      of the answers to part 2. Output for my data [visualised here](https://www.guided-naafi.org/aoc2021/2021/12/05/VisualisationOfAOC2021Day5Part2.html)
  * `python/day6part1.py` - Simple iterator algorithm, gets the answer in a second.
  Look, I can tell part2 is going to go all algorithmic-explosion, I just can't see
  how yet. Let's go have a look...
  * `python/day6part2.py` - Ah there it is. Amazing how finely-tuned that input was
  so that part 1 is "easy" but part 2 is "hard". Fortunately, fish fall into discrete
  age ranges so we can put them into buckets by age and work with them en masse. As a
  result, part2 executes 20 times faster than part 1 even after extending 80->256 days.
  * `python/day7part1.py` - Fairly simple algorithm but uses arrays not lists and also
  has an optimisation to only search occupied positions ONCE no matter how many crabs
  are in it. And of course we all know part 2 has the algorithmic explosion coming....
  * `python/day7part2.py` - It seems we can "get away" with a simple solution-space
  search algorithm provided we take a couple of steps to optimise. Feels like I've
  missed a trick to turn this trivial, not least of which will be that I'm a bit of a
  donkey calculating the cost step-by-step when it's clearly a series. *UPDATE:* oh
  yes, of course. It's a number series we need over and over. Pre-calculating it
  and having it as a lookup table makes _complete_ sense. Execution time drops from
  1 min 16 seconds to 0.58 seconds, a very worthwhile optimisation.....
  * `python/day8part1.py` - Leaving all the extraneous working in-place because this
  is an abject lesson in **read the whole exam question before answering**. Part 1
  question is a lot simpler than the expected "decode the sequences" question I was
  expecting. That'll be part 2....
  * `python/day8part2.py` - Here it is. This is a purely mechanical approach, which
  explains why I took so long, and even then it contains a heuristic approach (read:
  it works but I can't explain why) to decoding 6-segment and 5-segment numbers.
  As a final note as to how _wrong_ I went: my boy beat me by over an hour to the
  solution after starting way later.
  * `python/day9part1.py` - Bit of a better start. The Adjacency rules are actually
  making the code _more_ complicated than it needs to be, but I'm pretty happy with
  the discriminator code I came up with to do it (much better than mechanical `if`
    clause testing for boundary conditions). Now can I beat Adam to part 2...
  * `python/day9part2.py` - Missed a trick (originally) that the "growth algorithm"
  I use to find the boundaries of basins should _not_ use diagonals and therefore
  shares an adjacency-test with the part1 answer I'd already proved correct. Some
  refactoring thus occurred. Also, the working actually stores/calculates way more
  detail than the solution needs as a legacy of me checking my working.  But, in the
  end a reasonably "clean" approach and fast-calculating answer. If I had time I'd
  definitely do a visualisation of the heightmap and it's contours/low points.
     * `python/day9part2_extracredit.py` - strictly speaking I _didn't_ have time,
     but this was too delicious to pass up. Output and explanation on t'blog [visualised here](https://www.guided-naafi.org/aoc2021/2021/12/09/VisualisationOfAOC2021Day9Part2.html
  * `python/day10part1.py` - For something that ought to be a simple parser this took
  WAY too much time. I needed about 3 run-ups to get the recursive token finder
  algorithm correct. And I've still bodged the exit conditions. _And_ I don't think
  this helps me with part 2 very much either....
  * `python/day10part2.py` - OK, part1's method got me a lot closer to the solution
  for part 2 than I was thinking it was, a bit of futzing with the recursion closure
  bookkeeping (I'm not proud of this, it's not good coding practice, it just...works)
  and a lot of phaffing around with the daft scoring mechanism (and working out an
  off-by-one line termination clause I'd missed in the part1 solution) and boomshanka.
  * `python/day11part1.py` - coding in a YHA using wet string networking edition.
  Hampered by an odd keyboard, weak internet, and the fact that I'm here
  with friends in Derbyshire and doing stuff like walking etc instead of
  coding. Answer took much longer to code than it should, also the fact
  that I mis-read the "clamp to zero until end of step after flash"
  condition, but the final answer is _sweet_.
  * `python/day11part2.py` - This one looked too good to be true, I was
  sure it was one of those Combinatorial Explosions In Disguise they love
  so much but, no, it was a genuine gimmie. A very simple adaptation of
  the part1 answer and the solution presents itself in moments.
  * `python/day11part2_extracredit.py` - Long day spent out of doors, too frazzled
  to even tempt myself with today's challenge, instead a simple sequence-of-still
  images-making-up-a-movie animation of yesterday's answer published to the blog
  [here](https://www.guided-naafi.org/aoc2021/2021/12/12/VisualisationOfAOC2021Day11Part2.html)
  * `python/day12part1.py` - Depth-first route finding solution. Not bad. Got beef with
  the final question specification which _appears_ to add an additional condition but
  actually doesn't. 

## NodeJS / JavaScript
  * `node/day1part2.js` - Look, this is a straightforward non-idiomatic translation.
  (but it does work)
  * `node/day2part2.js` - Another transliteration of the python solution but I did
  make use of a `switch{}` statement (python's most obvious lacking feature)
  * `node/day3part2.js` - More of a straightforward transliteration than I was
  hoping for, but it does have the one-recursion-only optimisation. Not sure that
  makes much difference t.b.h....

## Go
  * `go/day1part2.go` - It's not exactly idiomatic but it is better structured and
  (by virtue of parameters) it can solve both part 1 and part 2 in a single program.
  * `go/day2part2.go` - More boilerplate conversion from the python version.
  * `go/day3part2.go` - Spent more time fighting type-conversions than I'd have thought
  was reasonable...

## Rust
  * `rust/day1part2.rs` - Again, this is a whatever-works answer. Rust's compiler
  is quite handy for suggesting work-arounds though. Very similar implementation
  and capabilities to the Go version, simpel testing suggests it's 3x faster
  to run, though...
  * `rust/day2part2.rs` - Same as Go,Javascript versions - a transliteration of
  the rather simple Python algorithm to it-compiles-it-must-be-valid Rust. There's
  more cargo-cult statements in this (copied off t'web) than I'm happy with.

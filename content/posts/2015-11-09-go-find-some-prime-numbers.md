---
Title: go find some prime numbers!
Authors: dword
Category: programming
Date: 2015-11-09
Slug: go-find-primes
Summary: finding prime numbers with Go

---
so a few friends keep bugging me that i need to learn their wonderful hipster language go, finally i relented this evening and poked around in it for about 45 minutes to create my tried and true primes code that i can almost do in my sleep now. its ugly and nowhere near as fast as i had it running in c++ back in the day but its kinda cool that i could get it done in about an hour from first writing a line of code in go. i honestly don&#8217;t know if i will ever use the language as a main language in any projects but its the first time i have touched a compiled language in probably the better part of 5 years, these days i do about 105% of my things in python or bash when there are command line tools to do most of what i want.

```go
import "fmt"

func main() {
        var limit int = 10000
        for j := 2; j &lt;= limit; j++ {
                if j % 2 == 0 {
                        // not prime, we care not!
                } else {
                        // lets do the test loop thing
                        var slimit int = j / 2

                        var multiples int = 0
                        for jj := 1; jj &lt;= slimit; jj++ {
                                if j % jj == 0 {
                                        multiples++
                                } else {
                                        // no multiples here boss
                                }
                        }
                        if multiples == 1 {
                                fmt.println(j, "is probably a prime")
                        }
                }
        }
```

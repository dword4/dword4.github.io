Title: Staircase Challenge
Date: 2021-08-27
Category: programming
Slug: staircase-programming-challenge
Authors: dword4
Summary: a quick code blurb I wrote for an online challenge

The other day I was doing a programming challenge somewhere online and was given the staircase problem randomly, its a pretty simple one but after looking my code over a few times I thought I had this about as simplified as possible without resorting to something like using lambdas.

    :::python
    #!/usr/bin/env python3

    def caseit(n):
        spaces = n - 1
        stairs = 1

        for i in range(n):
            space = ""
            stair = ""
            for sp in range(spaces):
                space += " "
            for st in range(stairs):
                stair += "#"
            print(f"{space}{stair}")
            spaces -= 1
            stairs += 1

    caseit(35)

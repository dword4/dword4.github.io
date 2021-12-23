Title: Sunsetting a Project
Date: 2021-10-13
Category: thoughts
Slug: sunsetting-hockey-info
Authors: dword4
Summary: ruminating on the end of a project and the path forward

For a while now I have struggled to develop the [hockey-info](http://gitlab.com/dword4/hockey-info) project further, trying to make it faster or more friendly for mobile use.  I dabbled with new frameworks to make a faster interface, pondered the idea of turning it into an API and learning JS to put a more stylish interface in front of it.  Even put time into moving some of the more cumbersome API hits into redisJSON objects for the sake of speed. 

It wasn't until I had the local version configured to use Redis that I realized I would have to pay more to run it on the internet, and after some research I realized that it would more than double the cost from 5$ a month to about 20 to 25$ a month depending on where I decided to host it.  There are some hosted Redis options that would have simplified the process but they were the most expensive, when I looked at doing most of the configruation by hand it saved me money but added more complexity that I wasn't really interested in.

Realizing I had hit the wall of a reasonable hobby project, going from 60$ a year to well over 240$ was something I could not justify.  I had pondered ways to try to monetize things but they fell flat when I looked at actual traffic numbers.  The users were simply not there to run any sort of advertising and without actual users nobody would donate to such a project either to keep it online.  With the financial realities staring at me from a spreadsheet and the difficulty of writing actual code to move the project forward I decided it was time to hang it up.

I started the project in March of 2019 almost a year after I had begun documenting the NHL API, taking all the things I learned along the way and creating someting to show for all my efforts.  In more than a few job interviews I talked about the project, how I had grown it and shaped it into something I used almost daily. It was great fun to grow the application with new features, fixing the various quirks that showed up during the Covid-19 shortened season as the NHL altered playoff formats.  But as with so many things it just doesn't make sense to put money into hosting it when there are so many better applications out there doing the same thing.

While it is kind of bittersweet to sunset a project like this I think it will eventually free up some mental resources to put into something new and exciting that hopefully will force me to learn some new languages and techniques along the way.

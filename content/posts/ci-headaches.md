Title: CI Headaches
Date: 2025-03-17
Category: devops
Slug: ci-headaches
Authors: dword4
Tags: CI/CD, Gitlab, DevOps
Summary: The longer I am in this space the more I find myself noticing shortcimings of software that just seems obvious to me. Recently the target of a lot of that feeling has beocme Gitlab which I use on a daily basis for work.  Particularly a lot of the things around their CI/CD Pipelines has lead to quite a bit of frustration and annoyance.

<!-- PELICAN_BEGIN_SUMMARY -->

## Artifacts and Caches

I have a rather large terraform project with multiple modules and I was working on adding a new one that would ultimately add some alarms. The terraform itself wasnt overly complex, the real pain came when I realized at scale I would be kicking off 181 jobs at once in the apply stage. 

Kicking off the full 181 jobs at once caused an almost immediate crawl in the runner that got the unfortunate luck of the draw, utlimately leading to a bunch of timeouts pulling down the job plan artifats.  I started diging into the logs, wondering why my shiny and bright new terraform was not producing the magic I expected from it.  I looked at the first job in the stack and right off the bat I saw it was pulling down a TON of artifacts, but that makes sense I have a lot of them right?  Checked another and saw the same thing, and another, and then as I hopped through more of the jobs I started seeing messages that indicated I was being ratelimited by Gitlab.

Keeping an old school calculator on my desk I punched in the math to figure out just how many calls for artifacts I could be generating at once (since it was all happening with `parallel:`) and realized the headache I was in for: 181 jobs each pulling 181 artifacts at once works out to be 32,761 artifact pulls.  This was definitely not going to work so I hit the search engines and LLMs and landed on caching as an alternative to pass my plan files between stages.

In the movies this would be a montage spot, burn several hours and water bottles full of caffine and the cache option was proving to be no better. It would fail to update the cache seemingly at random and then the apply runs wouldnt find the plans the expected to be there. At this point I was beyond annoyed with it all and decided to say screw it and go back to the old ways. I reverted back to using artifacts (way easier than the first go-round for some reason) and commentd out all but 10 items in my list. The computer gods were smiling on me at that point (or maybe laughing) and decided to bless me with success across the board.

After the tediuous 10-at-a-time process was done and everything checked out I went back to documentation searching and saw suggestions to use something other than gitlab for artifacts when you have very large workloads like what I had. The first suggestion was s3, which in hindsight would have been a fine alternative however I realized that the time to implement that would have slowed things down even further.

What I truly wish Gitlab made possible would be intelligent fetching of artifacts so that I could specify what artifacts a job/stage needs and it ONLY gets those instead of everything under the sun. Unfortunately I don't see that happening anytime soon (more likely masking in pipeline variables will land before something that useful does). 

## Deploys or Local?

Again in the context of work we have a slack bot we have been slowly building up over time with utility for the rest of the team. Initially it was just me working on it but once we added a 3rd person to my squad we decided to branch out and everyone took up tasks for it. Deployment for this was rather simple, I had it refined down enough to a docker-compose file that would stand up everything.

Somewhere along the way we decided the bot needed to be a little more professional so it got moved over to ECS from the standalone EC2 Docker server I stood up initially.  This worked great for quite a while, I could work on an update to the bot locally, run it with dev creds and test it a bunch then when ready send it along its way to the main branch and update with a quick docker-compose command and done. This unfortunately did not last for too long as we eventually pulled the dev instance into ECS as well, so now in order to test even the smallest code changes it requires a whole deploy pipeline. 

I realize its probably best to work this way for the sake of doing things in an industry acceptable way but it drives me crazy how much it slows down the process. First the pushes to the repo trigger a whole host of company mandated scans like secrets detection, dependency scanning and a few others I cant recall. Then you have tag the code, login to AWS, fiddle with task definitions and ultimately trigger a new deployment for the dev instance. Now imagine doing this every single time you make a change in code! Forgot a character or mis-typed a variable name? Yep time to do that whole process.  

There has to be some kind of middle ground between wild west locally running things and a rigid and formalized process for something that ultimately is non-critical and just a handy tool to save a little bit of time? I wish I had a good answer for what that middle ground could or should be because the process as it stands really is a turn-off to putting in work adding new features.
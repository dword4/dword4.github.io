Title: PaaS Frustrations
Date: 2021-02-03
Category: programming, cloud, git
Slug: paas-frustrations
Authors: dword4
Summary: Working through a slightly obscure Gitlab problems

So after several days working with the Support folks at Digital Ocean they finally nailed down why my deploys were never getting new code and I am still not clear on the reason it was an issue to begin with but I figured it needs to be documented to maybe save someone else the trouble.

**The Details**

My code is a mix of Python (and some HTML/JS) using Flask, Python version in this specific situation was 3.8.2 (at least locally anyway). Using the Digital Ocean App platform and a domain hosted through them as well (hockey-info.online). Docker version locally was 20.10.2, build 2291f61 on a Fedora 32 based system.

**The Problem**

No code changes I made after Jan 15th seemed to be pulled when doing a deploy, deploys would trigger properly however they never got the correct code just the correct commit sum. I tried manual deploys, I tried automatic, I searched the internet high, low and inbetween but couldn’t figure it out.

**Solution (Eventually)**

I finally broke down and opened a ticket with DO on a Wednesday, after going back and forth with their support people and trying a lot of things they finally informed me of a solution on the Tuesday after. It seems that in the Dockerfile I was doing a ```RUN git clone https://gitlab.com/dword4/hockey-info.git .``` which was running the git command to pull code down outside of the methods used by the App platform. The fix turns out was as simple as replacing that line with ```COPY . /hockey-info``` and then pushing the code up.

Still not entirely sure why this functions this way, there appears to be some kind of git caching going on but I have no real insight as to why, probably due to how the app platform is built.

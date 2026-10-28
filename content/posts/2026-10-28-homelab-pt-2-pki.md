Title: PKI in the Homelab
Date: 2026-10-28
Category: homelab
Slug: homelab-pki
Authors: dword4
Summary: I got tired of clicking through certificate warnings and typing curl -k, so I built an internal CA. Here's how NestCA and Certwarden fit together, why distributing trust is the hard part, and what I'd do differently.


For a long time my homelab had a dirty little secret: a browser full of "Your connection is not private" warnings that I had trained myself to click straight through, and a shell history littered with `curl -k`. I would never let that fly at work, so eventually I got tired of letting it fly at home. This is the story of how I ended up running my own certificate authority, and what I wish I had known before I started.

## Why Bother?

The honest answer is that it started as annoyance and turned into a learning exercise. Once I had Authentik handing out SSO via OIDC, Forgejo running CI, Infisical holding secrets and a pile of other services all talking to each other over HTTPS, the self-signed cert shortcuts stopped being a minor nuisance and started being actual breakage. OIDC clients refuse to talk to an IdP they dont trust, CI runners fail builds on certificate errors, and every tool has its own special flag for ignoring them (none of which are the same flag, naturally).

The other reason is that PKI is one of those topics that is easy to hand-wave in a work environment because someone else set it up years ago. Building one from scratch forces you to actually understand what a trust chain is, who is vouching for whom, and what breaks when the answer is nobody.

## The Setup

The short version of my current layout:

- **NestCA** is my internal certificate authority
- **Certwarden** sits in front of it and handles requesting, renewing and distributing certificates over ACME
- **Technitium** serves the `int.itsn.network` zone so everything has a real hostname
- **Nginx Proxy Manager** terminates TLS for a lot of the web apps

Every service that lives under `*.int.itsn.network` gets a valid certificate, and I went with a wildcard to keep things simple. Is a wildcard the most security-minded choice? No, one stolen key opens up the whole domain. But for a network where I am the only admin and the alternative is a hundred individual certs to babysit, I was happy to make that trade.

&#91;DREW: add a sentence or two here on how NestCA is built (software, root vs intermediate, where the root key lives) and how long your certs are valid for. I did not want to guess at those details.\]

## Certwarden Is the Part That Makes It Livable

Issuing a certificate once is easy. Issuing it every few weeks forever and getting the new one to the right place is the part that kills homelab PKI projects. Anyone can follow a guide and generate a cert, then forget about it until it expires on a Saturday night and half the house stops working.

Certwarden changed that for me by treating certificates as something with a lifecycle rather than a file I generated once. It requests them, renews them before they expire, and gives the consuming services a stable place to fetch the current version. The first time a certificate rotated on its own and nothing noticed, I stared at the logs for a while waiting for the other shoe to drop. It never did.

## Distributing Trust (The Actually Painful Part)

Here is the thing nobody warns you about: running a CA is the easy half. The hard half is getting every single client to trust it.

Browsers and workstations are the simple case, you import the root once and you are done. The pain shows up in all the places you forget about. Forgejo Actions runners need to trust NestCA or every pipeline that talks to an internal service falls over. Containers carry their own trust stores, so a service that works fine on the host can fail the instant it runs in a container that has never heard of your CA. Wiring up the Infisical integration for my pipelines meant chasing down TLS chain problems in more than one place, and at least once the mysterious "TLS issue" I spent an evening on turned out to be a typo in the hostname. Classic.

The lesson I took away is to treat the trust store like any other piece of configuration. Put the root cert in your Ansible roles and your base images from day one, and you stop discovering missing trust one broken pipeline at a time.

## What I Would Do Differently

If I were starting over I would be more deliberate up front about the boring things:

- Decide how the root and intermediates are structured *before* issuing anything, because changing it later means re-trusting everywhere
- Bake the CA into base images and configuration management immediately
- Put expiry monitoring in place early. Prometheus and Grafana are already in my stack, so watching certificate expiry dates is a small amount of work that saves a very annoying outage

## Was It Worth It?

Absolutely, though not for the reason I expected. The padlock in the browser is nice, and no longer typing `-k` is nicer. What I really got was a much better mental model of how trust works, which has paid off at work more than once.

The pain is front-loaded. It is miserable until the first time everything just works, and then it quietly stops being something you think about at all. I think that is about the best thing you can say about any piece of infrastructure.

\#PKI #Homelab #TLS #Certwarden


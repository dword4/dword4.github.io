---
Title: Curl within a salt-state
Authors: dword
Date: 2017-09-12
Category: automation
Slug: curl-in-salt
Summary: using Curl from a within a salt state file

---
So I have been looking all over for how to make this happen and finally figured it out, preserving it for anybody else who wants to kick off a curl in a salt state to say add something into monitoring or begin another process via an API call

```
# this will perform a curl on the target minion
do_a_curl:
  cmd.run:
    - name: &gt;-
        curl -X POST -d '{"hostname":"192.168.1.65","version":"v2c","community":"public"}' -H 'X-Auth-Token: 286755fad04869ca523320acce0dc6a4' "http://192.168.1.85/api/v0/devices"
```

Right now this is just using testing data from my lab, but as long as you enclose all the salient data in &#8216; or &#8221; it should be fine

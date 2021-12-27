---
Title: Homelab: Synology failure post-mortem
Authors: dword
Date: 2018-07-02
Category: homelab
Tags: homelab, librenms, linux, monitoring, xenserver
Slug: synology-post-mortem
Summary: a post-mortem of my Synology storage system's failure

---
I take my homelab very seriously, its modeled after several production environments I have worked on over the years. What follows is my recap of events over a few weeks leading up to the total failure of my central storage system, my beloved Synology DS1515 hosting 5.5TB of redundant network storage. The first signs of problems cropped up on May 31st and culminated over the last week in June.

<!--more-->

### Prelude

So about a month ago I got a curious alert from LibreNMS about one of my servers going down. Normally this is just me patching things and not scheduling a maintenance window or something. Upon checking the server however SNMP was indeed failing, I logged in to check the server and found snmpd was well and truly hung. No big deal right? I&#8217;ll just reboot it and go on my merry way. I restart the service and watch it for a few minutes and it goes funky again. Now I am wondering what the hell has changed so I start digging into the logs.

A few minutes later I finally turn something up in /var/log/messages which points to a remote filesystem going away unexpectedly. I only had one remote filesystem mounted at the time, a NFS share for backups of VMs so I go check the storage system to see what is up.

Upon trying to login to the web interface of the storage system I find it unresponsive, so I try to ssh to it instead. Nope, not having that either it seems, maybe it will respond to ping? Naturally that didn&#8217;t work either, so now I am confused as to what is going on. About that time I check my email to see if I got any alerts but alas there nothing. Fresh out of ideas I trot myself downstairs and stab the power button a few times until it turns blue and starts coming back, a little weird it took more than one poke but whatever.

As the storage system comes back up I hear a beep of an incoming email; seems it did in fact have a power failure and shut down&#8230;

[![screenshot](images/storage-email-1024x163.png)](images/storage-email-1024x163.png)

### Intermission

All is well for a few weeks, then some drunken idiot snaps a telephone pole about 1am and knocks everything offline.  Seems I sleep too heavily to hear an accident less than 50 ft away.  I also sleep too soundly to hear the chorus of UPS alert tones telling me the entire lab was about to shut down ungracefully.  The power company took a few hours to get me power back, Comcast however took two days.

Surprisingly the lab all came back fine other than a storm of delayed alerts and some VMs that didn&#8217;t start automatically.  Once I get all the alerts cleared I call it a day and go relax.  Unfortunately I was unaware that I had maybe another 24h of peace before the Synology decided to truly flake out.

### Finale

On June 27th out of the blue I start getting hammered with alerts via Pushover coming from the lab.  Seems a bunch of VMs on xenserver are unhappy.  Login, check and they look green in xen orchestra, what about monitoring?  Yep monitoring says they are down, starting to have flashbacks to the previous storage problems.  I run through all the same steps I have before and come to the conclusion that storage is down again.  I start it up once more and this time it takes even longer to convince the power button to work.  Later in the evening it goes down again, not even a full 24h of uptime on it.  At this point I start to accept that its probably dying and I may lose a lot of data including backups and VM disks.

With plans in mind for a replacement I went about my business and disabled a few monitors to cut down on noise.  With those monitors disabled I started the selection process for a replacement which I&#8217;m still working on.  Several hours later I get an alert that my xenserver is down.  Fastfoward 5 minutes and I get a cleared notification that its back to normal.  At this point I am tired so I just call it a night and silence my phone.

The following day I get more of the same alerts for both xen and proxmox along with the recoveries as well.  By the afternoon I get fed up and just ignore all the alerts from both servers completely.  This of course is making my neck itch, I hate not knowing what is going on in the lab.  Several days go by and I am still wondering about the weird alerts.  I look in LibreNMS to find that its happening on a regular interval, this is interesting!

[![screenshot](images/Greenshot-2018-07-02-16.39.57-1-1024x330.png)](images/Greenshot-2018-07-02-16.39.57-1-1024x330.png)

Focusing on the monitoring system I checked crontab for a few users and didn&#8217;t find anything useful. Upon checking cron.d however I finally found the culprit, or at least a smoking gun of sorts.

```
# Using this cron file requires an additional user on your system, please see install docs.

33  */6   * * *   librenms    /opt/librenms/discovery.php -h all &gt;&gt; /dev/null 2&gt;&1
*/5  *    * * *   librenms    /opt/librenms/discovery.php -h new &gt;&gt; /dev/null 2&gt;&1
*/5  *    * * *   librenms    /opt/librenms/cronic /opt/librenms/poller-wrapper.py 16
15   0    * * *   librenms    /opt/librenms/daily.sh &gt;&gt; /dev/null 2&gt;&1
*    *    * * *   librenms    /opt/librenms/alerts.php &gt;&gt; /dev/null 2&gt;&1
*/5  *    * * *   librenms    /opt/librenms/poll-billing.php &gt;&gt; /dev/null 2&gt;&1
01   *    * * *   librenms    /opt/librenms/billing-calculate.php &gt;&gt; /dev/null 2&gt;&1
*/5  *    * * *   librenms    /opt/librenms/check-services.php &gt;&gt; /dev/null 2&gt;&1
```

Now I know its discovery going off every 6 hours, something has to be making it angry. More clicking and clacking on my behalf and I realize that the xenserver discovery takes over 800 seconds.  By now I am fed up with the dead storage system causing me grief, its time to go nuclear.  I go into both xen and proxmox and delete the remote storage as well as any now-dead VMs that lived on it.  Backup jobs? yep deleted those as well since they weren&#8217;t going to run again. One more time I restart snmpd and kick off a discovery manually and await the results.

Another 800 seconds later I get my answer, still taking too long to complete and failing. Its still the same two servers too despite all my ministrations on them to remove the failed remote storage.  I have advanced from annoyed to frustrated to pissed at this point, I just want things back working and my alert board green. With furious typing I login to the xenserver and manually check the mount points.  What. The. Hell. There are still mount points to the remote filesystems despite Xen Orchestra and the Xen Client telling me that its gone. Tired of all this I run umount -l on the mount point,which is the least polite option I can find for removing it. Again with the restart of snmpd and a discovery and wait.

Success! Now the discovery is much faster, but there is one more system still slowing it down a bit, the proxmox server.  A quick check reveals its also got the mount pointing hanging around so snmp is still trying to reach it and timing out.  Blow that one away and test again and now discovery is completing in under 10 seconds as opposed to 800. Eager to finally get to bed as its now midnight I re-enable all the monitors on the hypervisors and head for sleep.

### Conclusions
[![screenshot](images/Greenshot-2018-07-02-17.06.50-1-1024x348.png)](images/Greenshot-2018-07-02-17.06.50-1-1024x348.png)

Monitoring was worth its weight in gold in this situation even for a homelab, it gave me context I didn&#8217;t easily have otherwise.  Being able to look over 48 hours of data made the difference in finding the discovery process possible.  Although I still have a lot of tuning to do for better alerting getting them still prompted my action.  Another point I realized is to never rely on a single tool or information source.  I trusted both xenserver and proxmox to faithfully show me that the storage was gone but they did not.  While that is not a fault of them so much as a discrepancy between OS and applications running on top its still important to note.

Ticketing was another valuable tool for me in writing this up afterwards.  Being able to look up dates in tickets made finding graphs much easier for me. I am more than a little proud of the fact that I wrote the [Gitlab Transport for LibreNMS][4] myself, and its nice that its proven useful in the homelab beyond just a programming and OSS contribution project.

As for the now dead Synology it might be possible to rescue but I am not holding my breath.  One thing is for sure, its replacement will be much larger and probably not an appliance.

 [4]: https://github.com/librenms/librenms/pull/8246

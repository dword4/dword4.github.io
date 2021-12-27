---
Title: Patching CentOS 7 (and overcoming problems)
Authors: dword
Date: 2019-06-19
Category: sysadmin
Tags: linux, centos7

---
So I was working on patching some of my Icinga infrastructure at work, and it seems that sometimes libyajl breaks things, as illustrated below

```
root@icingasatellite ~]# yum update
 Loaded plugins: fastestmirror, rhnplugin
 This system is receiving updates from RHN Classic or Red Hat Satellite.
 Loading mirror speeds from cached hostfile`

  * `epel: mirror.optus.net
 Resolving Dependencies
 --> Running transaction check
 ---> Package icinga2.x86_64 0:2.10.4-1.el7.icinga will be updated
 ---> Package icinga2.x86_64 0:2.10.5-1.el7.icinga will be an update
 ---> Package icinga2-bin.x86_64 0:2.10.4-1.el7.icinga will be updated
 ---> Package icinga2-bin.x86_64 0:2.10.5-1.el7.icinga will be an update
 --> Processing Dependency: libyajl.so.2()(64bit) for package: icinga2-bin-2.10.5-1.el7.icinga.x86_64
 Traceback (most recent call last):
 File "/bin/yum", line 29, in 
 yummain.user_main(sys.argv[1:], exit_code=True)
 File "/usr/share/yum-cli/yummain.py", line 375, in user_main
 errcode = main(args)
 File "/usr/share/yum-cli/yummain.py", line 239, in main
 (result, resultmsgs) = base.buildTransaction()
 File "/usr/lib/python2.7/site-packages/yum/`**`init`**`.py", line 1198, in buildTransaction
 (rescode, restring) = self.resolveDeps()
 File "/usr/lib/python2.7/site-packages/yum/depsolve.py", line 893, in resolveDeps
 CheckDeps, checkinstalls, checkremoves, missing = self._resolveRequires(errors)
 File "/usr/lib/python2.7/site-packages/yum/depsolve.py", line 1025, in _resolveRequires
 (checkdep, missing, errormsgs) = self._processReq(po, dep)
 File "/usr/lib/python2.7/site-packages/yum/depsolve.py", line 350, in _processReq
 CheckDeps, missingdep = self._requiringFromTransaction(po, requirement, errormsgs)
 File "/usr/lib/python2.7/site-packages/yum/depsolve.py", line 680, in _requiringFromTransaction
 rel=pkg.rel)
 File "/usr/lib/python2.7/site-packages/yum/`**`init`**`.py", line 5280, in update
 availpkgs = self._compare_providers(availpkgs, requiringPo)
 File "/usr/lib/python2.7/site-packages/yum/depsolve.py", line 1648, in _compare_providers
 bestnum = max(pkgresults.values())
 ValueError: max() arg is an empty sequence
```

Turns out the secret is simply to install yaljl and yajal-devel and then I can patch successfully, really surprised nobody else out there has run into this yet but its the second time in a month I have had it happen when patching.

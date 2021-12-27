---
Title: Crontab – Always Check your Environment Variables
Authors: dword
Type: post
Date: 2016-06-16
Category: general
Slug: always-check-env-variables
Summary: Always remember to check environment variables folks

---
So I have been running into this issue for like a month now where a script that I can run from the command line by hand executes fine, but when I try to run it via a crontab job it just goes absolutely pear shaped without any real explanation.  Finally I got some time at the beginning of a shift to sit with one of our senior guys to take a look at it as the script provides data the entire team uses and when it doesn&#8217;t run they get cranky.  It turns out that the environment my cron jobs run as is highly different, as indicated by the following which is obtained by adding adding a line to output env to a text file every time the crontab job ran.

```bash
XDG_SESSION_ID=159
SHELL=/bin/sh
OLDPWD=/home/dword
USER=dword
<strong>PATH=/usr/bin:/bin
</strong>PWD=/home/dword/labmap
LANG=en_US.UTF-8
HOME=/home/dword
SHLVL=2
LOGNAME=dword
XDG_RUNTIME_DIR=/run/user/1000
_=/usr/bin/env
```

Compare that against the results from env when run by hand

```bash
 XDG_SESSION_ID=145
 HOSTNAME=dword-cent7
 TERM=xterm
 SHELL=/bin/bash
 HISTSIZE=500000
 SSH_CLIENT=192.168.42.120 49429 22
 SSH_TTY=/dev/pts/0
 USER=dword
 LS_COLORS=rs=0:di=01;34:ln=01;36:mh=00:pi=40;33:so=01;35:do=01;35:bd=40;33;01:cd=40;33;01:or=40;31;01:mi=01;05;37;41:su=37;41:sg=30;43:ca=30;41:tw=30;42:ow=34;42:st=37;44:ex=01;32:*.tar=01;31:*.tgz=01;31:*.arc=01;31:*.arj=01;31:*.taz=01;31:*.lha=01;31:*.lz4=01;31:*.lzh=01;31:*.lzma=01;31:*.tlz=01;31:*.txz=01;31:*.tzo=01;31:*.t7z=01;31:*.zip=01;31:*.z=01;31:*.Z=01;31:*.dz=01;31:*.gz=01;31:*.lrz=01;31:*.lz=01;31:*.lzo=01;31:*.xz=01;31:*.bz2=01;31:*.bz=01;31:*.tbz=01;31:*.tbz2=01;31:*.tz=01;31:*.deb=01;31:*.rpm=01;31:*.jar=01;31:*.war=01;31:*.ear=01;31:*.sar=01;31:*.rar=01;31:*.alz=01;31:*.ace=01;31:*.zoo=01;31:*.cpio=01;31:*.7z=01;31:*.rz=01;31:*.cab=01;31:*.jpg=01;35:*.jpeg=01;35:*.gif=01;35:*.bmp=01;35:*.pbm=01;35:*.pgm=01;35:*.ppm=01;35:*.tga=01;35:*.xbm=01;35:*.xpm=01;35:*.tif=01;35:*.tiff=01;35:*.png=01;35:*.svg=01;35:*.svgz=01;35:*.mng=01;35:*.pcx=01;35:*.mov=01;35:*.mpg=01;35:*.mpeg=01;35:*.m2v=01;35:*.mkv=01;35:*.webm=01;35:*.ogm=01;35:*.mp4=01;35:*.m4v=01;35:*.mp4v=01;35:*.vob=01;35:*.qt=01;35:*.nuv=01;35:*.wmv=01;35:*.asf=01;35:*.rm=01;35:*.rmvb=01;35:*.flc=01;35:*.avi=01;35:*.fli=01;35:*.flv=01;35:*.gl=01;35:*.dl=01;35:*.xcf=01;35:*.xwd=01;35:*.yuv=01;35:*.cgm=01;35:*.emf=01;35:*.axv=01;35:*.anx=01;35:*.ogv=01;35:*.ogx=01;35:*.aac=01;36:*.au=01;36:*.flac=01;36:*.mid=01;36:*.midi=01;36:*.mka=01;36:*.mp3=01;36:*.mpc=01;36:*.ogg=01;36:*.ra=01;36:*.wav=01;36:*.axa=01;36:*.oga=01;36:*.spx=01;36:*.xspf=01;36:
 MAIL=/var/spool/mail/dword
<strong> PATH=/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/home/dword/.local/bin:/home/dword/bin</strong>
 PWD=/home/dword/labmap
 LANG=en_US.UTF-8
 HISTCONTROL=ignoredups
 SHLVL=1
 HOME=/home/dword
 LOGNAME=dword
 SSH_CONNECTION=192.168.42.120 49429 192.168.33.232 22
 LESSOPEN=||/usr/bin/lesspipe.sh %s
 XDG_RUNTIME_DIR=/run/user/1000
 _=/usr/bin/env
 OLDPWD=/home/dword/labmap/web
```

Notice the path statement is very sparse when cron outputs the environment variables, turns out that anemic path lacked access to fping which was integral to my script building out a list of live hosts within our lab environment. Once that was fixed the cron jobs hum along nicely and churn out an updated map of the lab every hour without me doing anything and now I know that crontabjobs run with fairly different environment variables than scripts manually ran and can cause all kinds of havoc if you don&#8217;t use full explicit path statements in your bash scripts that you plan to automate.

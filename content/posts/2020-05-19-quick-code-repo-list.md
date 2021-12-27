---
Title: Quick Code: Repo List
Author: dword
Date: 2020-05-19
Category: programming
Tags: git, python
Slug: git-repo-list
Summary: Quick little bit of code to let you list all repos your currently logged in account can access

---
So I ran into an interesting problem over the weekend, I forgot my 2FA token for Gitlab at home while I was away. My laptop&#8217;s SSH key was already loaded into Gitlab so I knew I could clone any of my repositories if only I could remember the exact name. That of course turned out to be the problem: I couldn&#8217;t remember the name of a specific repository that I wanted to work on. I even tried throwing a bunch of things at git clone to try to guess it and still had no luck. Enter the Gitlab API:

```

#!/usr/bin/env python3

import requests
from tabulate import tabulate

personal_token = 'asdf132kj6lkj1lk6j'
user_id = 'dword4'

base_url = 'https://gitlab.com/api/v4/'
repo_url = 'users/'+user_id+'/projects'

full_url = base_url + repo_url + '?private_token=' + personal_token

res = requests.get(full_url).json()

table = []
for project in res:
    name = project['name']
    name_spaced = project['name_with_namespace']
    path = project['path']
    if project['description'] is None:
        description = ''
    else:
        description = project['description']
    table.append([name, description])
print(tabulate(table, headers=["name", "description"]))
```
This is of course super simplistic and does virtually no error checking, fancy formatting, etc. However now with a quick alias I can get a list of my repositories even when I do flake out and forget my token at home.

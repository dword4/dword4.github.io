---
Title: Simple CI with Chef
Authors: dword
Date: 2018-09-04
Category: automation
Tags: automation, chef, CI, devops, git
Slug: simple-ci-chef
Summary: Creating a simple pipeline using Chef
---

So I needed to work out a way to make a script I wrote recently be deployed across a whole host of systems, turns out the only option is Chef so I had to dive into it and read a bunch of stuff.  Also had to try a bunch of things and ended up with my own Chef server in the lab to test against.  Several hours of clicking and clacking later and I have my task worked out, so here it is.

First we need to create a new cookbook and drop a pretty simple default recipe in, all it does is make sure git is installed then clone a repo to /opt/nhlapi.

```ruby
#
# Cookbook:: repo
# Recipe:: default
#
# Copyright:: 2018, The Authors, All Rights Reserved.
#
#
package 'git' do
  action :install
end

git '/opt/nhlapi' do
  repository 'git://gitlab.com/dword4/nhlapi.git'
  revision 'master'
  action :sync
end
default.rb (END)
```

Once we have the recipe we need a role to tell it what to do.

```json
{
   "name": "repo-update",
   "description": "update chef from time to time",
   "json_class": "Chef::Role",
   "default_attributes": {
     "chef_client": {
       "interval": 1800,
       "splay": 60
     }
   },
   "override_attributes": {
   },
   "chef_type": "role",
   "run_list": ["recipe[chef-client::default]",
                "recipe[chef-client::delete_validation]"
   ],
   "env_run_lists": {
   }
}
```

Create the role with `# knife role from file repo-update.json`  (or whatever you named the file to create the role from).

Now all that is left is to assign the role to the node so use `#knife node edit itsj-cheftest.itscum.local` and assign the role and repo to the node we want

```json
{
  "name": "itsj-cheftest.itscum.local",
  "chef_environment": "_default",
  "normal": {
    "tags": [

    ]
  },
  "policy_name": null,
  "policy_group": null,
  "run_list": [
    "recipe[nginx]",
    "recipe[repo]",
    "role[repo-update]"
]

}
```

That is enough to get it working, you can kick back and watch it with `while :; do knife status 'role:repo-update' run-list; sleep 120; done` and wait to see it run in about 30 minutes based on the interval and splay values.  Speaking of which Interval is pretty self explanatory, but Splay not-so-much; Splay is used keep a bunch of nodes from all running at once basically so it doesn&#8217;t overwhelm a system that they might be checking into or otherwise digitally assaulting.

Title: Taking Back Email - An Overview
Date: 2021-12-17
Category: thoughts
Slug: taking-back-email
Authors: dword4
Summary: a quick overview of how to take back email

**So full disclosure I got this idea from a friend who has already done a lot of the leg work**

One of the biggest ways we give away TONS of data is using email providers such as Gmail which 
outright data mine our entire inbox contents to build profiles on us.  While I no longer aspire
to run a basement datacenter for fun there is a middle ground to be had I think.  In this case
it would be utilizing a service such as Azure to do the hosting portion but keeping control of
the assets and managing them myself (to a degree).

The general idea is to setup an Azure AD Premium P2 instance (9$/month) for authentication and 
control and use Office 365 Business specifically for the email portion (5$/month).  With O365 
business you currently get a 50GB mailbox, ability to use a custom domain (required for the AD
portion I believe) and a 1TB OneDrive account.  Comparison wise it costs about 10$ a month to get 
2TB of storage with Google to split between your Drive and Gmail account.

Another perk of this path is that I can utilize the AD authentication to tie various apps into 
a central authentication platform that I control.  This opens up a whole new realm of control
and configuration to ensure that I can help keep my data safe and private, allowing for a degree 
of control that otherwise would require a great deal more configuration work to self-host email 
at home.

The general idea here is to document the process as I go to help guide others who want to take 
back some control of their data. That and it forces me to use Pelican more to update this so its
a nice bonus.

Title: Looping Unknown API Results
Date: 2025-12-12
Category: programming
Slug: api-results-loop
Authors: dword4
Summary: Dealing with APIs that return unknown numbers of results

ome APIs do not tell you how many results you have to work with, so you end up blindly looping until a failure which is not generally ideal. 

`api/v1/projects` 

Take the endpoint above, lets say it takes two possible parameters

`size` which represents the number of results returned by the current call
`offset` which means where in the unknown list of projects we want to start the retrieval of the **size** number of results

So we would get a bunch of calls like this
```
api/v1/projects?size=20&offset=0
api/v1/projects?size=20&offset=20
api/v1/projects?size=20&offset=40
...
```

But we must remember we don't _know_ how many of these calls we may need to make without cheating and looking at say the web interface this API is used to build. To help simulate this experience I threw together a very rudimentery script to imitate the idea of an unknown sized list we can use to work against

```python
import random

MAX = random.randint(300, 500)
SIZE = 20

API = []

for i in range(0,MAX):
API.append({
	"id": i,
	"name": f"Project {i}",
	"rulesets": [f"Ruleset {j}" for j in range(random.randint(1, 5))],
	"rules": random.randint(1, 100)

})
```

So this gives us a randomized list called **API** which we can work against to figure out a sensible looping strategy. Since we don't know the size of **API** in theory, we cant use a for loop without some rather complex conditions, so lets try something much simpler.

```python
while True:
	# loop contents
```

While loops are ideal for this since we can just do a True/False loop because we either get data we can use from the API or we don't, there is no other potential situation (minus obvious outliers like ratelimits, authentication failures, etc) we would occur that the loop needs to handle

To facilitate this and make things more readable we need a function that will grab a chunk of results from **API** and return them, that way we can separate out logic a bit.

```python
def grab_projects(offset, size):

url_projects = f"https://some.api.host/api/v1/projects?limit={size}&offset={offset}"
print(f"Fetching projects from {offset} to {offset + size}, URL: {url_projects}")
subset = API[offset:offset + size]

return subset
```

So now we have a function that takes two inputs for size and offset, then returns us that chunk of results. If you were actually making API calls here is where you would slap some requests work and any error handling you may want.

With that in place we can do the meat and potatoes of this loop, which looks something like this

```python
while True:
	set_of_projects = grab_projects(offset, SIZE)
	if not set_of_projects:
		break
	batches.append(set_of_projects)
	offset += SIZE
```

This loops until there is a failure to set the variable **set_of_projects** from the return from grab_projects() so we don't know how many times it will loop, only that there will eventually be and end and we stop looping when thats hit. In order to allow us to collect all of the information we have a list called **batches** to which we append **set_of_projects** on each iteration of the loop, then after we are done we can flatten it into something we can use elsewhere by using a list comprehension

```python
# flatten the list of lists
all_projects = [project for batch in batches for project in batch]
```

When put together it looks like this 

```python
import random

MAX = random.randint(300, 500)
SIZE = 20

  

API = []
for i in range(0,MAX):
	API.append({
		"id": i,
		"name": f"Project {i}",
		"rulesets": [f"Ruleset {j}" for j in range(random.randint(1, 5))],
		"rules": random.randint(1, 100)
})

offset = 0

def grab_projects(offset, size):
	url_projects = f"https://some.api.host/api/v1/projects?limit={size}&offset={offset}"
	print(f"Fetching projects from {offset} to {offset + size}, URL: {url_projects}")
	subset = API[offset:offset + size]

	return subset

  

batches = []

all_projects = []

  

while True:
	set_of_projects = grab_projects(offset, SIZE)

	if not set_of_projects:
		break

	batches.append(set_of_projects)
	offset += SIZE

  

# flatten the list of lists

all_projects = [project for batch in batches for project in batch]

  
# output from all_projects 
for project in all_projects:
	print(project['id'], project['name'], project['rulesets'], project['rules'])
```

Now this at least gets you the results to work with and provides me a chance to show where you could go from here. If the API is particularly slow (which the one I was working with at the moment) then you don't want to wait forever for this loop to do its thing. From here it would be worthwhile to make some changes to the script to define a temporary MAX of like say 200 if you are taking chunks of 20 results, run the code and benchmark it to see how long it takes for the 10 calls to return their results. 

Armed with some benchmark information (in my case it was 2 minutes to pull 430ish projects in chunks of 20, avg of like 5 seconds per call) its possible to apply some threading or other similar methodology to get the data set faster


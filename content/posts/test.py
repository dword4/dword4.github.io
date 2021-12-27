
#!/usr/bin/env python3
import requests                                                                                               from tabulate import tabulate
personal_token = 'asdfqwerzxcv1234'                                                                          
user_id = 'dword4'                                                                                                                                                                                                          base_url = 'https://gitlab.com/api/v4/'                                                                       repo_url = 'users/'+user_id+'/projects'                                                                                                                                                                                     full_url = base_url + repo_url + '?private_token=' + personal_token                                                                                                                                                         res = requests.get(full_url).json()
table = []
for project in res:                                                                                               name = project['name']
    name_spaced = project['name_with_namespace']
    path = project['path']
    path_spaced = project['path_with_namespace']
    if project['description'] is None:
        description = ''
    else:
        description = project['description']
        table.append([name, description])
    print(tabulate(table, headers=["name", "description"]))

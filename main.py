# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def main():
    # Use a breakpoint in the code line below to debug your script.
    print('Start scrawling')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

import requests

baseUrl = 'https://api.github.com'
owner='Kaggle'
accessToken='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'
headers = {'Accept':'application/vnd.github+json','X-GitHub-Api-Version':'2022-11-28'}
parameters = {'Authorization': 'Bearer '+accessToken}

response = requests.get(baseUrl+'/orgs/'+owner+'/repos', params=parameters, headers=headers)
print(response.json())
for repo in response.json():
    print(repo['name'])
    repoUrl=baseUrl+'/repos/'+owner+'/'+repo['name']
    r=requests.get(repoUrl,params=parameters, headers=headers)
    print(r)
    stars=r.json()['stargazers_count']
    forks=r.json()['forks_count']

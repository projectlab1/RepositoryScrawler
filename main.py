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
#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
headers = {'Accept':'application/vnd.github+json','X-GitHub-Api-Version':'2022-11-28'}
parameters = {'Authorization': 'Bearer '+accessToken}

#response = requests.get(baseUrl+'/orgs/'+owner+'/repos', params=parameters, headers=headers)
#print(response.json())
#for repo in response.json():
    #print(repo['name'])
    #repoUrl=baseUrl+'/repos/'+owner+'/'+repo['name']
    #r=requests.get(repoUrl,params=parameters, headers=headers)
    #print(r)
    #starCount=r.json()['stargazers_count']
    #print(starCount)
    #forkCount=r.json()['forks_count']
    #print(starCount)
    #branchUrl=baseUrl+'/repos/'+owner+'/'+repo['name']+'/branches'
    #r = requests.get(branchUrl, params=parameters, headers=headers)
    #branchCount=len(r.json())
    #print(branchCount)
    #branchNames=[]
    #for b in r.json():
        #branchNames.append(b['name'])
    #print(branchNames)

url = "https://api.github.com/graphql"

body = """
query {
  repoA: repository(owner:"Kaggle", name:"kagglehub") {
    name
    forkCount   
  },
  repoB: repository(owner:"Kaggle", name:"docker-python") {
    name
    forkCount
  }
}
"""
head = {'Authorization': 'Bearer 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'}
response = requests.post(url=url, json={"query": body},headers=head)
print("response status code: ", response.status_code)
if response.status_code == 200:
    print("response : ", response.content)
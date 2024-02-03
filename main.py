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
import json

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
organizationName='Kaggle'
getAllRepos="""
query{
  organization(login: \""""+organizationName+"""\") {
    repositories(first: 20) {
      totalCount
      nodes {
        name
      }
    }
  }
}
"""
head = {'Authorization': 'Bearer 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'}
response = requests.post(url=url, json={"query": getAllRepos},headers=head)
print("response status code: ", response.status_code)
if response.status_code == 200:
    print("response : ", response.content)
numberOfRepos=response.json()['data']['organization']['repositories']['totalCount']
nameOfRepos=response.json()['data']['organization']['repositories']['nodes']
query="""
query{

"""
x=0
for repo in nameOfRepos:
    print(repo['name'])
    tempQuery="""
    : repository(owner:\""""+organizationName+"""\", name:\""""+repo['name']+"""\") {
    name
    forkCount
    stargazerCount
    releases(first:0){
      totalCount
    }
    issues(states:CLOSED) {
      totalCount
    }
    languages(first:10) {
      totalCount
      totalSize
      edges{
        size
      }
      nodes{
        name 
      }
    }
	refs(refPrefix: "refs/heads/", first: 100){
        nodes{
          name
          target {
          ... on Commit {
            history(first: 0) {
              totalCount
            }
          }
        }
        }
    }
  }
    """
    query=query+'repo'+str(x)+tempQuery+""",
    """
    x=x+1
query=query+"""
}"""

counter=0

response = requests.post(url=url, json={"query": query},headers=head)
print("response status code: ", response.status_code)
if response.status_code == 200:
    organizationData={}
    repoData=[]
    while counter<numberOfRepos:
        repo=response.json()['data']['repo'+str(counter)]
        tempData={}
        tempData['name']=repo['name']
        tempData['stars']=repo['stargazerCount']
        tempData['forks']=repo['forkCount']
        repoData.append(tempData)
        organizationData[organizationName]=repoData
        counter=counter+1
    json_data = json.dumps(organizationData, indent=2)
    file_path = "Data/AllRepositoryInformation.json"
    with open(file_path, 'w') as json_file:
        json_file.write(json_data)





body = """
query {
  repoA: repository(owner:"Kaggle", name:\""""+'gyfy'+"""\") {
    name
    forkCount
    stargazerCount
    releases(first:0){
      totalCount
    }
    issues(states:CLOSED) {
      totalCount
    }
    languages(first:10) {
      totalCount
      totalSize
      edges{
        size
      }
      nodes{
        name 
      }
    }
	refs(refPrefix: "refs/heads/", first: 100){
        nodes{
          name
          target {
          ... on Commit {
            id
            history(first: 0) {
              totalCount
            }
          }
        }
        }
    }
  },
  repoB: repository(owner:"Kaggle", name:"docker-python") {
    name
    forkCount
    releases(first:0){
      totalCount
    }
     refs(refPrefix: "refs/heads/", first: 100){
        nodes{
          name
          target {
          ... on Commit {
            id
            history(first: 0) {
              totalCount
            }
          }
        }
        }
    }
    issues(states:CLOSED) {
      totalCount
    }
  }
}
"""

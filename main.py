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
import statistics


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

getAllInfoQuery="""
query{

"""
counter=0
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
    getAllInfoQuery=getAllInfoQuery+'repo'+str(counter)+tempQuery+""",
    """
    counter=counter+1
getAllInfoQuery=getAllInfoQuery+"""
}"""

response = requests.post(url=url, json={"query": getAllInfoQuery},headers=head)
print("response status code: ", response.status_code)

# ----- Another query required for TAGS only ----
counter=0
getTagsQuery="""
query{

"""
for repo in nameOfRepos:
    tempQuery="""
    : repository(owner:\""""+organizationName+"""\", name:\""""+repo['name']+"""\") {
        refs(refPrefix: "refs/tags/", first: 100){
          totalCount
        }
    }
    """
    getTagsQuery=getTagsQuery+'repo'+str(counter)+tempQuery+""",
    """
    counter=counter+1
getTagsQuery=getTagsQuery+"""
}"""

getTagsResponse = requests.post(url=url, json={"query": getTagsQuery},headers=head)
print("response status code: ", getTagsResponse.status_code)


counter=0
organizationData={}
repoData=[]
starList=[]
forkList=[]
closedIssuesList=[]
releasesList=[]
commitsList=[]
tagsList=[]
branchList=[]
languageList=[]

if response.status_code == 200:
    while counter<numberOfRepos:
        repo=response.json()['data']['repo'+str(counter)]
        tempData={}
        tempData['name']=repo['name']
        tempData['stars']=repo['stargazerCount']
        starList.append(repo['stargazerCount'])
        tempData['forks']=repo['forkCount']
        forkList.append(repo['forkCount'])
        tempData['closedIssues']=repo['issues']['totalCount']
        closedIssuesList.append(repo['issues']['totalCount'])
        tempData['releases']=repo['releases']['totalCount']
        releasesList.append(repo['releases']['totalCount'])

        languageStatistics={}
        languageStatistics['numberOfLanguage']=repo['languages']['totalCount']
        languageList.append(repo['languages']['totalCount'])
        languageStatistics['totalSizeInBytesofFilesWrittenInLanguage']=repo['languages']['totalSize']
        listOfLanguages=[]
        for l in range(repo['languages']['totalCount']):
            language = {}
            language['name']=repo['languages']['nodes'][l]['name']
            language['sizeInBytesofFilesWrittenInLanguage'] = repo['languages']['edges'][l]['size']
            listOfLanguages.append(language)
        languageStatistics['listOfLanguage']=listOfLanguages
        tempData['languageStatistics']=languageStatistics

        branchStatistics={}
        listOfBranches=[]
        totalCommits=0
        branchList.append(len(repo['refs']['nodes']))
        for b in range(len(repo['refs']['nodes'])):
            branch={}
            branch['name']=repo['refs']['nodes'][b]['name']
            branch['branchCommits'] = repo['refs']['nodes'][b]['target']['history']['totalCount']
            totalCommits=totalCommits + repo['refs']['nodes'][b]['target']['history']['totalCount']
            listOfBranches.append(branch)
        branchStatistics['numberOfBranch']=len(repo['refs']['nodes'])
        branchStatistics['listOfBranches']=listOfBranches
        tempData['branchStatistics']=branchStatistics
        tempData['commits']=totalCommits
        commitsList.append(totalCommits)

        tempData['tags']=getTagsResponse.json()['data']['repo'+str(counter)]['refs']['totalCount']
        tagsList.append(tempData['tags'])

        repoData.append(tempData)
        organizationData[organizationName]=repoData
        counter=counter+1




overAllStatistics={}
overAllStatistics['totalStars']=sum(starList)
overAllStatistics['medianStars']=statistics.median(starList)
overAllStatistics['totalForks']=sum(forkList)
overAllStatistics['medianForks']=statistics.median(forkList)
overAllStatistics['totalClosedIssues']=sum(closedIssuesList)
overAllStatistics['medianClosedIssues']=statistics.median(closedIssuesList)
overAllStatistics['totalRelease']=sum(releasesList)
overAllStatistics['medianRelease']=statistics.median(releasesList)
overAllStatistics['totalCommits']=sum(commitsList)
overAllStatistics['medianCommits']=statistics.median(commitsList)
overAllStatistics['totalTags']=sum(tagsList)
overAllStatistics['medianTags']=statistics.median(tagsList)
overAllStatistics['totalBranches']=sum(branchList)
overAllStatistics['medianBranches']=statistics.median(branchList)
overAllStatistics['totalLangugaes']=sum(languageList)
overAllStatistics['medianLanguages']=statistics.median(languageList)

organizationData['overAllStatistics']=overAllStatistics

json_data = json.dumps(organizationData, indent=2)
file_path = "Data/AllRepositoryInformation.json"
with open(file_path, 'w') as json_file:
    json_file.write(json_data)


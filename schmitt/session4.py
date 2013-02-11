# 
# Session 4 SciLifeLab python course 2013 -- pandas and course repository status
# 
#
# Thomas Schmitt thms.schmitt@gmail.com
#
import requests
import getpass
import calendar
from pandas import DataFrame
from pandas import Series
from dateutil import parser

NO_RESULTS = 409 #Github status code for no results

def fetchCommitHistory(organisation,auth=None):
    """ Fetches the commit history for all repositories for a given organisation from github.
        Return a pandas dataframe with repositories as columns, rows as time points, and commit messages as values. """
    
    if auth is None:
        auth = promptUsernameAndPassword()
    
    
    getOrganizationRepositoriesURL = "https://api.github.com/orgs/{org}/repos"
    
    r = requests.get(getOrganizationRepositoriesURL.format(org=organisation),auth=auth)
    
    if r.status_code == NO_RESULTS: #No repositories
        return None
    if not r.ok:
        r.raise_for_status()
    
    repositories = r.json()
    
    allCommitSeries = {}
    
    for repository in repositories:
    
        name = repository[u"name"]
        commitURL = repository[u"commits_url"].replace(u"{/sha}","")
        
        commitSeries = _fetchCommits(commitURL,auth)
        if commitSeries is not None:
            allCommitSeries[name] = (commitSeries)
    
    return DataFrame(allCommitSeries)


def mostCommonWeekdayAndHour(commitsDataFrame):
    """ Returns the most common day of the week and hour of the day for commits """
    
    hour = maxAverageCommits(commitsDataFrame,"hour")
    day = maxAverageCommits(commitsDataFrame,"day")

    return (calendar.day_name[day],hour)


def _fetchCommits(commitsURL,auth):
    """ Fetches all commit messages for a given repository time indexed as pandas series """

    r = requests.get(commitsURL,auth=auth)
    
    if r.status_code == NO_RESULTS: #Repository is empty
        return None
    if not r.ok:
        r.raise_for_status()
        
    commits = r.json()
    
    messages = []
    dates = []
    
    for commit in commits:
    
        message = commit[u"commit"][u"message"]
        date = parser.parse(commit[u"commit"][u"committer"][u"date"])
        
        dates.append(date)
        messages.append(message)
        
    return Series(messages, index=dates)


def promptUsernameAndPassword():
    """ Asks for username and password on the commandline. 
    Doesn't work in ipython notebook. """
    
    user = raw_input("User: ")
    password = getpass.getpass()
    
    return (user,password)
    
def readUsernameAndPassword(file):
    """ Reads username and password from a file. """
    
    with open(file) as secret:
        user = secret.readline().strip()
        pw = secret.readline().strip()
    
    return (user,pw)
    
    
def maxAverageCommits(commits,mode):
    """ Calculates the maximum average commits per hour of the day/day of the week """
    
    #Count none-NaN columns - allows for multiple commits at exactly the same time
    #Sum commits by time interval
    commitsByTime=commits.count(1).resample(mode[0].upper(),how='sum').fillna(0)
    
    if mode == 'hour':
        grouping = commitsByTime.index.hour
    elif mode == "day":
        grouping = commitsByTime.index.dayofweek
    else:
        raise ValueError("Mode should be 'hour' or 'day'")  
    
    #group commits and calculate the average
    averages = commitsByTime.groupby(grouping).mean()
    
    #retur max index of max value
    return averages.idxmax()
    
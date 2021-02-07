from github import Github, GithubException, BadCredentialsException, Label
import requests
import getpass
import sys

# ANSI color codes - irrelevant to moving issues, but I like colors in the terminal
BOLD = '\033[32;1m'  # Bold green text
END = '\033[0m'  # Reset to default color

def create_label(label):
    l = Label.Label()
    l.edit(label['name'], label['color'])
    return l


username = input('enter your username: ') # or put your GitHub username here
password = getpass.getpass(prompt='enter password: ')  # window users, password.getpass doesn't work for you. You'll need to replace with password= 'your password'


base_repo_name = input('enter the repo name e.g. readinglist for a repo located at https://github.com/claraj/readinglist/') 

source_url = 'https://api.github.com/repos/claraj/{}/issues'.format(base_repo_name)

github = Github(username, password)

base_repo = github.get_repo('claraj/' + base_repo_name)
base_issues = base_repo.get_issues()


your_repo = github.get_repo(username + "/" + base_repo_name)

labels = base_repo.get_labels()

try:

    print('Creating labels in your repository')
    for label in labels:
        try:
            your_repo.create_label(label.name, label.color)
        except GithubException:
            print('Error creating label %s. Does it already exist?' % label.name)


except BadCredentialsException:
    print('Username or password incorrect. Please run program again to start over.')
    sys.exit(-1)


print('Creating issues in your repository')

for issue in base_issues:
    try:
        your_repo.create_issue(issue.title, body=issue.body, labels=issue.labels)
        print (BOLD + 'Created issue with title: ' + issue.title + END +  "\n" + issue.body + '\n')
    except GithubException as e:
        print('Can\'t create issue. Make sure you have enabled issues in your repository.')
        sys.exit(-1)

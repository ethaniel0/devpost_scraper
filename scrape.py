import project
import user
import hackathon
from __fetch_lib import get_soup_from_link

def get_user(username):
    url = f'https://devpost.com/{username}'
    soup = get_soup_from_link(url)
    return user.User(soup)

def get_project(project_name):
    url = f'https://devpost.com/software/{project_name}'
    soup = get_soup_from_link(url)
    return project.Project(soup)

def get_hackathon(hackathon_name):
    url = f'https://{hackathon_name}.devpost.com'
    soup = get_soup_from_link(url)
    return hackathon.Hackathon(url, soup)

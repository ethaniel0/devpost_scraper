from bs4 import BeautifulSoup
from __fetch_lib import get_soup_from_link

class ProjectInfo:
    def __init__(self, link, img, title, description, members, likes, comments):
        self.link = link
        self.img = img
        self.title = title
        self.description = description
        self.members = members
        self.likes = likes
        self.comments = comments

class Hackathon:
    def __init__(self, link, soup: BeautifulSoup):
        self.soup = soup
        self.link = link
        self.date = self.__date()
        self.location = self.__location()
        self.type = self.__type()
        self.projects = self.__projects()
        
    def __date(self):
        calendar_icon = self.soup.find(class_="fa-calendar")
        return calendar_icon.parent.text.strip()
    def __location(self):
        globe_icon = self.soup.find(class_="fa-globe")
        return globe_icon.parent.text.strip()
    def __type(self):
        landmark_icon = self.soup.find(class_="fa-landmark")
        return landmark_icon.parent.text.strip()
    def __projects(self):
        url = self.link + "/project-gallery"
        soup = get_soup_from_link(url)
        
        projects = []
        projects.extend(self.__get_projects(soup))
        
        next = soup.find(class_="next_page")
        
        while next and not ('unavailable' in next.get('class')):
            url2 = self.link + next.find('a')['href']
            print('url2:', url2)
            soup = get_soup_from_link(url2)
            projects.extend(self.__get_projects(soup))
            next = soup.find(class_="next_page")
        
        return projects
    def __get_projects(self, soup):
        items = soup.find_all(class_="gallery-item")
        projects = []
        for item in items:
            projects.append(self.__parse_project(item))
        return projects        
    def __parse_project(self, gallery_item):
        link = gallery_item.find('a')['href']
        img = gallery_item.find('img')['src']
        body = gallery_item.find(class_="entry-body")
        title = body.find('h5').text.strip()
        description = body.find('p').text.strip()
        
        members = []
        for member in gallery_item.find_all(class_="user-profile-link"):
            members.append(member['data-url'])
            
        like_count = int(gallery_item.find(class_="like-count").text.strip())
        comment_count = int(gallery_item.find(class_="comment-count").text.strip())
        
        return ProjectInfo(link, img, title, description, members, like_count, comment_count)

from bs4 import BeautifulSoup
from .__fetch_lib import get_soup_from_link

class ProjectInfo:
    def __init__(self, link, img, title, description, members, likes, comments):
        self.link = link
        self.img = img
        self.title = title
        self.description = description
        self.members = members
        self.likes = likes
        self.comments = comments

    def __str__(self):
        return f"ProjectInfo(title={self.title}, link={self.link})"
    
    def __repr__(self):
        return self.__str__()

class Hackathon:
    def __init__(self, link: str, soup: BeautifulSoup):
        self.soup = soup
        try:
            self.link: str = link
            self.date: str = self.__date()
            self.location: str = self.__location()
            self.type: str = self.__type()
            self.projects: list[ProjectInfo] = self.__projects()
        except:
            self.link = None
            self.date = None
            self.location = None
            self.type = None
            self.projects = None
        
    def __date(self) -> str:
        calendar_icon = self.soup.find(class_="fa-calendar")
        return calendar_icon.parent.text.strip()
    def __location(self) -> str:
        globe_icon = self.soup.find(class_="fa-globe")
        if not globe_icon:
            globe_icon = self.soup.find(class_="fa-map-marker-alt")
        return globe_icon.parent.text.strip()
    def __type(self) -> str:
        landmark_icon = self.soup.find(class_="fa-landmark")
        return landmark_icon.parent.text.strip()
    def __projects(self) -> list[ProjectInfo]:
        url = self.link + "/project-gallery"
        soup = get_soup_from_link(url)
        
        projects = []
        projects.extend(self.__get_projects(soup))
        
        next = soup.find(class_="next_page")
        
        while next and not ('unavailable' in next.get('class')):
            url2 = self.link + next.find('a')['href']
            soup = get_soup_from_link(url2)
            projects.extend(self.__get_projects(soup))
            next = soup.find(class_="next_page")
        
        return projects
    def __get_projects(self, soup) -> list[ProjectInfo]:
        items = soup.find_all(class_="gallery-item")
        projects = []
        for item in items:
            projects.append(self.__parse_project(item))
        return projects        
    def __parse_project(self, gallery_item) -> ProjectInfo:
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

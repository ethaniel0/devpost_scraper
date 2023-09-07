from bs4 import BeautifulSoup

class User:
    def __init__(self, soup: BeautifulSoup):
        self.soup = soup
        self.name = self.__name()
        self.user_photo = self.__photo()
        self.location = self.__location()
        self.socials = self.__socials()
        self.skills = self.__skills()
        self.interests = self.__interests()
        
    def __name(self):
        user_el = self.soup.find(id="portfolio-user-name")
        small = user_el.find("small")
        user_id = small.text.strip().replace("(", '').replace(")", "")
        user_name = user_el.text.replace(small.text, "").strip()
        
        return (user_name, user_id)
    def __photo(self):
        return self.soup.find(class_="user-photo")["src"]
    def __location(self):
        icon = self.soup.find(class_="ss-location")
        if icon is None:
            return ""
        return icon.parent.text.strip()
    def __github(self):
        icon = self.soup.find(class_="ss-social")
        if icon is None:
            return ""
        return icon.parent.find('a')['href']
    def __linkedin(self):
        icon = self.soup.find(class_="ss-linkedin")
        if icon is None:
            return ""
        return icon.parent.find('a')['href']
    def __website(self):
        icon = self.soup.find(class_="ss-link")
        if icon is None:
            return ""
        return icon.parent.find('a')['href']
    def __skills(self):
        skills_container = None
        for lst in self.soup.find_all(class_="tag-list"):
            if lst.find('span').text.strip() == "Skills":
                skills_container = lst
                break
        lis = skills_container.find('ul').find_all('li')
        tags = []
        for li in lis:
            tags.append(li.text.strip())
        return tags 
    def __interests(self):
        interests_container = None
        for lst in self.soup.find_all(class_="tag-list"):
            if lst.find('span').text.strip() == "Interests":
                interests_container = lst
                break
        lis = interests_container.find('ul').find_all('li')
        tags = []
        for li in lis:
            tags.append(li.text.strip())
        
        return tags
    def __socials(self):
        socials = {}
        links = {
            "github": self.__github(),
            "linkedin": self.__linkedin(),
            "website": self.__website()
        }
        for item in links:
            link = links[item]()
            if link != "":
                socials[item] = link
        
        return socials
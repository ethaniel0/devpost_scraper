from bs4 import BeautifulSoup
from markdownify import markdownify 

class GalleryItem:
    
    def __init__(self, type: str, src: str, description: str):
        self.type: str = type
        self.src: str = src
        self.description: str = description

class Project:
    def __init__(self, soup: BeautifulSoup):
        self.soup = soup
        self.title, self.description = self.__title_and_description()
        self.about = self.__about()
        self.gallery = self.__gallery()
        self.built_with = self.__built_with()
        self.team = self.__team()
        self.links = self.__links()
        self.likes = self.__likes()
        
    def __title_and_description(self):
        title = self.soup.find(id='app-title')
        description = title.parent.find('p')
        return (title.text.strip(), description.text.strip())
    def __about(self):
        gallery = self.soup.find(id='gallery')
        next_div = gallery.find_next_sibling('div')
        innerhtml = next_div.decode_contents()
        md = markdownify(innerhtml, heading_style="ATX")
        return md.strip()
    def __gallery(self):
        gallery_el = self.soup.find(id='gallery')
        
        ul = gallery_el.find('ul')
        # find all divs of class slick-slide
        slide_els = ul.find_all('li')
        
        slides = []
        # within each slide, find either: 
        # - iframe inside a div with class flex-video
        # - img inside an a tag
        # add to slides as {type: iframe|img, src: src, description: description}
        
        for slide in slide_els:
            iframe = slide.find('iframe')
            if iframe is not None:
                slides.append(GalleryItem("iframe", iframe['src'], ""))
                continue
            img = slide.find('img')
            if img is not None:
                src: str = img['src']
                if src.startswith("//"):
                    src = "https:" + src
                elif src.startswith("/"):
                    src = "https://devpost.com" + src
                description = slide.find('a')['data-title']
                slides.append(GalleryItem("img", src, description))
                continue
        
        return slides
    def __built_with(self):
        # find tag with Id "build-with", then search for the ul tag enclosed in it. From there, find all tags with .cp-tag and extract innerText
        built_with = self.soup.find(id='built-with')
        ul = built_with.find('ul')
        lis = ul.find_all('li')
        
        tags = []
        for li in lis:
            tags.append(li.text.strip())
        return tags
    def __team(self):
        # get section with id app-team
        section = self.soup.find(id='app-team')
        ul = section.find('ul')
        people_els = ul.find_all('li', class_='software-team-member')
        
        people = []
        
        for person in people_els:
            bubble = person.find('div', class_='bubble')
            testemonial = bubble.text.strip()
            
            row = person.find('div', class_='row')
            divs = row.find_all('div')
            
            # get user image and profile link
            a = divs[0].find('a')
            user_link = a['href']
            img = a.find('img')
            src = img['src']
            name = img['title']
            
            people.append({
                "name": name,
                "image": src,
                "link": user_link,
                "testemonial": testemonial
            })
        
        return people
    def __links(self):
        # find ul with data-roll="software-urls"
        ul = self.soup.find('ul', attrs={"data-role": "software-urls"})
        a_tags = ul.find_all('a')
        links = []
        for a in a_tags:
            href = a['href']
            description: str = a.find('span').text.strip()
            links.append({
                "href": href,
                "description": description
            })
        return links
    def __likes(self):
        a = self.soup.find('a', class_="like-button")
        count = a.find('span', class_="side-count").text.strip()
        return int(count)

from bs4 import BeautifulSoup
from markdownify import markdownify 

class GalleryItem:
    
    def __init__(self, type: str, src: str, description: str):
        self.type: str = type
        self.src: str = src
        self.description: str = description
        
    def __str__(self):
        return f"GalleryItem(type={self.type}, src={self.src}, description={self.description[:10]})"
    

class Project:
    def __init__(self, soup: BeautifulSoup):
        self.soup = soup
        title, desc = self.__title_and_description()
        self.title: str = title
        self.description: str = desc
        self.about: str = self.__about()
        self.gallery: list[GalleryItem] = self.__gallery()
        self.built_with: list[str] = self.__built_with()
        self.team: list[dict] = self.__team()
        self.links: list[dict] = self.__links()
        self.likes: int = self.__likes()
        
    def __title_and_description(self) -> tuple[str, str]:
        title = self.soup.find(id='app-title')
        description = title.parent.find('p')
        return (title.text.strip(), description.text.strip())
    def __about(self) -> str:
        gallery = self.soup.find(id='gallery')
        if gallery is None:
            return ""
        next_div = gallery.find_next_sibling('div')
        innerhtml = next_div.decode_contents()
        md = markdownify(innerhtml, heading_style="ATX")
        return md.strip()
    def __gallery(self) -> list[GalleryItem]:
        gallery_el = self.soup.find(id='gallery')
        if gallery_el is None:
            return []
        
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
                desc_tag = slide.find('a')
                if desc_tag and desc_tag.has_attr('data-title'):
                    description = desc_tag['data-title']
                else:
                    description = ""
                slides.append(GalleryItem("img", src, description))
                continue
        
        return slides
    def __built_with(self) -> list[str]:
        # find tag with Id "build-with", then search for the ul tag enclosed in it. From there, find all tags with .cp-tag and extract innerText
        built_with = self.soup.find(id='built-with')
        ul = built_with.find('ul')
        lis = ul.find_all('li')
        
        tags = []
        for li in lis:
            tags.append(li.text.strip())
        return tags
    def __team(self) -> list[dict]:
        # get section with id app-team
        section = self.soup.find(id='app-team')
        ul = section.find('ul')
        people_els = ul.find_all('li', class_='software-team-member')
        
        people = []
        
        for person in people_els:
            bubble = person.find('div', class_='bubble')
            if bubble:
                testemonial = bubble.text.strip()
            else:
                testemonial = ""
            
            row = person.find('div', class_='row')
            divs = row.find_all('div')
            
            # get user image and profile link
            a = divs[0].find('a')
            user_link = ""
            if a:
                user_link = a['href']
            img = divs[0].find('img')
            src = img['src']
            name = img['title'] 
            
            people.append({
                "name": name,
                "image": src,
                "link": user_link,
                "testemonial": testemonial
            })
        
        return people
    def __links(self) -> list[dict]:
        # find ul with data-roll="software-urls"
        links = []
        
        ul = self.soup.find('ul', attrs={"data-role": "software-urls"})
        if ul is None:
            return links
        a_tags = ul.find_all('a')
        if a_tags is None:
            return links
        
        for a in a_tags:
            href = a['href']
            description: str = a.find('span').text.strip()
            links.append({
                "href": href,
                "description": description
            })
        return links
    def __likes(self) -> int:
        a = self.soup.find('a', class_="like-button")
        span = a.find('span', class_="side-count")
        if span is None:
            return 0
        count = span.text.strip()
        return int(count)

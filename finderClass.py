import re
import requests
from bs4 import BeautifulSoup
import json
class FacebookPostLinkExtractor:
    def __init__(self):
        self.pattern = re.compile(r'(value)*\w{9,11}[:"][:"]\d{15,17}')
        self.pattern2 = re.compile(r'value="(\d{15,16})"')
        self.pattern3 = re.compile(r'(id)*\w{15}')
        self.pattern4 = re.compile(r'"entity_id":"(\d{15,16})"')
        self.pattern5 = re.compile(r'fbid=(\w{15,16})')
        self.link_pattern = r'link href="https://www\.facebook\.com/[^/]+/posts/[^/]+/\d+/"'
    def get_facebook_post_link(self, link):
        try:
            if 'm.f' in link:
                return self.extract_post_link_from_mf(link)
                
            else:
                return self.extract_post_link_from_posts(link)
        except Exception as exc:
            return str(exc)

    def extract_post_link_from_posts(self, link):
        link = link.replace("m.f", "www.f")
        res = requests.get(link)
        soup_data = BeautifulSoup(res.text, 'html.parser')
        
        match = re.search(self.link_pattern, soup_data.prettify())
        if match:
            link = match.group()
            
            link2 = link.strip('link href=').strip('"').split('/')
            
            link3 = 'https://www.facebook.com/{}/posts/{}/'.format(link2[3],link2[6])
            result = link3
        return result


    def extract_post_link_from_mf(self, link):
        link = link.replace("m.f", "www.f")
        storyid_matches = self.pattern5.finditer(link)
        storyid_match = [object[0] for object in storyid_matches]
        profileid_matches = self.pattern3.finditer(link)
        profileid_match = [object[0] for object in profileid_matches]
        result = "https://www.facebook.com/{0}/posts/{1}".format(
            profileid_match[1], storyid_match[0].split("=")[1])
        return result

if __name__ == "__main__":
    FacebookPostLinkExtractor.get_facebook_post_link()
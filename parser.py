from bs4 import BeautifulSoup


class AdvertisementParser():

    # *title
    # *price
    # *body
    # *post_id
    # *created_time

    def __init__(self):
        self.soup = None

    @property
    def title(self):
        title_tag = self.soup.find('span', attr={'id': 'titletextonly'})
        if title_tag:
            return title_tag.text
        return None

    @property
    def price(self):
        price_tag = self.soup.find('span', attrs={'class': 'price'})
        if price_tag:
            return price_tag.text
        return None

    @property
    def post_id(self):
        post_id_selection = 'body > section > section > section > div.postinginfos > p:nth-child(1)'
        post_id_tag = self.soup.select_one(post_id_selection)
        if post_id_tag:
            return post_id_tag.text.replace('post id: ', '')
        return None

    @property
    def images(self):
        images_list = self.soup.find_all('img')
        images_sources = set([img.attrs['src'].replace('50x50c', '600x450') for img in images_list])
        return [{"url": src, 'flag': False} for src in images_sources]


    def parse(self, html_data):
        self.soup = BeautifulSoup(html_data, 'html.parser')
        data = {
            'title': self.title, 'price': self.price, 'post_id': self.post_id, 'images': self.images
        }
        return data


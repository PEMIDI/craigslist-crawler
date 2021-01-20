from bs4 import BeautifulSoup


class AdvertisementParser():

    def parse(self, html_data):

        soup = BeautifulSoup(html_data, 'html.parser')

        data = {
            'title':None, 'price': None, 'post_id': None
        }

        title_tag = soup.find('span', attrs={'id': 'titletextonly'})
        if title_tag:
            data['title'] = title_tag.text

        price_tag = soup.find('span', attrs={'class': 'price'})
        if price_tag:
            data['price'] = price_tag.text


        return data
    
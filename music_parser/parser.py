import logging
from grab import Grab
from bs4 import BeautifulSoup
import urllib.parse as url_parse
from flask import abort
from flask import url_for

logger = logging.getLogger('grab')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

g_object = Grab()
g_object.setup(log_dir='log')
web_url = 'https://music.yandex.ru'


class Artist:
    def __init__(self, name, href, genres, avatar):
        self.name = name
        self.genres = genres
        self.href = href
        self.avatar = avatar

    def __str__(self):
        artist_string = f'\nИмя исполнителя:\n\t{self.name}\nЖанры:\n'
        for genre in self.genres:
            artist_string += f'\t{genre}'
        return artist_string


class Genre:
    def __init__(self, name, href):
        self.name = name
        self.href = href

    def __str__(self):
        return self.name


def create_artist_list(elems):
    artist_list = []

    for artist in elems:
        genres_list = []
        link = artist.find('a', 'd-link', 'deco-link')
        name = link.getText()

        link_href = url_parse.urljoin(web_url, link['href'])

        try:
            genres = artist.find('div', 'd-genres').find_all('a')
            for genre in genres:
                genre_name = genre.getText()
                genre_href = url_parse.urljoin(web_url, genre['href'])
                genres_list.append(Genre(genre_name, genre_href))
        except:
            genre_name = 'Неизвестно'
            genre_href = '#'
            genres_list.append(Genre(genre_name, genre_href))

        avatar_link = artist.find('img', 'artist-pics__pic')['src']
        if avatar_link == '/blocks/artist-pics/placeholder-artist.svg':
            avatar_link = url_for('static', filename='images/no-image.png')

        new_artist = Artist(name, link_href, genres_list, avatar_link)
        artist_list.append(new_artist)
    return artist_list


def collect_genres(artist_list):
    genres_names = []
    genres_list = []
    for artist in artist_list:
        for genre in artist.genres:
            if genre.name not in genres_names:
                genres_list.append(genre)
                genres_names.append(genre.name)
    return genres_list


def main(g, name):
    g.go(f'{web_url}/users/{name}/artists')
    resp = g.doc

    if resp.code == 404:
        abort(404)

    if not 200 <= resp.code <= 400:
        raise Exception(f'response not valid: {resp.code}')

    result = resp.unicode_body()
    soup = BeautifulSoup(result, 'lxml')
    artists_html = soup.find_all('div', 'artist')

    artists = create_artist_list(artists_html)
    genres_list = collect_genres(artists)

    return [artists, genres_list]


if __name__ == '__main__':
    main(g_object, 'filipp.pravda')

































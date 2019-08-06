import logging
from bs4 import BeautifulSoup
import urllib.parse as url_parse
from flask import abort
from flask import url_for
import json
import requests

logger = logging.getLogger('grab')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

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

    def to_json_obj(self):
        genre_name_list = []
        for genre in self.genres:
            genre = str(genre)
            genre_name_list.append(genre)

        return {
            self.name: {
                'genres': genre_name_list,
                'href':   self.href,
                'avatar': self.avatar
            }
        }


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


def return_soup_if_ok(response):
    if response.status_code == 404:
        abort(404)

    if not 200 <= response.status_code <= 400:
        raise Exception(f'response not valid: {response.code}')

    result = response.text
    soup = BeautifulSoup(result, 'lxml')
    return soup


def main(name):
    resp = requests.get(f'{web_url}/users/{name}/artists')
    soup = return_soup_if_ok(resp)

    artists_html = soup.find_all('div', 'artist')
    artists = create_artist_list(artists_html)
    genres_list = collect_genres(artists)

    return [artists, genres_list]


def sub_query(artist_id):
    resp = requests.get(f'{web_url}/artist/{artist_id}/info')
    soup = return_soup_if_ok(resp)

    artist_title = soup.find('div', 'd-generic-page-head__main-top')
    name = str(artist_title.h1)
    like = artist_title.find('div', 'page-artist__summary').getText()

    artist_title = {
        'name': name,
        'like': like
    }

    try:
        artist_info = soup.find('div', 'page-artist__description').getText()
    except AttributeError:
        artist_info = 'Нет описания исполнителя.'

    resp = requests.get(f'{web_url}/artist/{artist_id}/similar')
    soup = return_soup_if_ok(resp)

    artists_html = soup.find_all('div', 'artist')
    artists = create_artist_list(artists_html)

    artists_for_json = []

    for artist in artists:
        artists_for_json.append(artist.to_json_obj())

    json_obj = {
        'info':    artist_info,
        'title':   artist_title,
        'similar': artists_for_json
    }
    return json.dumps(json_obj)


if __name__ == '__main__':
    print('\nThis is part of flask app.\nGoodbye.')

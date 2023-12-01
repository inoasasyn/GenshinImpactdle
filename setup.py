from bs4 import *
import requests
import re
import urllib.request
import os

from Character import Character
from finder import find_by_name, find_by_element, find_by_region, find_by_weapon_type, find_by_ascension_boss_drop, \
    find_by_ascension_local_speciality, find_by_ascension_mob_drop


def scrap_all_characters():
    first_url = "https://genshin-impact.fandom.com/wiki/Character/List"
    response = requests.get(first_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    indiatable = soup.find_all('table', limit=1)

    character_urls = re.findall(r'<tr>\n<td><a href=".*?"', str(indiatable[0]))
    for i in range(len(character_urls)):
        character_urls[i] = "https://genshin-impact.fandom.com" + character_urls[i][18:-1]

    characters = create_character_objects(open_character_file())

    #mock
    character_urls = character_urls

    if len(character_urls) != len(characters):
        i = 0
        all_chars = re.findall(r'<tr>.*?</tr>', str(indiatable[0]), flags=re.DOTALL)
        for j in range(1, len(all_chars)):
            all_chars[j] = re.findall(r'<td>.*?</td>', all_chars[j], flags=re.DOTALL)
        for url in character_urls:
            name = re.search('/wiki/', url)
            name = url[name.end():]
            name = re.sub('_', " ", name)
            is_character_in = find_by_name(characters, name)
            if not is_character_in:
                icon_url = re.findall(r'src=".*?"', all_chars[i+1][0], flags=re.DOTALL)[0]
                icon_url = get_url(icon_url)
                get_img(icon_url, name)

                response = requests.get(url)
                soup = BeautifulSoup(response.text, 'html.parser')

                rarity = re.findall(r'<td class="pi-horizontal-group-item pi-data-value pi-font pi-border-color pi-item-spacing" data-source="quality"><img alt="[4-5]', str(soup))[-1][-1]

                weapon = re.findall(r'<td class="pi-horizontal-group-item pi-data-value pi-font pi-border-color pi-item-spacing" data-source="weapon">.*? title=".*?"', str(soup))[-1]
                weapon_end_index = re.search('title="', weapon)
                weapon = weapon[weapon_end_index.end():-1]
                is_weapon_in = find_by_weapon_type(characters, weapon)
                if not is_weapon_in:
                    weapon_url = re.findall(r'src=".*?"', all_chars[i + 1][4], flags=re.DOTALL)[0]
                    weapon_url = get_url(weapon_url)
                    get_img(weapon_url, weapon)

                element = re.findall(r'<td class="pi-horizontal-group-item pi-data-value pi-font pi-border-color pi-item-spacing" data-source="element">.*?title=".*?"', str(soup))
                if len(element) > 0:
                    element = element[-1]
                    element_end_index = re.search('title="', element)
                    element = element[element_end_index.end():-1]
                    is_element_in = find_by_element(characters, element)
                    if not is_element_in:
                        element_url = re.findall(r'src=".*?"', all_chars[i + 1][3], flags=re.DOTALL)[0]
                        element_url = get_url(element_url)
                        get_img(element_url, element)
                else:
                    element = "None"

                model_type = re.findall(r'title=".*?>.*?</a>', all_chars[i + 1][6], flags=re.DOTALL)[0][:-4]
                model_type_start_index = re.search(r'Characters">', model_type)
                model_type = model_type[model_type_start_index.end():]

                region = re.findall(r'Region.*?\n.*?title=".*?"', str(soup))
                if len(region) > 0:
                    region = region[-1]
                    region_end_index = re.search('title="', region)
                    region = region[region_end_index.end():-1]
                    is_region_in = find_by_region(characters, region)
                    if not is_region_in:
                        region_url = re.findall(r'src=".*?"', all_chars[i + 1][5], flags=re.DOTALL)[0]
                        region_url = get_url(region_url)
                        get_img(region_url, region)
                else:
                    region = "None"

                special_stat = re.findall(r'Special Stat.*?title=".*?"', str(soup))[-1]
                special_stat_end_index = re.search('title="', special_stat)
                special_stat = special_stat[special_stat_end_index.end():-1]

                ascension_item = re.findall(r'</ol></div><b>Total Cost.*?</a></span></div></span>', str(soup))[0]
                ascension_item_icons_url = re.findall(r'data-image-name="Item.*?src=".*?"', ascension_item)

                ascension = [6, 1, 8]
                for number in ascension:
                    mat = ascension_item_icons_url[number]
                    mat_start_index = re.search('data-image-name="Item ', mat)
                    mat_end_index = re.search('png"', mat)
                    mat = mat[mat_start_index.end():mat_end_index.start() - 1]
                    if number == 6:
                        is_mat_in = find_by_ascension_local_speciality(characters, mat)
                    elif number == 1:
                        is_mat_in = find_by_ascension_boss_drop(characters, mat)
                    else:
                        is_mat_in = find_by_ascension_mob_drop(characters, mat)
                    if not is_mat_in:
                        mat_url = get_url(ascension_item_icons_url[number])
                        get_img(mat_url, mat)
                    ascension[ascension.index(number)] = mat
                ascension_local_speciality = ascension[0]
                ascension_boss_drop = ascension[1]
                ascension_mob_drop = ascension[2]

                release_date = re.findall(r'Release_Date.*?\n.*?>.*?<', str(soup))[-1]
                release_date_end_index = re.search('font">', release_date)
                release_date = release_date[release_date_end_index.end():-1]

                help_version = re.findall(r'<td><a href="/wiki/.*?" title=".*?">.*?</a>', str(indiatable[0]))
                indices = [i for i, s in enumerate(help_version) if name in s][0]
                version = re.findall(r'<td><a href="/wiki/Version/.*?</a>', str(indiatable[0]))[int(indices/4)]
                version_end_index = re.search('">', version)
                version = version[version_end_index.end():-4]

                #print(name, rarity, element, model_type, region, special_stat, ascension_local_speciality,
                #      ascension_boss_drop, ascension_mob_drop, release_date, version)
                new_character = [name, rarity, element, weapon, model_type, region, special_stat,
                                 ascension_local_speciality, ascension_boss_drop, ascension_mob_drop, release_date,
                                 version]
                add_character(new_character)
                characters.append(create_character_objects([new_character])[0])
            i += 1
    return characters


def get_url(table):
    table_start_index = re.search('src="', table)
    table = table[table_start_index.end():-1]
    table_end_index = re.search('down/', table)
    table = table[:table_end_index.end()] + "200"
    return table


def get_img(url, name):
    name = re.sub(' ', '_', name)
    png_name = name + "_Icon.png"
    urllib.request.urlretrieve(url, png_name)
    data = requests.get(url).content
    png_path = 'Icons/' + png_name
    f = open(png_path, 'wb')
    f.write(data)
    f.close()
    os.remove(png_name)


def open_character_file():
    f = open("characters.csv", 'r')
    character_data = []
    for line in f:
        line = line[:-1]
        character_data.append(line.split('; '))
    return character_data


def add_character(data):
    f = open("characters.csv", 'a')
    data_in = '; '.join(data) + '\n'
    f.write(data_in)
    f.close()


def create_character_objects(data):
    character_obj = []
    for character in data:
        c1 = Character(character[0], character[1], character[2], character[3], character[4], character[5], character[6],
                       character[7], character[8], character[9], character[10], character[11])
        character_obj.append(c1)
    return character_obj


scrap_all_characters()

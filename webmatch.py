# from lxml import etree
# from lxml.html import fromstring
# import requests
# import selenium
import time
# from urllib.request import urlopen
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
import webcolors
import ast
import sys


# def match_text_length(elem, min_length, max_length):
#     if min_length == '':
#         min_length = 0
#     if max_length =='':
#         max_length = 1000

#     if elem.text and len(elem.text) >= min_length and len(elem.text) <= max_length:
#         return True
#     else:
#         try:
#             elem.find_element_by_tag_name('a')
#             if elem.find_element_by_tag_name('a').text:
#                 if len(elem.find_element_by_tag_name('a').text) >= min_length and len(elem.find_element_by_tag_name('a').text) <= max_length:
#                     return True
#         except:
#             pass
#     return False
def match_text_length(node, min_length, max_length):
    if min_length == '':
        min_length = 0
    if max_length == '':
        max_length = 1000

    if node and len(node['text']) >= min_length and len(node['text']) <= max_length:
        return True

    return False



def match_font_size(node, font_size):
    if font_size == '' or node['font_size'] == font_size:
        return True
    return False

# def closest_colour(requested_colour):
#     min_colours = {}
#     for key, name in webcolors.css3_hex_to_names.items():
#         r_c, g_c, b_c = webcolors.hex_to_rgb(key)
#         rd = (r_c - requested_colour[0]) ** 2
#         gd = (g_c - requested_colour[1]) ** 2
#         bd = (b_c - requested_colour[2]) ** 2
#         min_colours[(rd + gd + bd)] = name
#     return min_colours[min(min_colours.keys())]

# def match_font_color(elem, font_color):
#     if font_color == '':
#         return True
#     color = elem.value_of_css_property('color')
#     if color:
#         r,g,b, alpha = ast.literal_eval(color.strip("rgba"))
#         rgb = []
#         rgb.append(r)
#         rgb.append(g)
#         rgb.append(b)
#         try:
#             color_name = webcolors.rgb_to_name(rgb)
#         except ValueError:
#             color_name = closest_colour(rgb)
#         if color_name == font_color.lower():
#             return True
#         else:
#             return False
#     return False

# def match_class_name(elem, class_name):

#     if class_name == '' or elem.get_attribute('class') == class_name:
#         return True
#     return False

def match_image_size(node, image_minht, image_minwd, image_maxht, image_maxwd):

    if image_minht == '':
        image_minht = 0
    if image_minwd =='':
        image_minwd = 0

    getht = node['height']
    getwd = node['width']

    if image_maxht == '' and image_maxwd == '':
        return True
    if image_maxht == '' and (getwd >= image_minwd and getwd <= image_maxwd):
        return True
    elif image_maxwd == '' and (getht >= image_minht and getht <= image_maxht):
        return True
    elif (getwd >= image_minwd and getwd <= image_maxwd) and (getht >= image_minht and getht <= image_maxht):
        return True
    else:
        return False

def match_image_location(node, image_minx, image_miny, image_maxx, image_maxy):

    if image_minx == '':
        image_minx = 0
    if image_miny =='':
        image_miny = 0

    getxloc = node['x']
    getyloc= node['y']

    if image_maxx == '' and image_maxy == '':
        return True
    if image_maxx == '' and (getyloc >= image_miny and getyloc <= image_maxy):
        return True
    elif image_maxy == '' and (getxloc >= image_minx and getxloc <= image_maxx):
        return True
    elif (getyloc >= image_miny and getyloc <= image_maxy) and (getxloc >= image_minx and getxloc <= image_maxx):
        return True
    else:
        return False


def match(all_nodes, tag_name='p', min_length=0, max_length=sys.maxsize, font_size='', font_color='', class_name='', ext_type = 'text',\
          image_minht = '', image_minwd = '', image_maxht = '', image_maxwd = '',\
          image_minx ='', image_miny='', image_maxx='', image_maxy=''):

    matched_nodes = []

    print(len(all_nodes))

    for node in all_nodes:
        # try:
        #     elem = driver.find_element_by_xpath(path)
        # except:
        #     continue
        if ext_type == 'text':
            if match_text_length(node, min_length, max_length) and match_font_size(node, font_size):
                matched_nodes.append(node['num'])
        if ext_type == 'image':
            if match_image_size(node,image_minht,image_minwd,image_maxht,image_maxwd) and \
               match_image_location(node, image_minx, image_miny, image_maxx, image_maxy):
                matched_nodes.append(node['num'])

    return matched_nodes

import time
import webcolors
import ast
import sys
import re
from collections import defaultdict 


def match_text_length(node, min_length, max_length):
    if min_length == '':
        min_length = 0
    if max_length == '':
        max_length = 1000

    if node and len(node['text']) >= min_length and len(node['text']) <= max_length:
        return True

    return False

def match_str_contains(node, substring):
    if substring == '':
        return True

    if node and ((node['text'].lower()).find(substring.lower()) != -1):
        return True

    return False

def match_str_begins(node, substring):
    if substring == '':
        return True

    if node and ((node['text'].lower()).find(substring.lower()) == 0):
        return True

    return False

def match_str_regex(node, regex_string):
    if regex_string == '':
        return True

    searchObj = re.search(regex_string, node['text'], re.M | re.I) 

    if node and searchObj:
        return True

    return False


def match_font_size(node, font_size):
    if font_size == '' or node['font_size'] == font_size:
        return True
    return False

'''def closest_colour(requested_colour):
    min_colours = {}
    for key, name in webcolors.css3_hex_to_names.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_colour[0]) ** 2
        gd = (g_c - requested_colour[1]) ** 2
        bd = (b_c - requested_colour[2]) ** 2
        min_colours[(rd + gd + bd)] = name
    return min_colours[min(min_colours.keys())]

def match_font_color(node, font_color):
    if font_color == '':
        return True
    color = node['font_color']
    if color:
        r,g,b, alpha = ast.literal_eval(color.strip("rgba"))
        rgb = []
        rgb.append(r)
        rgb.append(g)
        rgb.append(b)
    try:
        color_name = webcolors.rgb_to_name(rgb)
    except ValueError:
        color_name = closest_colour(rgb)
    if color_name == font_color.lower():
        return True
    else:
        return False
    return False'''

def match_class_name(node, class_name):

    if class_name == '' or node['class'] == class_name:
     return True
    return False


def match_all_images(node):

    if node['tag'] == 'IMG':
        return True
    return False

def match_all_nonimages(node):

    if node['tag'] != 'IMG':
        return True
    return False


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

def match_left_align(all_nodes):
    
    #Group nodes that have same xposition, key is x location, value is list of node numbers
    left_align = defaultdict(list)    
    for node in all_nodes:
        xloc = node['x']
        left_align[xloc].append(node['id'])

    #Return the key group with most number of entries    
    maxkey = max(left_align.keys(), key=(lambda k: len(left_align[k]))) 
    return left_align[maxkey]

def match_right_align(all_nodes):
    
    #Group nodes that have same xposition + width, key is xposition + width, value is list of node numbers
    right_align = defaultdict(list)
    for node in all_nodes:
        xloc = node['x']
        width = node['width']        
        right_align[xloc + width].append(node['id'])

    #Return the key group with most number of entries    
    maxkey = max(right_align.keys(), key=(lambda k: len(right_align[k])))
    return right_align[maxkey]

def match_bottom_align(all_nodes):
    
    #Group nodes that have same ypos, key is ypos, value is list of node numbers
    bottom_align = defaultdict(list)
    for node in all_nodes:
        yloc = node['y']
        bottom_align[yloc].append(node['id'])

    #Return the key group with most number of entries    
    maxkey = max(bottom_align.keys(), key=(lambda k: len(bottom_align[k])))
    return bottom_align[maxkey]

def match_top_align(all_nodes):
    
    #Group nodes that have same ypos + height, key is ypos + height, value is list of node numbers
    top_align = defaultdict(list)
    for node in all_nodes:
        yloc = node['y']
        height = node['height']            
        top_align[yloc + height].append(node['id'])

    #Return the key group with most number of entries    
    maxkey = max(top_align.keys(), key=(lambda k: len(top_align[k])))
    return top_align[maxkey]


def match_vertical_align(all_nodes):
    
    #Intersection of left and right align
    left_align = match_left_align(all_nodes)
    right_align = match_right_align(all_nodes)
    
    #print(left_align,right_align)
    return list(set(left_align) & set(right_align))
    

    


def match_horizontal_align(all_nodes):
    
    #Intersection of top and bottom align
    top_align = match_top_align(all_nodes)
    bottom_align = match_bottom_align(all_nodes)
    
    #print(top_align,bottom_align)
    return list(set(top_align) & set(bottom_align))

    

    
def match(all_nodes, tag_name='p', min_length=0, max_length=sys.maxsize, font_size='', font_color='', class_name='', ext_type = 'text',\
          text_begins = '', text_contains = '', regex_string = '',\
          image_minht = '', image_minwd = '', image_maxht = '', image_maxwd = '',\
          image_minx ='', image_miny='', image_maxx='', image_maxy='', align = ''):

    initial_matched_nodes = []
    matched_nodes = []

    print("length", len(all_nodes))
    print("tag_name", tag_name)

    additional_filters = []

    
    
    for node in all_nodes.keys():

        '''if all_nodes[node]['tag'] == tag_name:
            print("L1:",tag_name, all_nodes[node]['tag'], all_nodes[node]['class'])'''

        
        
        if ext_type == 'text':
            if match_text_length(all_nodes[node], min_length, max_length) and match_font_size(all_nodes[node], font_size) and match_class_name(all_nodes[node],class_name) and \
               match_str_contains(all_nodes[node],text_contains) and match_str_begins(all_nodes[node],text_begins) and match_str_regex(all_nodes[node],regex_string) \
               and all_nodes[node]['tag'] == tag_name: 
                initial_matched_nodes.append(all_nodes[node]['id'])
                additional_filters.append(all_nodes[node])
        if ext_type == 'image':
            if match_all_images(all_nodes[node]) and match_image_size(all_nodes[node],image_minht,image_minwd,image_maxht,image_maxwd) and \
               match_image_location(all_nodes[node], image_minx, image_miny, image_maxx, image_maxy):
                initial_matched_nodes.append(all_nodes[node]['id'])
                additional_filters.append(all_nodes[node])

    #print("Initial", initial_matched_nodes)
    


    if align == 'left':
        matched_nodes = match_left_align(additional_filters)
        return matched_nodes

    elif align == 'right':
        matched_nodes = match_right_align(additional_filters)
        return matched_nodes

    elif align == 'top':
        matched_nodes = match_top_align(additional_filters)
        return matched_nodes

    elif align == 'bottom':
        matched_nodes = match_bottom_align(additional_filters)
        return matched_nodes

    elif align =='vertical':
        matched_nodes = match_vertical_align(additional_filters)
        return matched_nodes

    elif align == 'horizontal':
        matched_nodes = match_horizontal_align(additional_filters)
        return matched_nodes

    else:
        return initial_matched_nodes

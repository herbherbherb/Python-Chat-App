# import requests
import json
# from flask import request, Flask,render_template,json
# from html.parser import HTMLParser
import webmatch
from ParseJsonQuery import ParseJsonQuery


def query_filter(res=None, query = None):
    pq = ParseJsonQuery(query)

    fieldlist = pq.parsedquery['extract.fields']
    resdict = {}
    #This helps in getting more than one field : like price and laptop titles
    for each_field in fieldlist:
        identifier = each_field['Field_id']
        requirements = each_field['match']
        tagname = each_field['match']['tagName']

        if "fontColor" not in requirements:
            requirements['fontColor'] = ''
        if "fontSize" not in requirements:
            requirements['fontSize'] = ''
        if "className" not in requirements:
            requirements['className'] = ''
        if "TextLength" not in requirements:
            requirements['minTextLength'] = ''
            requirements['maxTextLength'] = ''
        else:
            requirements['minTextLength'] = ''
            requirements['maxTextLength'] = ''
            if 'lt' in requirements['TextLength']:
                requirements['maxTextLength'] = requirements['TextLength']['lt']
            if 'gt' in requirements['TextLength']:
                requirements['minTextLength'] = requirements['TextLength']['gt']
        if "imgXLoc" not in requirements:
            requirements['imgminXLoc'] = ''
            requirements['imgmaxXLoc'] = ''
        else:
            requirements['imgminXLoc'] = ''
            requirements['imgmaxXLoc'] = ''
            if 'lt' in requirements["imgXLoc"]:
                requirements['imgmaxXLoc'] = requirements["imgXLoc"]['lt']
            if 'gt' in requirements["imgXLoc"]:
                requirements['imgminXLoc'] = requirements["imgXLoc"]['gt']
        if "imgYLoc" not in requirements:
            requirements['imgminYLoc'] = ''
            requirements['imgmaxYLoc'] = ''
        else:
            requirements['imgminYLoc'] = ''
            requirements['imgmaxYLoc'] = ''
            if 'lt' in requirements["imgYLoc"]:
                requirements['imgmaxYLoc'] = requirements["imgYLoc"]['lt']
            if 'gt' in requirements["imgXLoc"]:
                requirements['imgminYLoc'] = requirements["imgYLoc"]['gt']
        if "imgWidth" not in requirements:
            requirements['imgminWidth'] = ''
            requirements['imgmaxWidth'] = ''
        else:
            requirements['imgminWidth'] = ''
            requirements['imgmaxWidth'] = ''
            if 'lt' in requirements["imgWidth"]:
                requirements["imgmaxWidth"] = requirements["imgWidth"]['lt']
            if 'gt' in requirements["imgWidth"]:
                requirements["imgminWidth"] = requirements["imgWidth"]['gt']
        if "imgHeight" not in requirements:
            requirements['imgminHeight'] = ''
            requirements['imgmaxHeight'] = ''
        else:
            requirements['imgminHeight'] = ''
            requirements['imgmaxHeight'] = ''
            if 'lt' in requirements["imgHeight"]:
                requirements["imgmaxHeight"] = requirements["imgHeight"]['lt']
            if 'gt' in requirements["imgHeight"]:
                requirements["imgminHeight"] = requirements["imgHeight"]['gt']
        matched_nodes = webmatch.match(res,tagname,font_color=requirements['fontColor'],\
                                      font_size=requirements['fontSize'],min_length = requirements['minTextLength'],\
                                      max_length = requirements['maxTextLength'],class_name=requirements['className'], \
                                      ext_type = requirements['type'], \
                                      image_minht = requirements['imgminHeight'],image_minwd = requirements['imgminWidth'],\
                                      image_maxht = requirements['imgmaxHeight'], image_maxwd = requirements['imgmaxWidth'], \
                                      image_minx = requirements['imgminXLoc'],image_miny = requirements['imgminYLoc'],\
                                      image_maxx = requirements['imgmaxXLoc'], image_maxy = requirements['imgmaxYLoc'])



        resdict[identifier] = matched_nodes





    if query:
        return json.dumps(resdict)

    return json.dumps({'error' : 'Query is missing or URL fetch failed'})



# @app.route('/GetandParse', methods=['POST'])
# def GetandParse():
#     print (request)
#     serialized_nodes = test();
#     query = request.form['query']
#     fid = request.form['fieldid']
#     matchitem = request.form['match']
#     query = "{\"extract\":{\"fields\":[{" + "\"Field_id\":" +    fid     +    ",\"match\":" + ""    +        matchitem        +      ""  + "}]} }"

#     print(query)
#     pq = ParseJsonQuery(query)

#     fieldlist = pq.parsedquery['extract.fields']
#     resdict = {}
#     #This helps in getting more than one field : like price and laptop titles
#     for each_field in fieldlist:
#         identifier = each_field['Field_id']
#         requirements = each_field['match']
#         tagname = each_field['match']['tagName']

#         if "fontColor" not in requirements:
#             requirements['fontColor'] = ''
#         if "fontSize" not in requirements:
#             requirements['fontSize'] = ''
#         if "className" not in requirements:
#             requirements['className'] = ''
#         # if "minTextLength" not in requirements:
#         #     requirements['minTextLength'] = ''
#         # if "maxTextLength" not in requirements:
#         #     requirements['maxTextLength'] = ''






#         if "TextLength" not in requirements:
#             requirements['minTextLength'] = ''
#             requirements['maxTextLength'] = ''
#         else:
#             print('sss')
#             requirements['minTextLength'] = ''
#             requirements['maxTextLength'] = ''
#             if 'lt' in requirements['TextLength']:
#                 requirements['maxTextLength'] = requirements['TextLength']['lt']
#             if 'gt' in requirements['TextLength']:
#                 requirements['minTextLength'] = requirements['TextLength']['gt']
#         if "imgXLoc" not in requirements:
#             requirements['imgminXLoc'] = ''
#             requirements['imgmaxXLoc'] = ''
#         else:
#             requirements['imgminXLoc'] = ''
#             requirements['imgmaxXLoc'] = ''
#             if 'lt' in requirements["imgXLoc"]:
#                 requirements['imgmaxXLoc'] = requirements["imgXLoc"]['lt']
#             if 'gt' in requirements["imgXLoc"]:
#                 requirements['imgminXLoc'] = requirements["imgXLoc"]['gt']
#         if "imgYLoc" not in requirements:
#             requirements['imgminYLoc'] = ''
#             requirements['imgmaxYLoc'] = ''
#         else:
#             requirements['imgminYLoc'] = ''
#             requirements['imgmaxYLoc'] = ''
#             if 'lt' in requirements["imgYLoc"]:
#                 requirements['imgmaxYLoc'] = requirements["imgYLoc"]['lt']
#             if 'gt' in requirements["imgXLoc"]:
#                 requirements['imgminYLoc'] = requirements["imgYLoc"]['gt']
#         if "imgWidth" not in requirements:
#             requirements['imgminWidth'] = ''
#             requirements['imgmaxWidth'] = ''
#         else:
#             requirements['imgminWidth'] = ''
#             requirements['imgmaxWidth'] = ''
#             if 'lt' in requirements["imgWidth"]:
#                 requirements["imgmaxWidth"] = requirements["imgWidth"]['lt']
#             if 'gt' in requirements["imgWidth"]:
#                 requirements["imgminWidth"] = requirements["imgWidth"]['gt']
#         if "imgHeight" not in requirements:
#             requirements['imgminHeight'] = ''
#             requirements['imgmaxHeight'] = ''
#         else:
#             requirements['imgminHeight'] = ''
#             requirements['imgmaxHeight'] = ''
#             if 'lt' in requirements["imgHeight"]:
#                 requirements["imgmaxHeight"] = requirements["imgHeight"]['lt']
#             if 'gt' in requirements["imgHeight"]:
#                 requirements["imgminHeight"] = requirements["imgHeight"]['gt']

#         print(requirements)
#         matched_nodes = webmatch.match(serialized_nodes,tagname,font_color=requirements['fontColor'],\
#                                       font_size=requirements['fontSize'],min_length = requirements['minTextLength'],\
#                                       max_length = requirements['maxTextLength'],class_name=requirements['className'], \
#                                       ext_type = requirements['type'], \
#                                       image_minht = requirements['imgminHeight'],image_minwd = requirements['imgminWidth'],\
#                                       image_maxht = requirements['imgmaxHeight'], image_maxwd = requirements['imgmaxWidth'], \
#                                       image_minx = requirements['imgminXLoc'],image_miny = requirements['imgminYLoc'],\
#                                       image_maxx = requirements['imgmaxXLoc'], image_maxy = requirements['imgmaxYLoc'])



#         resdict[identifier] = matched_nodes




#     if url and query:
#         return json.dumps({'return_url' : request.form['url'], 'return_query' : resdict[identifier]})
#     return json.dumps({'error' : 'Query is missing or URL fetch failed'})

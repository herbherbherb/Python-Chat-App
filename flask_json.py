# import requests
import json
# from flask import request, Flask,render_template,json
# from html.parser import HTMLParser
import webmatch
from ParseJsonQuery import ParseJsonQuery
from collections import defaultdict 


def query_filter(res=None, query = None):
    newres = {}
    for allnode in res:
        idnum = str(allnode['id'])
        newres[idnum] = allnode
    res = newres
    pq = ParseJsonQuery(query)

    fieldlist = pq.parsedquery['extract.fields']
    resdict = {}
    reslist = []
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
        if "beginsWith" not in requirements:
            requirements['beginsWith'] = ''
        if "strContains" not in requirements:
            requirements['strContains'] = ''
        if "strRegex" not in requirements:
            requirements['strRegex'] = ''
        
        if "align" not in requirements:
            requirements['align'] = ''


        matched_nodes = webmatch.match(res,tagname,font_color=requirements['fontColor'],\
                                      font_size=requirements['fontSize'],min_length = requirements['minTextLength'],\
                                      max_length = requirements['maxTextLength'],class_name=requirements['className'], \
                                      ext_type = requirements['type'], text_begins = requirements['beginsWith'], \
                                      text_contains = requirements['strContains'], regex_string = requirements['strRegex'],\
                                      image_minht = requirements['imgminHeight'],image_minwd = requirements['imgminWidth'],\
                                      image_maxht = requirements['imgmaxHeight'], image_maxwd = requirements['imgmaxWidth'], \
                                      image_minx = requirements['imgminXLoc'],image_miny = requirements['imgminYLoc'],\
                                      image_maxx = requirements['imgmaxXLoc'], image_maxy = requirements['imgmaxYLoc'],\
                                      align = requirements['align'])



        resdict[identifier] = matched_nodes


    # records = []
    # for each_field in fieldlist:
    #     identifier = each_field['Field_id']
    #     subres = resdict[identifier]
    #     if len(reslist) == 0: 
    #         itemlist = []
    #         for item in subres: 
    #             itemlist.append(item)
    #             record = {}
    #             record[identifier] = item
    #             records.append(record)
    #         reslist.append(itemlist)
    #         #print(reslist)
    #     else: 
    #         newlist = []
    #         # for item in reslist[0]: 
    #         for k in range(len(reslist[0])): 
    #             item = str(reslist[0][k])
    #             for newitem in subres:
    #                 temp_item = str(item)
    #                 temp_new = str(newitem) 
    #                 itemparent = []
    #                 newparent = []
    #                 for i in range(5): 
    #                     #print(res[temp_item])
    #                     if  'parent' in res[temp_item] and int(res[temp_item]['parent']) >= 0: 
    #                         itemparent.append(res[temp_item]['parent'])
    #                         temp_item = str(res[temp_item]['parent'])
    #                     if 'parent' in res[temp_new] and int(res[temp_new]['parent']) >= 0: 
    #                         newparent.append(res[temp_new]['parent'])
    #                         temp_new = str(res[temp_new]['parent'])
    #                 lca = 9999
    #                 for i in range(len(itemparent)): 
    #                     for j in range(len(newparent)): 
    #                         if itemparent[i] == newparent[j]: 
    #                             lca = min(i, j)
    #                             break
    #                     if lca < 9999: 
    #                         break
    #                 if lca < 4: 
    #                     newlist.append(newitem)
    #                     records[k][identifier] = newitem
    #         if len(newlist) > 0: 
    #             #print(newlist)
    #             reslist.append(newlist)
    # """
# definition of formats: 
# records = [ {'title': xxx, 'price': yyy, 'record': zzz}, {'title': aaa, 'price': bbb, 'record':'ccc'} ]
# final_ans = {'title': [xxx, aaa], 'price':[yyy, bbb], 'record':[zzz, ccc]}
# reslist = [[xxx, aaa], [yyy, bbb]]
# """
    records = []
    final_ans = {}
    for each_field in fieldlist:
        identifier = each_field['Field_id']
        subres = resdict[identifier]
        # both reslist and records is empty
        if len(reslist) == 0: 
            itemlist = []
            for item in subres: 
                itemlist.append(item)
                record = {}
                record[identifier] = item
                records.append(record)
            reslist.append(itemlist)
            final_ans[identifier] = itemlist
        # 2nd field of a record, container not found yet
        elif 'record' not in final_ans: 
            newlist = []
            containers = []
            # for item in reslist[0]: 
            for k in range(len(reslist[0])): 
                item = str(reslist[0][k])
                for newitem in subres:
                    temp_item = str(item)
                    temp_new = str(newitem) 
                    itemparent = []
                    newparent = []
                    for i in range(5): 
                        if  'parent' in res[temp_item] and int(res[temp_item]['parent']) >= 0: 
                            itemparent.append(res[temp_item]['parent'])
                            temp_item = str(res[temp_item]['parent'])
                        if 'parent' in res[temp_new] and int(res[temp_new]['parent']) >= 0: 
                            newparent.append(res[temp_new]['parent'])
                            temp_new = str(res[temp_new]['parent'])
                    lca = 9999
                    for i in range(len(itemparent)): 
                        for j in range(len(newparent)): 
                            if itemparent[i] == newparent[j]: 
                                lca = min(i, j)
                                container = itemparent[i]
                                break
                        if lca < 9999: 
                            break
                    if lca < 4: 
                        newlist.append(newitem)
                        records[k][identifier] = newitem
                        records[k]['record'] = container
                        containers.append(container)
            if len(newlist) > 0: 
                reslist.append(newlist)
                final_ans['record'] = containers
                final_ans[identifier] = newlist   
        else: 
            newlist = []
            for record in records: 
                for k in range(len(subres)): 
                    item = subres[k]
                    temp_item = item 
                    for i in range(4): 
                        if 'parent' in res[str(temp_item)] and int(res[str(temp_item)]['parent']) >= 0: 
                            if int(res[str(temp_item)]['parent']) == record['record']: 
                                record[identifier] = item
                                newlist.append(item)
                                print(k)
                                break
                            else: 
                                temp_item = str(res[str(temp_item)]['parent'])
                    if identifier in record: 
                        break
            if len(newlist) > 0: 
                final_ans[identifier] =  newlist
                reslist.append(newlist)

    final_ans = defaultdict(list)

    for rec in records:
    	for key,val in rec.items():
    		final_ans[key].append(val)








    if query:
       
        # return json.dumps({'return_query' : resdict[identifier]})
        return json.dumps(final_ans)

    return json.dumps({'error' : 'Query is missing or URL fetch failed'})



# @app.route('/GetandParse', methods=['POST'])
# def GetandParse():
#     serialized_nodes = test();
#     query = request.form['query']
#     fid = request.form['fieldid']
#     matchitem = request.form['match']
#     query = "{\"extract\":{\"fields\":[{" + "\"Field_id\":" +    fid     +    ",\"match\":" + ""    +        matchitem        +      ""  + "}]} }"

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
if __name__ == '__main__':
    query = """ {
    "extract" : {

        "fields": [

            {
                "Field_id": "AA",
                "match" : {
                "type" : "text",
                "TextLength" : {"lt":100,"gt":80},               
                "tagName"   : "H2"
                }
            },

            {
                "Field_id": "BB",
                "match" : {
                "type" : "text",
                "TextLength" : {"lt":20, "gt":2},               
                "tagName" : "SPAN"
                }
            },

            {
                "Field_id": "CC",
                "match" : {
                "type" : "text",
                "TextLength" : {"lt":250,"gt":50},                
                "tagName"   : "H2"
                }
            },

            {
                "Field_id": "DD",
                "match" : {
                "type" : "text",
                "TextLength" : {"lt":250,"gt":50},                
                "tagName"   : "H3"
                }
            }




    ]
   },

  "from" :  {
    "url" : "https://www.amazon.com/s/ref=nb_sb_noss/138-7753184-2542555?url=search-alias%3Delectronics&field-keywords=computer&rh=n%3A172282%2Ck%3Acomputer"

    }

}
"""

    a = [{'id':1,'height':200,'text':'sss','tag':'ss'},{'id':3, 'height':200,'text':'sss','tag':'ss'},{'id':4, 'height':200,'text':'sss','tag':'ss'},{'id':4, 'height':200,'text':'sss','tag':'ss'}]

    print(query_filter(a , query))
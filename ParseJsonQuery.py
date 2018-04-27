import json,sys,csv

''' Query Parser: The stored queery is in self.parsedquery.

    The helperquery function has details on how to access the stored qery object'''

class ParseJsonQuery:

    def __init__(self,jsonstring):
        #Input json query from front-end as string
        self.inpjson = jsonstring
        #Dictionary object containing parsed query
        self.parsedquery = None
        #self.jsonformat = json.loads(self.inpjson)
        self.ParseInpString()

    def ParseInpString(self):
        json_data = json.loads(self.inpjson)
        #Flatten nested Json with "." as separator
        self.parsedquery =  self.FlattenJson(json_data,".")

    #To flatten a nested json
    def FlattenJson(self,b,delim):
        val = {}
        for i in b.keys():
            if isinstance( b[i], dict ):
                get = self.FlattenJson( b[i], delim )
                for j in get.keys():
                    val[ i + delim + j ] = get[j]
            else:
                val[i] = b[i]

        return val

    
    def helperquery(self):

         fieldlist = self.parsedquery['extract.fields']
         url = self.parsedquery['from.url']

         #This is the number of things to extract. For example, if we have to extract title and price of laptops, this number wil be 2
         num_fields = len(fieldlist)

         for each_field in fieldlist:
              #Unique identifer for every
              identifier = each_field['Field_id']
              #Match params is a dictionary. Key is primitives and value is user-specified value, For example minLength is key with value as 80 from Query1
              matchparams = each_field['match']
              for key, val in matchparams.items():
                print(key)
                print(val)




if __name__ == "__main__":

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

    pq = ParseJsonQuery(query)
    pq.ParseInpString()
    #pq.helperquery()

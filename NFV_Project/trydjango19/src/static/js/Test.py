# import urllib2
# import json
#
#
#  locu_api = '912745008ba80f5788732481d15de1837db98eb7'
#  api_key=locu_api
#  url='https://api.locu.com/v1_0/venue/search/?locality=Newport%20beach&api_key=912745008ba80f5788732481d15de1837db98eb7'
#  json_obj=urllib2.urlopen(url)
# data=json.load(json_obj)
# for item in data['objects']:
#     print item['name'], item['phone']


import urllib2
import json
import requests

locu_api='912745008ba80f5788732481d15de1837db98eb7'
api_key=locu_api
url='https://api.locu.com/v1_0/venue/search/?locality=Newport%20beach&api_key=912745008ba80f5788732481d15de1837db98eb7'
json_obj=requests.get(url)
if json_obj.status_code!=200:
    print ('API Error')
for item in json_obj.json():
    print item['name'], item['phone']

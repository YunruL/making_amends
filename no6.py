#-*-coding:utf-8-*-
import urllib
import urllib2
import json
import random
import datetime
import csv
import matplotlib.pyplot as plt 

apikey = '63920c745058a71d5083ad7fa5b6d141b512262b'
venue = 'HHLEX'
stock = 'ELCY'
base_url = 'https://api.stockfighter.io/ob/api'

account = 'CES87121129'
timeouts = 5
accountslist = set()
pricelist = []
idlist = []
maxprice = 0
maxid = 0
minprice = 100000
minid = 0
accountscount = {}
impocount = {}

for times in range(1,5):
	print times
	idlist = []
	for i in range(1,30):
	  try:
		arand = random.randint(1,5)
		order = {"account": account,"qty": arand,"direction": "buy", "orderType": "market"}
		order_data = json.dumps(order)
		requrl = base_url+'/venues/'+venue+'/stocks/'+stock+"/orders"
		req = urllib2.Request(url = requrl, data = order_data, headers =  {'X-Starfighter-Authorization' : apikey})
		res3_data = urllib2.urlopen(req,timeout = timeouts)
		res3 = json.loads(res3_data.read())
		idlist.append(res3['id'])
	  except Exception, e:
	  	print e
	 
	for j in idlist:
	 try:
	 	print j
		requrl = base_url+'/venues/'+venue+'/stocks/'+stock+"/orders/"+str(j)
		req = urllib2.Request(url = requrl, headers =  {'X-Starfighter-Authorization' : apikey})
		res_data = urllib2.urlopen(req,timeout = timeouts)
		res = json.loads(res_data.read())
		if res['totalFilled']>0:
			theprice  = res['fills'][0]['price']
			if theprice>maxprice:
				maxprice = theprice
				maxid = j
			if theprice<minprice:
				minprice = theprice
				minid = j
			#pricelist.append(res['fills'][0]['price'])

	 except Exception, e:
	  	print e
	if minid == idlist[0] or minid == idlist[-1] or maxid == idlist[0] or maxid == idlist [-1] :
		continue

	for j in [minid, maxid]:
		getaccount = set()
		print j
		for c in range(1,20):
			try:
				aid = j-c
				data = {'account':account}
				order_data = json.dumps(data)
				requrl = base_url+'/venues/'+venue+'/stocks/'+stock+'/orders/'+str(aid)+'/cancel'
				req = urllib2.Request(url = requrl, data = order_data, headers =  {'X-Starfighter-Authorization' : apikey})
				#req = urllib2.Request(url = requrl)
				res_data = urllib2.urlopen(req, timeout = timeouts)
				res = json.loads(res_data.read())
				print res
			except urllib2.HTTPError, a:
				erdata = json.loads(a.read())
				if a.code == 401:
					newaccount = erdata['error'][-11:-1]
					accountscount.setdefault(newaccount, 0)
					accountscount[newaccount] = accountscount[newaccount]+1
					impocount.setdefault(newaccount, 0)
					impocount[newaccount] = impocount[newaccount]+1
			except Exception, e:
				print e
			

		for c in range(1,20):
			try:
				aid = j+500+c
				data = {'account':account}
				order_data = json.dumps(data)
				requrl = base_url+'/venues/'+venue+'/stocks/'+stock+'/orders/'+str(aid)+'/cancel'
				req = urllib2.Request(url = requrl, data = order_data, headers =  {'X-Starfighter-Authorization' : apikey})
				#req = urllib2.Request(url = requrl)
				res_data = urllib2.urlopen(req, timeout = timeouts)
				res = json.loads(res_data.read())
				print res
			except urllib2.HTTPError, a:
				erdata = json.loads(a.read())
				if a.code == 401:
					newaccount = erdata['error'][-11:-1]
					getaccount.add(newaccount)
					accountscount.setdefault(newaccount, 0)
					accountscount[newaccount] = accountscount[newaccount]+1
			except Exception, e:
				print e
	print accountscount
	print impocount
			
#print accountscount
#print impocount

candidate = ''
cancount = 0.0
for x in impocount:
	now = float(impocount[x])/float(accountscount[x])
	if now > cancount: 
		cancount = now
		candidate = x
print candidate
print cancount
# wfile = open('orders.csv','wb')
# writer = csv.writer(wfile)
# for s in accountslist:
# 	requrl = base_url+'/venues/'+venue+'/accounts/'+s+'/stocks/'+stock+'/orders'
# 	#req = urllib2.Request(url = requrl, headers =  {'X-Starfighter-Authorization' : apikey})
# 	req = urllib2.Request(url = requrl)
# 	res_data = urllib2.urlopen(req)
# 	res = json.loads(res_data.read())
# 	print res
# 	for i in res['orders']:
# 		line = [i['id'],i['direction'], i['originalQty'],i['qty'],i['price'],i['orderType'],i['account'],i['ts'],i['totalFilled'],i['open']]
# 		print line
# 		writer.writerow(line)

# wfile.close()
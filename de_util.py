import urllib2
import constants
import re
import sublime

def returnErrorArray(caption, text):
	errorCaption = padSpace(caption, 4)
	errorText = padSpace(text, 12) 
	return [errorCaption, errorText]

def padSpace(value, spaces):
	addedSpace = ""
	for i in xrange(spaces):
		addedSpace += " "
	
	return addedSpace + value

def buildServerPath(filePath):
	absolutePath = ""

	relativePath = re.search("websites(.+)", filePath)

	if relativePath:
		absolutePath = "/var/" + relativePath.group()

	return absolutePath

def buidlUrl(url, queryString):
	return url + "?" + queryString

def alert(message):
	sublime.message_dialog(message)

def log(message):
	print message

def error(message):
	sublime.error_message(message)

def httpGet(data, headers):
	result = ""

	try:
		proxy_support = urllib2.ProxyHandler({})
		opener = urllib2.build_opener(proxy_support)
		urllib2.install_opener(opener)

		http_handler = urllib2.HTTPHandler()
		opener = urllib2.build_opener(http_handler)
		
		request = urllib2.Request(url=buidlUrl(constants.LOCALHOST_VARSCOPER_URL, data)
			,headers=headers)
		response = urllib2.urlopen(request, "3")

		result = response.read()
	except urllib2.HTTPError as e:
		log("HTTPError: " + str(e.code))
	except urllib2.URLError as e:
		log("URLError: " + str(e.reason))

	return result

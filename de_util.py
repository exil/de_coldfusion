import urllib2
import constants
import re
import sublime

def getResultObject():
	result = {}
	result["errors"] = []
	result["regions"] = []

	return result

def mergeResults(result1, result2):
	result1["errors"].extend(result2["errors"])
	result1["regions"].extend(result2["regions"])

	return result1

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
	sublime.message_dialog(constants.DE_LINTER + " :: " + message)

def log(message):
	print (constants.DE_LINTER + " :: " + message)

def error(message):
	sublime.error_message(constants.DE_LINTER + " :: " + message)

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

		response = urllib2.urlopen(request, "1")

		result = response.read()
	except urllib2.HTTPError as e:
		log("HTTPError: " + str(e.code))
	except urllib2.URLError as e:
		log("URLError: " + str(e.reason))

	return result

def getSettings(setting):
	settings = sublime.load_settings(constants.DE_LINTER_SETTINGS).get(setting)

	return settings
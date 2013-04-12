import re
import sublime

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
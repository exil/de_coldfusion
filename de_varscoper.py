import constants
import urllib
import de_util
from xml.dom import minidom
from de_base import LinterBase

class DeVarscoper():
	def getResult(self, view):
		self.baseLinter = LinterBase(view)

		errorResult = None
		absolutePath = de_util.buildServerPath(view.file_name())

		if (absolutePath is None) or (absolutePath == ""):
			de_util.log("Could not locate file in ~/var/websites/")

		else:
			try:
				data = urllib.urlencode({
					"filePath" : absolutePath
					,"displayFormat" : "xml"
					,"recursiveDirectory" : "true"
					,"parseCFScript" : "disabled"
				})

				headers = {
					"Content-Type" : "text/xml"
		    		,"Content-Length": len(data)
				}

				xmlResult = de_util.httpGet(data=data, headers=headers)
			except Exception as e:
				de_util.log("Error getting http response : " + str(e))
			else:
				try:
					result = self.parseXmlResult(xmlResult)

					if result["errors"]:
						errorResult = result
				
				except Exception as e:
					de_util.log(str(e))

		return errorResult

	def parseXmlResult(self, xmlResult):
		result = de_util.getResultObject()

		try:
			xmlDoc = minidom.parseString(xmlResult)

			functionNodes =xmlDoc.getElementsByTagName("function")

			for fNode in functionNodes:
				fName = fNode.getAttribute("name")
				fDetail = fNode.firstChild

				fVariable = fDetail.getElementsByTagName("type")[0].firstChild.nodeValue
				fLineNumber = fDetail.getElementsByTagName("line_number")[0].firstChild.nodeValue
				
				errorText = "Function [ %s ] :: Variable [ %s ] " % (fName, fVariable)
				errorCaption = "Varscoper :: %s " % (fLineNumber)

				result["errors"].append(de_util.returnErrorArray(errorCaption, errorText))
				result["regions"].append(self.baseLinter.getRegion(fLineNumber))

		except Exception as e:
			de_util.log("Error parsing xml results :: " + str(e))

		return result
	




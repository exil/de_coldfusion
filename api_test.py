import urllib  
import urllib2  
import threading  

class ApiCall(threading.Thread):  
    def __init__(self, absolutePath, timeout):  
        self.absolutePath = absolutePath  
        self.timeout = timeout  
        self.result = None  
        threading.Thread.__init__(self)  
  
    def run(self):  
        try:  
            data = urllib.urlencode({"filePath" : self.absolutePath})  
            request = urllib2.Request(url='http:http://core.local.discoveryeducation.com/varscoper/index.cfm'
                ,data=data
                ,headers=({"Content-Type" : "application/xml"}))
            
            response = urllib2.urlopen(request, timeout=self.timeout)  
            self.result = response.read() 

            print self.result 
            return  
  
        except (urllib2.HTTPError) as (e):  
            err = '%s: HTTP error %s contacting API' % (__name__, str(e.code))  
        except (urllib2.URLError) as (e):  
            err = '%s: URL error %s contacting API' % (__name__, str(e.reason))  
            
        # sublime.error_message(err)
        self.result = False 


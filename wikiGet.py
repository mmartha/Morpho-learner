#import relevant modules
import urllib2
from urllib2 import urlopen
import cookielib
from cookielib import CookieJar
import re


# Build opener and change header so we don't look like a bot
cj = CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
opener.addheaders = [('User-agent','Mozilla5.0')]

def getContent(url):
	sourceCode = opener.open(url).read()
	# Select everything marked as paragraph text
	pattern = re.compile(r'<p>(.*)</p>')
	# findall returns a list, select first element which is a string
	content = " ".join(re.findall(pattern, sourceCode))
	return content
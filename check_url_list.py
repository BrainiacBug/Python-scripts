#!/usr/bin/env python

import urllib2
from urllib2 import URLError

url_list = open("url_list.txt", "r")
output= []

def print_error_pages(list):
    """Outputs all urls that gives back some kind of error"""
    print "__________ URLs Errors __________"
    for item in list:
        if item[3]:
            print "Url: " +  item[0] + " Error: " + item[3]
    print "_________________________________\n"

def print_short_message_pages(list):
    """Outputs all urls that contains only short words in page. e.g it works!"""
    print "__________ URLs short message __________"
    for item in list:
        if item[2]:
            print "Url: " +  item[0] + " message: " + item[2].replace("\n", "")
    print "_________________________________\n"

def print_redirected_pages(list):
    """Outputs all urls that change after opening page"""
    print "__________ URLs redirected __________"
    for item in list:
        if not item[1] == item[0] and item[1]:
            print "Url: " +  item[0] + " new url: " + item[1]
    print "_________________________________\n"

def print_normal_pages(list):
    """Outputs all urls that didn't change after opening page"""
    print "__________ Normal URLs  __________"
    for item in list:
        if item[0] == item[1]:
            print "Url: " +  item[0] 
    print "_________________________________\n"

for line in url_list:
        url_page = line.replace("\n", "")
        url_prefix = "http://"
        if not url_prefix in url_page:
            url_page = url_prefix + url_page
        try: 
            response = urllib2.urlopen(url_page)
            error_code = ""
            real_url = response.geturl()
            data = response.read()
        except URLError, e:
            error_code = e.reason
            real_url = ""
        if len(data) < 25 and len(data) > 1:
            data = data
        else:
            data = ""
        output.append((url_page, real_url, data, error_code))

# Close file and urllib
response.close()
url_list.close()

# Print output
print_error_pages(output)
print_short_message_pages(output)
print_redirected_pages(output)
print_normal_pages(output)

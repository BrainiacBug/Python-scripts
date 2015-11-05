# -*- coding: utf-8 -*-
import re
import urllib
import urllib2
import argparse
from time import sleep
from bs4 import BeautifulSoup


parser = argparse.ArgumentParser(description='Find all links from google search.')
parser.add_argument('-q', '--query', help='Query to find from google search.', required=True)
parser.add_argument('-r', '--results', default=25, help='Results on one page.', required=False)
parser.add_argument('-d', '--delay', default=2, help='Delay for every new page.', required=False)
args = parser.parse_args()

links = []
#Settings
delay = args.delay
linksCountOnPage = args.results


def make_google_query(query, dislaySize=linksCountOnPage, startNumb=0):
    address = "http://www.google.com/search?q=%s&num=%s&hl=en&start=%s" % (urllib.quote_plus(query), str(dislaySize), str(startNumb))
    request = urllib2.Request(address, None, {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.124 Safari/537.36'})
    urlfile = urllib2.urlopen(request)
    page = urlfile.read()
    soup = BeautifulSoup(page)
    return soup


def find_links(soup):
    for li in soup.findAll('li', attrs={'class': 'g'}):
        sLink = li.find('a')
        links.append(sLink['href'])
    return links


def find_results_count(soup):
    stats = soup.findAll('div', attrs={'id': 'resultStats'})
    raw = str(stats[0].get_text())
    regex = re.compile('About ([0-9]+) results')
    result = regex.match(raw)
    return result.group(1)


def get_all_pages_links(query):
    links_count = linksCountOnPage
    g_page = make_google_query(query)
    total_results = find_results_count(g_page)
    while (int(total_results) > int(links_count)):
        sleep(delay)
        next_page = make_google_query(query, startNumb=links_count)
        find_links(next_page)
        links_count += linksCountOnPage
        if (int(total_results) < int(links_count)):
            print "All done! Got %s Links!" % (len(links))
            break
    return links


def write_in_to_file(content):
    txtfile = open('google_links_output.txt', 'a+')
    for line in content:
        txtfile.write(line + '\n')
    file.close
    print "All links in file!"

if __name__ == '__main__':
    write_in_to_file(get_all_pages_links(args.query))

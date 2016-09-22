import re
import os
import urllib
from bs4 import BeautifulSoup


sites = []
sorted_sites = []


# Neti.ee
def get_top_links_from_neti():
    """Finds all top100 links from neti.ee page"""
    page = urllib.urlopen("http://www.neti.ee/info/top100.html")
    page_src = page.read()
    soup = BeautifulSoup(page_src,  'html.parser')
    print "[..] Opened Neti.ee webpage."
    main_list = soup.find('ul', attrs={'class': 'top-100'})
    for item in main_list.findAll('a'):
        item_link = item.get('href')
        print "[*] Found link: " + item_link
        sites.append(item_link)
    print "[..] All links found in Neti.ee!"


# Metrix top 120
def get_metrix_top_page(page):
    """Opens metrix top page
    :param page: top page number (int)"""
    page = urllib.urlopen("http://metrix.ee/?page=" + str(page - 1))
    page_src = page.read()
    soup = BeautifulSoup(page_src,  'html.parser')
    print "[..] Opened metrix.ee webpage."
    return soup


def get_top_links_from_metrix(page_nr):
    """Finds all top links from metrix page
    :param page_nr: top list page number (int)"""
    soup = get_metrix_top_page(page_nr)
    for list_elm in soup.findAll('td'):
        for item in list_elm.findAll('a'):
            item_link = item.get('href')
            item_title = item.get('title')
            if len(item_title) > 1:
                main_link = item_title
            else:
                link_a = item_link.split('/')
                main_link = link_a[3].replace('-', '.')
            if "http" not in main_link:
                main_link = "http://" + main_link
            else:
                main_link = main_link
            print "[*] Found link: " + main_link
            try:
                main_link.decode('ascii')
                sites.append(main_link)
            except UnicodeEncodeError:
                print "[!]Found unicode inside url!"
    print "[..] All links found in page " + str(page_nr) + "!"


def get_all_metrix_pages():
    """Gets all 3 matrix pages for top 120"""
    get_top_links_from_metrix(page_nr=1)
    get_top_links_from_metrix(page_nr=2)
    get_top_links_from_metrix(page_nr=3)


def clear_sites_url():
    """Clears all urls from file to unique list"""
    for site in sites:
        regex = "((http|https):\/{2})([\da-z-]+)\.?([\da-z-]+)\.([\da-z-]+)\.?([\da-z-]+)"
        re_match = re.match(regex, site.lower())
        try:
            clean_url = re_match.group()
            if clean_url not in sorted_sites:
                sorted_sites.append(clean_url)
            else:
                print "[!] Site already in sorted sites list! " + clean_url
        except AttributeError:
            print "[!] No match from regex: " + site


def get_robot_txt_file_from_site():
    """Downloads given site robot.txt file"""
    for item in sorted_sites:
        # Make file name from url
        item_name = item.split('//')
        site_name = item_name[1].replace('.', '_')
        robot_url = item + "/robots.txt"
        # Read from webpage and write to file
        try:
            site = urllib.urlopen(robot_url)
            write_to_file(site_name + ".txt", site.read())
        except IOError:
            print "[!] IOerror in opening site: " + item


def make_folder_for_files():
    """Makes folder robots if needed and change path"""
    text_dir = "robots"
    if not os.path.exists(text_dir):
        os.makedirs(text_dir)
        print "[..] Created folder: " + text_dir
    os.chdir(os.curdir + "/robots")


def write_to_file(file_name, file_data):
    """Write data to file.
     :param file_name: file name (str),
     :param file_data: data (str)"""
    robot_file = open(file_name, "w+")
    robot_file.write(file_data)
    robot_file.close()
    print "[*] File created: " + file_name


if __name__ == '__main__':
    print"-------------------------------------------------"
    print"-   ROBOT.TXT FINDER FOR TOP ESTONIAN WEBPAGES  -"
    print"-------------------------------------------------"
    print"- Finds top webpages from neti.ee and metrix.ee -"
    print"-------------------------------------------------"
    get_top_links_from_neti()
    get_all_metrix_pages()
    clear_sites_url()
    make_folder_for_files()
    get_robot_txt_file_from_site()
    print "[..] Total sites in list :" + str(len(sites))
    print "[..] Total sorted sites :" + str(len(sorted_sites))

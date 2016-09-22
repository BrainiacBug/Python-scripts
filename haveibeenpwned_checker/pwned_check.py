from argparse import ArgumentParser
import json
import urllib2
import sys
from time import sleep

API_URL = "https://haveibeenpwned.com/api/v2/breachedaccount/%s"
UA = {"User-Agent": "pwnd_email_list_Test"}


def get_args():
    parser = ArgumentParser()
    parser.add_argument('-i', dest='input_file',   help='Path to text file that lists email addresses.')
    parser.add_argument('-o', dest='output_file',  help='Path to output text file.')
    parser.add_argument('-p', dest='pwned_emails', action='store_true', help='Print only the pwned email addresses.')
    parser.add_argument('-s', dest="single_email", help='Send query for just one email address.')

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    return parser.parse_args()


def make_request(email_list):
    req_results = []

    print "[!] Sending requests. Total requests: %s" % len(email_list)

    for email in email_list:
        data = []
        req = urllib2.Request(API_URL % email, headers=UA)

        try:
            response = urllib2.urlopen(req)
            data = json.loads(response.read())
            breach_data = parse_data(data)
            req_results.append((email, True, breach_data))

        except urllib2.HTTPError as error:
            if error.code == 400:
                print "%s does not appear to be a valid email address.  HTTP Error 400." % email
            if error.code == 403:
                print "Forbidden - no user agent has been specified in the request.  HTTP Error 403."
            if error.code == 404:
                req_results.append((email, False, data))
            if error.code == 429:
                print "Too many requests; going over the request rate limit.  HTTP Error 429."

        sleep(2)
    return req_results


def parse_data(data):
    breaches = ""
    for breach in data:
        breach_string = "[-] Breach: " + breach["Title"] + "/ Domain: " + breach["Domain"] + "/ Date: " + breach["BreachDate"] + "/ Leaked info: "
        for data_class in breach["DataClasses"]:
            breach_string += data_class + " "
        breaches += breach_string + " \n"
    return breaches


def write_to_file(filename, data, pwnd):
    output = open(filename, 'w')
    for entry in data:
        data_text = ""
        if pwnd:
            if entry[1]:
                data_text = "[>>]" + str(entry[0]) + "\n" + str(entry[2])
        else:
            data_text = "[>>]" + str(entry[0]) + "\n" + str(entry[2])
        output.write(str(data_text))
    output.close()
    print "[*] Created file %s with results!" % filename


def main():
    opts = get_args()

    if opts.single_email:
        email_list = [opts.single_email.strip()]
    else:
        email_list_file = open(opts.input_file, 'r')
        email_list = [line.strip() for line in email_list_file]
        email_list_file.close()

    results = make_request(email_list)
    if opts.output_file:
        write_to_file(opts.output_file, results, opts.pwned_emails)
    else:
        for result in results:
            if opts.pwned_emails:
                if result[1]:
                    print "[>>]" + result[0]
                    print result[2]
            else:
                print "[>>]" + result[0]
                print result[2]


if __name__ == '__main__':
    main()

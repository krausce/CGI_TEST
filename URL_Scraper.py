import os
from datetime import datetime as dt
import time
import re
from signal import signal, SIGINT
import sys
from concurrent.futures import ThreadPoolExecutor
import urllib.request as request
import yaml


class URL_Scraper():

    '''
        URL_Scraper does as the name implies. Accepts .yaml file as an argument. To call this script from the command line,
        enter: "python URL_Scraper.py <file_name>.yaml" where "file_name" is any arbitrary name you may have entered for
        the argument configuration file.

        .yaml file should be configured as such:

                Regex_List:
                - (http|ftp|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?
                URLs:
                - sites.google.com
                - en.wikipedia.org
    '''

    def __init__(self, URL_file, URL_key, regex_key, out_file='SCRAPE_LOG.txt'):
        '''
            @param arg_file .yaml to retrieve args from
            @param regex_key Key to retrieve REGEXs from arg_input file
            @param URL_key Key to retrieve URLs from arg_input file
        '''
        self.out_file = out_file
        self.regex_key = regex_key
        self.URL_key = URL_key
        self.URL_file = URL_file
        self.get_params()
        self.format_URL()
        self.scrape_data()

    def format_URL(self):
        for i in range(len(self.URL_list)):
            url = self.URL_list[i]
            if not(url.__contains__('http')):
                if not(url.__contains__('www.')):
                    url = 'https://www.' + url

                else:
                    url = 'https://' + url
            self.URL_list[i] = url

    def get_params(self):
        '''
            Opens the source file and retrieves the regular expression and url lists. If the source file is a .txt
            instead of a .yaml file, then the params are extracted.
        '''

        try:
            # Check file type before proceeding
            if self.URL_file.__contains__('.yaml'):
                with open(self.URL_file) as arg_file:
                    temp = yaml.load(arg_file, Loader=yaml.FullLoader)
                    self.regex_list = temp.get(self.regex_key)
                    self.URL_list = temp.get(self.URL_key)

            elif self.URL_file.__contains__('.txt'):
                regex_extract = r"\'.+\'"
                url_extract = r'(http|ftp|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?'
                regex_list = [regex_extract, url_extract]
                self.extract_params(regex_list)

            else:
                raise TypeError()

        except FileNotFoundError:
            self.URL_file = input(
                'File not found, please enter a different file or path.')
            self.get_params()

        except TypeError:
            self.URL_file = input(
                'File type is not .txt nor .yaml. Enter a different file or terminate the program with Ctrl-C: ')

    def extract_params(self, regex_list):
        '''
           Stores the regex and URL lists as class instance variables.
        '''
        try:
            # Initialize class instance vars.
            self.url_list = []
            self.regex_list = []
            # Check if file is empty
            if os.stat(self.URL_file).st_size == 0:
                raise ValueError()
            with open(self.URL_file) as file:

                for line in file:
                    if re.search(regex_list[0], line):
                        self.regex_list.append(line.rstrip())
                    if re.search(regex_list[1], line):
                        self.url_list.append(line.rstrip())

        except FileNotFoundError:
            self.url_source = input(
                'File not found. Enter a different file or terminate the program with Ctrl-C: ')
            return self.get_params()

        except ValueError:
            self.url_source = input(
                'The provided input file is empty. Enter a different file or terminate the program with Ctrl-C: ')

    def extract_text(self, url):

        with open(self.out_file, 'a') as out_file:
  
            for r in self.regex_list:
                try:
                    current_time = dt.now().strftime("Date: %d-%m-%Y Time: %I:%M:%S:%f_%p")
                    start = time.perf_counter()
                    req = request.Request(url)
                    response = request.urlopen(req)
                    raw_text = response.read()
                    response_time = '%0.2f s' % (time.perf_counter() - start)
                    scraped_data = re.findall(r, str(raw_text))
                    if not (len(scraped_data) > 0):
                        print(
                            current_time + '| Response Time: {} | No data scraped using regex: {}'.format(
                                response_time, r), file=out_file)
                    else:
                        print(current_time + '| Response Time: {} | URL: {} | Regex: {}\nData Scraped: {}\n'.format(
                            response_time, url, r, scraped_data), file=out_file)
                except:
                    print('\n' + current_time +
                            "| URL: {1} | {0}\n".format(sys.exc_info()[0], url), file=out_file)
                    continue

    def scrape_data(self, start_time=time.perf_counter()):

        print('Beginning data scraping.')       

        with ThreadPoolExecutor(max_workers=20) as executor:
            executor.map(self.extract_text, self.URL_list)

        with open(self.out_file, 'a') as out_file:
            iteration_time = '%0.2f s' % (time.perf_counter() - start_time)
            print('Total run time for this iteration: {}\n'.format(iteration_time), file=out_file)

        


iter_count = {'iter_count': 1}


def main(iter_count=iter_count):
    URL_file = sys.argv[1]
    URL_key = 'URLs'
    regex_key = 'Regex_List'
    URL_Scraper(URL_file, URL_key, regex_key)
    print('Round {} complete.'.format(iter_count['iter_count']))
    iter_count['iter_count'] += 1


def handler(signal_received, frame):
    print('Program successfully terminated after %d iterations. Exiting gracefully.' %
          iter_count['iter_count'])
    sys.exit(0)


if __name__ == '__main__':
    # Tell Python to run the handler() function when SIGINT is recieved
    signal(SIGINT, handler)
    print('Running. Press CTRL-C to exit.')
    # Pings the arguments from the input file every 15 seconds until the program is terminated
    while True:
        main()
        time.sleep(15)

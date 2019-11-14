<h1><center> CGI Web Scraping With Regex </center></h1>

## Problem Statement ##

Develop a Python3 script which accepts configured lists of urls and regular expressions as arguments. For each url, it must be possible to determine which regular expression(s) were able to match content.

## Requirements ##

1. As a minimum, the results of all checks must be stored for later analysis; must contain the time of check, response time, and possible error if check was not successful.

2. The process must be able to run continuously doing the checks periodically, it must be able to deal with a large number of urls without exploding, it must always respond to user input (ctrl-c for example in case of CLI script) within one second and clean
up any resources gracefully on exit.

3. If you choose to make a GUI application use GTK or QT (Definitely not Tk).

4. You must document how to install and use your script and comment your code where you
see it being useful.

5. Script must work on Linux regardless of what OS was used for development.

6. Even if we use the word "script" it does not mean that the solution must be self-contained in one file.

7. This should be doable in a few hours ("One evening"), no need to get fancy: "Real developers ship".

8. All design decisions are yours to make, be prepared to explain why you made a particular choice.


## Sample Output ##

- Date: 14-11-2019 Time: 01:37:59:437300_AM| Response Time: 0.03 s | URL: https://www.sites.google.com | Regex:
- Date: 14-11-2019 Time: 01:38:00:053755_AM| URL: https://www.en.wikipedia.org | <class 'urllib.error.URLError'> (Error Logging)
- Date: 14-11-2019 Time: 01:38:00:059621_AM| Response Time: 0.03 s | URL: https://www.youtube.com | Regex:

## Tech Used ##
    Python 3
    Regular Expressions
    YAML Argument Config File
    [PEP8] Style

## Imported Libraries ##
    import os
    from datetime import datetime as dt
    import time
    import re
    from signal import signal, SIGINT
    import sys
    import urllib.request as request
    import yaml

**NOTE:** This script will run in the base Anaconda Environment with Python 3.

### Running Instructions ###

1. Make certain that this script is either run in the same working directory as the argument config file, or pass the appropriate complete file path *Only use ".yaml" files*.

##### Sample Argument Config File #####

    Regex_List:
    - (http|ftp|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?
  
    URLs:
    - sites.google.com
    - en.wikipedia.org
    - youtube.com
    - nordea.fi
    - cgi.fi

**NOTE:** Be sure to name the keys appropriately. (*Regex_List*, *URLs*)

1. The sample config file is **"URLs.yaml"**.

2. To run this script, simply open a command prompt from the folder where this script is stored on your machine and enter:
   
                            python URL_Scraper.py URLs.yaml

3. In the same working directory as this script, you will see a file named "**SCRAPE_LOG.txt**". This file contains the output of this script.
# CGI_TEST

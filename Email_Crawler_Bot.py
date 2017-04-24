# Programmed by Choyon Ahmed
# USAGE: python bot.py --pb --slx --debp --src --srx "something to search" 3 --proxy
# replace --n to skip a feature
# 3 represents number of pages to search
import urllib, httplib, urllib2, re, os, sys, ssl, socket
import time
from platform import system
from random import randint
socket.setdefaulttimeout(15)
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
opener = urllib2.build_opener(urllib2.HTTPSHandler(context=ctx))
opener.addheaders = [('User-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A')]
opener = urllib2.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A')]
headers={"User-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A"}
try:
    script, pbin, slx, debp, cus, srx, dork, pagedepth, prox = sys.argv
    #that damn blacklist will be created if not in there
    open('blacklist.txt', 'a+').close()
    open('sources.txt', 'a+').close()
    open('proxies.txt', 'a+').close()
    proxies = open('proxies.txt','r').read().split('\n')
    #Below function is created for extracting emails from specific url
    def getmails(link, proxy):
        #a'right. I gonna check if this link was already visited or not
        if link in open('blacklist.txt', 'r').read():
            return
        print 'Extracting emails from a webpage...\nSit tight ...'
        if 'https://' not in link:
            if 'http://' not in link:
                link = 'http://' + link
        link = link.replace('\n','')
        try:
            randomip = proxies[randint(0, len(proxies)-1)]
            if proxy == '--proxy':
                dataOfLink = urllib.urlopen(link, proxies={'http':randomip}).read()
            else:
                dataOfLink = urllib.urlopen(link).read()
            mailsfound = re.findall('[\w]+@[\w.]+', dataOfLink)
            for email in mailsfound:
                email = email.replace('\n', '')
                # below goes some banned keywords for email extraction
                # else garbage emails will be crawled
                if '.png' in email:
                    continue
                if '.gif' in email:
                    continue
                if '.jpg' in email:
                    continue
                if '._' in email:
                    continue
                if '@.' in email:
                    continue
                if '.' not in email:
                    continue
                try:
                    # below condition works to ensure unique emails
                    norepeat = open('collections.txt', 'r').read()
                    if email not in norepeat:
                        open('collections.txt', 'a+').write(email + ', ' + link + '\n')
                except IOError:
                    open('collections.txt', 'a+')
            # saving as blacklisted now
            open('blacklist.txt', 'a+').write(link + '\n') 
        except:
            pass

    #Below function is created for collecting pastebin recent pastes
    #WARNING: pastebin bans IP if much request is sent to their site
    #More info: https://pastebin.com/scraping
    def pastebin(prox):
        pburl = 'https://pastebin.com/archive'
        try:
            randomip = proxies[randint(0, len(proxies)-1)]
            if prox == '--proxy':
                getdata = urllib.urlopen(pburl, proxies={'http':randomip}).read()
            else:
                getdata = urllib.urlopen(pburl).read()
            pasteurl =  re.findall('class="i_p0" alt="" /><a href="(.*?)">', getdata)
            for link in pasteurl:
                link = 'https://pastebin.com/raw' + link
                getmails(link, prox)
                time.sleep(2)
        except IOError:
            pass
        except:
            pass

    #Below function is created for collecting slexy recent pastes
    def slexy(prox):
        pburl = 'http://slexy.org/recent'
        try:
            randomip = proxies[randint(0, len(proxies)-1)]
            if prox == '--proxy':
                getdata = urllib.urlopen(pburl, proxies={'http':randomip}).read()
            else:
                getdata = urllib.urlopen(pburl).read()
            pasteurl =  re.findall('<td><a href="/view(.*?)">', getdata)
            for link in pasteurl:
                link = 'http://slexy.org/raw' + link
                getmails(link, prox)
        except IOError:
            pass
        except:
            pass

    #Below function is created for collecting debpaste recent pastes
    def debpaste(prox):
        pburl = 'http://paste.debian.net'
        try:
            randomip = proxies[randint(0, len(proxies)-1)]
            if prox == '--proxy':
                getdata = urllib.urlopen(pburl, proxies={'http':randomip}).read()
            else:
                getdata = urllib.urlopen(pburl).read()
            pasteurl =  re.findall("<li><a href='//paste.debian.net(.*?)'>", getdata)
            i = 1
            for link in pasteurl:
                link = 'http://paste.debian.net/plain' + link
                getmails(link, prox)
                i += 1
                if i == 11:
                    # those are of no use, so stop
                    break
        except IOError:
            pass
        except:
            pass

    #this function is designed to extract emails from given urls(one url per line)
    def customurl(prox):
        lines = open('sources.txt', 'r').read().split('\n')
        for link in lines:
            link = link.replace('\n','')
            ink = link.replace('\r','')
            if 'https://' not in link:
                if 'http://' not in link:
                    link = 'http://' + link
            getmails(link, prox)

    #Below function is created for collecting urls from searx search engines
    def searx(dork,pages, prox):
        sitelist = []
        print "You are searching: " + dork
        print "Page depth: ",pages
        p = 1
        m = pages # max pages to crawl in the engine result
        while p <= m:
            data = urllib.urlencode({'category_general':'1', 'q':dork,'pageno': p , 'time_range':'', 'language':'all'})
            data = data.replace('+','%20')
            try:
                search = urllib2.Request('https://searx.laquadrature.net/', data)
                req = opener.open(search)
                source = req.read()
                if "we didn't find any results" in source:
                    print 'No Result in: ' + dork
                    p = 100000000  
                sites = re.findall('class="result_header"><a href="(.*?)" rel="noreferrer">', source)
                sitelist.extend(sites)
                if "</span> next page</button>" in source:
                    tp = p
                    p += 1
                    print 'Scanned page(s) so far: ' + str(tp)
                else:
                    p += 1000000000
            except urllib2.URLError as e:
                continue
            except urllib2.HTTPError as e:
                continue
            except IOError:
                continue
            except httplib.HTTPException:
                continue
            except:
                continue
        uniqsites = list(set(sitelist))
        for eachsite in uniqsites:
            getmails(eachsite, prox)

    # Main program interface starts from below
    print 'Total emails in collections: ',len(open('collections.txt', 'r+').readlines())
    print 'Hello Sir, welcome to your crawler index :)'
    print 'Select one of the below options to execute:'
    print '1. Search Pastebin Now'
    print '2. Search Slexy Now'
    print '3. Search Paste.Debian.net Now'
    print '4. Search SearX Now'
    print '5. Scan from File Urls'
    print '6. Exit'
    while 1:
        if pbin == '--pb':
            print 'Looking in pastebin ...'
            pastebin(prox)
        if slx == '--slx':
            print 'Looking in slexy ...'
            slexy(prox)
        if debp == '--debp':
            print 'Looking in debpaste'
            debpaste(prox)
        if cus == '--src':
            print 'Looking in File(sources.txt)'
            customurl(prox)
        if srx == '--srx':
            print 'Attempting scan in Searx'
            searx(dork, pagedepth, prox)
        print 'Total emails in collections now: ',len(open('collections.txt', 'r+').readlines())
        time.sleep(3)
except:
    print 'USAGE: python bot.py --pb --slx --debp --src --srx "something to search" 3 --proxy'
    print 'replace --n to skip a feature'
    print '3 represents number of pages to search'



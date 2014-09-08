
#!/usr/bin/python
#url_GOOG = "http://finance.yahoo.com/d/quotes.csv?s=GOOG&f=l1"
#url_AAPL = "http://finance.yahoo.com/d/quotes.csv?s=AAPL&f=l1"
#url_FB = "http://finance.yahoo.com/d/quotes.csv?s=FB&f=l1"
#url_ERIC = "http://finance.yahoo.com/d/quotes.csv?s=ERIC&f=l1"

#GOOG = urllib.urlopen(url_GOOG).read().strip().strip('"')
#AAPL = urllib.urlopen(url_AAPL).read().strip().strip('"')
#FB = urllib.urlopen(url_FB).read().strip().strip('"')
#ERIC = urllib.urlopen(url_ERIC).read().strip().strip('"')
#b = float(GOOG)           

#print "\033[37m\033[41mApple: " + str(round(float(ystockquote.get_price('AAPL')), 1)) + " \033[0m",
#print "\033[37m\033[41mEricsson: " + str(round(float(ystockquote.get_price('ERIC')), 1)) + " \033[0m",
#print "\033[37m\033[41mFacebook: " + str(round(float(ystockquote.get_price('FB')), 1)) + " \033[0m"
import time
import datetime
import ystockquote
import os, sys
import tty
import ast
from select import select
#----------------------------------------------------------

class stock_name:
    Google = 'GOOG'
    Facebook = 'FB'
    Ericsson = 'ERIC'
    Apple = 'AAPL'
    IBM = 'IBM'
    Euro = 'EURUSD=X'
#----------------------------------------------------------
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[37m\033[42m'
    #OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    #FAIL = '\033[91m'
    FAIL = '\033[37m\033[41m'    
    ENDC = '\033[0m'
#----------------------------------------------------------
class NotTTYException(Exception): pass

class TerminalFile:
    def __init__(self,infile):
        if not infile.isatty():
            raise NotTTYException()
        self.file=infile

        #prepare for getch
        self.save_attr=tty.tcgetattr(self.file)
        newattr=self.save_attr[:]
        newattr[3] &= ~tty.ECHO & ~tty.ICANON
        tty.tcsetattr(self.file, tty.TCSANOW, newattr)

    def __del__(self):
        #restoring stdin
        import tty  #required this import here
        tty.tcsetattr(self.file, tty.TCSADRAIN, self.save_attr)

    def getch(self):
        if select([self.file],[],[],0)[0]:
            c=self.file.read(1)
        else:
            c=''
        return c


#----------------------------------------------------------
def tid():
    now = datetime.datetime.now()
    return datetime.time(now.hour, now.minute, now.second)

#----------------------------------------------------------

def last_line(aktie):

    if os.path.exists(aktie + '.data') == True:
        if os.stat(aktie + '.data').st_size >= 1:
            s = open(aktie + '.data', 'r')
            return float((list(s)[-1]))
        else:
            return 0
    else:
        file(aktie + '.data', 'w').close()
        return 0
#----------------------------------------------------------

def get_p_c(aktie):
        price = round(float(ystockquote.get_price(aktie)), 1)
        if price > last_line(aktie):         
            f = open(aktie + '.data', 'a')
            f.writelines('\n' + str(tid()) + '\n' + str(price))
            f.close()
            return bcolors.OKGREEN + str(price) + bcolors.ENDC       
        if price < last_line(aktie):            
            f = open(aktie + '.data', 'a')
            f.writelines('\n' + str(tid()) + '\n' + str(price))
            f.close()
            return bcolors.FAIL + str(price) + bcolors.ENDC        
        else:
            return str(price)
#------------------------------------------------------------


def main():
    #a = raw_input('Enter stock name: ')
    a = 'Google'
    b = 'Apple'
    c = 'Facebook'
    d = 'IBM'
    s=TerminalFile(sys.stdin)
    print "Press q to quit..."
    while s.getch()!="q":
        print tid(),
        print a + ': ' + get_p_c(getattr(stock_name, a)),
        print b + ': ' + get_p_c(getattr(stock_name, b)),
        print c + ': ' + get_p_c(getattr(stock_name, c)),
        print '|' + d + ': ' + get_p_c(getattr(stock_name, d))
        print '--------+-------------+------------+---------------+----------+'
        
        #os.system('clear')
  




        

main()

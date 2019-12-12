# QND-Cisco_ISE_ANC_MAC_Address_Blacklist

This Quick & Dirty (QND) example uses Python to Blacklist a MAC Address in Cisco Identity Services Engine through a combination of the ISE's API and the Adaptive Network Control feature.

# Setup
### Cisco Identity Services Engine
This script successfully tested on ISE v2.3 and v2.4.

You must have ISE licensing in place that allows you to the Adaptive Network Control feature.  Today this feature is provided by Cisco ISE PLUS licensing.

In ISE you must;
 - Create Policy Conditions that reference the ANC Status and you must create authorisation profiles that take some kind of suitable action (like Deny Access, assign to a quaarantine VLAN, etc).
 - Enable External Restful Services ("ERS") via the **Administration > System > Settings** menu within the ISE GUI
 - Create an ERS User via the **Administration > System > Admin Access** menu and the **Administrators > Admin Users** sub-menu

### Python
This script tested on Python v3.7, but will likely work on any 3.x release.

This script requires use of the following Python modules;
 - requests
 - sys

This script assumes you have embedded the ERS Credentials within.  This is not particularly recommended best practiise for production scenarios, but for the sake of a QND example, keeping the credentials within the script makes it easier to understand and keeps focus on the task at hand.


# Usage

`ise.py [ISE IPv4 Primary Admin Mgmt Addr] [Colon delimited Endpoint MAC Address] ["Clear" | ISE ANC Policy Name]`

Eg, To add endpoint with MAC Address 0000.0000.0000 to the Blacklist ANC Group...
`ise.py 10.10.10.10 00:00:00:00:00:00 Blacklist`

Eg, To remove endpoint with MAC Address 1122.3344.5566 from any/all ANC Groups...
`ise.py 10.10.10.10 11:22:33:44:55:66 Clear`

**Note:*
 - The formatting of the MAC Address is important
 - ANC Policy Names, and the 'Clear' command, are all case sensitive

import os
import time
import subprocess
import re

def sendDeauth():

	saved_time = ""
	while(True):
		stream = os.popen('sudo tail -n 6 /var/log/snort/alert')
		output = stream.readlines()
		if output[0].find("Detected") != -1: 
			line = output[2]
			time_alert = line[0:14]
			src_ip_addr = line[22:30]

			print("Lasted alert time:"+ time_alert )
			if(saved_time != time_alert):
				print("-----------"+ src_ip_addr + "-----------")
				saved_time = time_alert

				with open('arptable.txt') as f:
					mactable = f.read()

					if src_ip_addr not in mactable:
						print("Can't find MAC address for " + src_ip_addr)
						print("Can't deauth")
					else:
						print("Found MAC address for "+ src_ip_addr)
						index = mactable.index(src_ip_addr)
						src_mac_addr = mactable[index+9:index+26]
						print(src_mac_addr)
						print("Start deauth STMAC: " + src_mac_addr + " in 10 second")
						deauth_p = subprocess.Popen("timeout 10 aireplay-ng -0 0 -a 02:00:00:00:03:00 -c "+src_mac_addr+" ap2-wlan1mon", shell=True, stdout=subprocess.PIPE)
						time.sleep(10)
						deauth_p.terminate() 
						print("Finished deauth station\n")
			else:
				print("-------Found nothing---------\n")
				time.sleep(5)

	
def pre_proc():
	print("Setting up pre-run configurations...")
	pre_p = subprocess.Popen("airmon-ng start ap2-wlan1",
		                 shell=True, stdout=subprocess.PIPE)
	time.sleep(3)
	pre_p = subprocess.Popen(
	    "airodump-ng ap2-wlan1mon --bssid 02:00:00:00:03:00 --channel 5", shell=True, stdout=subprocess.PIPE)
	time.sleep(3)
	pre_p.terminate()
	print("Finished configurations")
	print("Start waiting alert...")
	try:
		sendDeauth()
	except KeyboardInterrupt:
		print("\nTerminating prevention process.\nEmpty snort alert.\n")
		with open('/var/log/snort/alert', "w") as myfile:
			myfile.write("This snort alert logs is used for preventation...")

if __name__ == "__main__":
	pre_proc()


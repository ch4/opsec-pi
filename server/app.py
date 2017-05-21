import subprocess
import libs.evil as evil
from libs.iw_parse import get_interfaces
from flask import Flask, render_template, request, jsonify
app = Flask(__name__)
BACKHAUL_INTERFACE = 'wlan1' # TODO: load this from a preferences file

@app.route('/scan', methods=['GET'])
def scan_wifi():
	networks = get_interfaces(interface=BACKHAUL_INTERFACE)
	return jsonify({'networks':networks})
	
@app.route('/scan/open', methods=['GET'])
def scan_open_wifi():
	networks = get_interfaces(interface=BACKHAUL_INTERFACE)
	open_networks = filter(lambda x: x['Encryption'] == 'Open', networks) 
	return jsonify({'networks':open_networks})
	
@app.route('/network/connect', methods=['POST'])
def connect_to_network():
	body = request.get_json()
	name = body['Name']
	encryption = body['Encryption']
	password = None
	
	try:
		password = body['Password']
	except:
		pass
		
	print(str(body))
	evil.connect_to_network(BACKHAUL_INTERFACE, name, get_encryption_type_from_iwlist_type(encryption), password)
	return 'hello'

def get_encryption_type_from_iwlist_type(iwlist_type):
	if iwlist_type == 'Open':
		return 'OPEN'
	if iwlist_type == 'WEP':
		return 'WEP'

	return 'WPA'

@app.route("/")
def main():
	# [{'Name': 'ATT368', 'Address': '6C:CA:08:65:17:A0', 'Encryption': ' v.1', 'Bit Rates': '1 Mb/s; 2 Mb/s; 5.5 Mb/s; 11 Mb/s; 18 Mb/s', 'Signal Level': '-79 dBm', 'Quality': '44', 'Channel': '11'}]
	#~ networks = scan_wifi()
	#~ networks = scan_open_wifi()
	data = {
		#~ 'wifiNetworks' : networks
	}
	
	return render_template('index.html', **data)

#~ @app.route("/<changePin>/<action>")
#~ def action(changePin, action):
	#~ pass

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=80, debug=True)

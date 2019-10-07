import requests

a  = requests.post("http://127.0.0.1:5000/bus", json={'entry':'Bangalore', 'dest':'Gandhinagar', 'date':'07-10-2019', 'seats':'2', 'latEn':12.9716, 'lonEn':77.5946, 'latDes':23.2156, 'lonDes':72.6369}).text
print(a)
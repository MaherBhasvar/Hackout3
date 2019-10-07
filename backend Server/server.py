from flask import Flask
from flask import jsonify, request
from fetch import search_buses, search_flights, lat_lon
from func import majorCityFinder, nearby3, local
import re
from flask_cors import CORS, cross_origin

Data = [['Mumbai', 19.0760, 72.8777, 'BOM'],
['Ahmedabad', 23.0225, 72.5714, 'AMD'],
['Vadodara', 22.3072, 73.1812, 'BDQ'],
['Surat', 21.1702, 72.8311, 'STV'],
['Jaipur',  26.9124, 75.7873, 'JAI'],
['Bhopal', 23.2599, 77.4126, 'BHO'],
['Indore',  22.7196, 75.8577, 'IDR'],
['Chennai', 13.0827, 80.2707, 'MAA'],
['Delhi', 28.6139, 77.2090, 'DEL'],
['Lucknow', 26.8467, 80.9462, 'LKO'],
['Calicut', 11.2588, 75.7804, 'CCJ'],
['Hyderabad', 17.3850, 78.4867, 'HYD'],
['Bangalore', 12.9716, 77.5946, 'BLR'],
['Kolkata', 22.5726, 88.3639, 'CCU'],
['Kochi', 9.9312, 76.2673, 'COK'],
['Goa', 15.4909, 73.8278, 'GOI'],
['Mangaluru', 12.9141, 74.8560, 'IXE'],
['Varanasi', 25.3176, 82.9739, 'VNS'],
['Chandigarh', 30.7333, 76.7794, 'IXC'],
['Amritsar', 31.6340, 74.8723, 'LUH'],
['Siliguri', 26.7271, 88.3953, 'IXB'],
['Coimbatore', 11.0168, 76.9558, 'CJB'],
['Madurai', 9.9252, 78.1198, 'IXM'],
['Tiruchirapalli', 10.7905, 17.7047, 'TRZ'],
['Nagpur', 21.1458, 79.0882, 'NAG'],
['Bhuvneshwar', 20.2961, 85.8245, 'BBI'],
['Vishakhapatnam', 17.6868, 83.2185, 'VTZ'],
['Pune', 18.5204, 73.8567, 'PNQ']]

# Create the application.
APP = Flask(__name__)
cors = CORS(APP, resources={r"/": {"origins": "*"}})
APP.config['CORS_HEADERS'] = 'Content-Type'

latEn, lonEn = 0, 0
latDes, lonDes = 0, 0

@APP.route('/locate', methods=['GET', 'POST'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def Locate():
	global latEn, lonEn, latDes, lonDes
	data = request.json
	latEn, lonEn = lat_lon(data.get('entry'))
	latDes, lonDes = lat_lon(data.get('dest'))
	return jsonify({'1':2})

@APP.route('/locate1', methods=['GET', 'POST'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def Locate1():
	global latEn, lonEn
	data = request.json
	latEn, lonEn = lat_lon(data.get('city'))
	return jsonify(geometry={'lat':latEn, 'lon':lonEn})

@APP.route('/bus', methods=['GET', 'POST'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def bus():
	global latEn, lonEn, latDes, lonDes
	data = request.json
	entry = data.get('entry')
	dest = data.get('dest')
	date = data.get('date')
	seats = data.get('seats')
	d = search_buses(entry, dest, date, int(seats))
	if d==-1:
		majorCity1 = majorCityFinder(entry, [latEn, lonEn], Data)  ## Data Load
		majorCity2 = majorCityFinder(dest, [latDes, lonDes], Data)
		cas = -1
		if majorCity1[1]==-1 and majorCity2[1]==-1:
			d1, dd1 = search_buses(majorCity1[0][0], majorCity2[0][0], date, int(seats))
			cas=1
			price_a_local = local(majorCity1[2])
			price_b_local = local(majorCity2[2])
			packages = {'case':1,
						'Package1':{'A':entry,
									'D':dest,
									'Type':'Cost Effective', 
									'Bus Details':d1,
									'Bus Price':d1[4],
									'Total Price':float(re.sub(',','', d1[4]))+price_a_local[1]+price_b_local[1],
									'Local A': price_a_local[0],
									'Local B': price_b_local[1]},
						'Package2':{'A':entry,
									'D':dest,
									'Type':'Time effective', 
									'Bus Details':dd1,
									'Bus Price':dd1[4],
									'Total Price':float(re.sub(',','', dd1[4]))+price_a_local[1]+price_b_local[1],
									'Local A': price_a_local[0],
									'Local B': price_b_local[1]}
						}
		elif majorCity1[1]!=-1 and majorCity2[1]!=-1:
			a1, b1, c1 = nearby3(entry, [latEn, lonEn], Data)
			a2, b2, c2 = nearby3(dest, [latDes, lonDes], Data)
			print(a1)
			d1, dd1 = search_buses(a1[0][0], a2[0][0], date, int(seats))
			d2, dd2 = search_buses(a1[0][0], b2[0][0], date, int(seats))
			d3, dd3 = search_buses(b1[0][0], a2[0][0], date, int(seats))
			d4, dd4 = search_buses(b1[0][0], b2[0][0], date, int(seats))
			cas=2

			packages = {'case':2,
						'Package1':{'A':entry,
									'B':a1[0][0],
									'C':a2[0][0],
									'D':dest,
									'Type':'Cost Effective', 
									'Bus Details':d1,
									'Bus Price':d1[4],
									'Total Price':float(re.sub(',','',d1[4]))+local(a1[2])[1]+local(a2[2])[1],
									'Local A': local(a1[2])[0],
									'Local B': local(a2[2])[0]},
						'Package2':{'A':entry,
									'B':a1[0][0],
									'C':b2[0][0],
									'D':dest,
									'Type':'Cost Effective', 
									'Bus Details':d2,
									'Bus Price':d2[4],
									'Total Price':float(re.sub(',','',d2[4]))+local(a1[2])[1]+local(b2[2])[1],
									'Local A': local(a1[2])[0],
									'Local B': local(b2[2])[0]},
						'Package3':{'A':entry,
									'B':a1[0][0],
									'C':a2[0][0],
									'D':dest,
									'Type':'Time effective', 
									'Bus Details':dd1,
									'Bus Price':dd1[4],
									'Total Price':float(re.sub(',','',dd1[4]))+local(a1[2])[1]+local(a2[2])[1],
									'Local A': local(a1[2])[0],
									'Local B': local(a2[2])[0]},
						'Package4':{'A':entry,
									'B':a1[0][0],
									'C':b2[0][0],
									'D':dest,
									'Type':'Time Effective', 
									'Bus Details':dd2,
									'Bus Price':dd2[4],
									'Total Price':float(re.sub(',','',dd2[4]))+local(a1[2])[1]+local(b2[2])[1],
									'Local A': local(b1[2])[0],
									'Local B': local(b2[2])[0]},
						'Package5':{'A':entry,
									'B':b1[0][0],
									'C':a2[0][0],
									'D':dest,
									'Type':'Cost Effective', 
									'Bus Details':d3,
									'Bus Price':d3[4],
									'Total Price':float(re.sub(',','',d3[4]))+local(b1[2])[1]+local(a2[2])[1],
									'Local A': local(b1[2])[0],
									'Local B': local(a2[2])[0]},
						'Package6':{'A':entry,
									'B':b1[0][0],
									'C':a2[0][0],
									'D':dest,
									'Type':'Time Effective', 
									'Bus Details':dd3,
									'Bus Price':dd3[4],
									'Total Price':float(re.sub(',','',dd3[4]))+local(b1[2])[1]+local(a2[2])[1],
									'Local A': local(b1[2])[0],
									'Local B': local(a2[2])[0]},
						'Package7':{'A':entry,
									'B':b1[0][0],
									'C':b2[0][0],
									'D':dest,
									'Type':'Cost Effective', 
									'Bus Details':d4,
									'Bus Price':d4[4],
									'Total Price':float(re.sub(',','',d4[4]))+local(b1[2])[1]+local(b2[2])[1],
									'Local A': local(b1[2])[0],
									'Local B': local(b2[2])[0]},
						'Package8':{'A':entry,
									'B':b1[0][0],
									'C':b2[0][0],
									'D':dest,
									'Type':'Time Effective', 
									'Bus Details':dd4,
									'Bus Price':dd4[4],
									'Total Price':float(re.sub(',','',dd4[4]))+local(b1[2])[1]+local(b2[2])[1],
									'Local A': local(b1[2])[0],
									'Local B': local(b2[2])[0]}
									}

		elif majorCity1[1]!=-1:
			a1, b1, c1 = nearby3(entry, [latEn, lonEn], Data)
			print(a1, b1, c1)
			d1, dd1 = search_buses(a1[0][0], majorCity2[0][0], date, int(seats))
			d2, dd2 = search_buses(b1[0][0], majorCity2[0][0], date, int(seats))
			d3, dd3 = search_buses(c1[0][0], majorCity2[0][0], date, int(seats))
			cas=3
			packages = {'case':3,
						'Package1':{'A':entry,
									'B':a1[0][0],
									'D':dest,
									'Type':'Cost Effective', 
									'Bus Details':d1,
									'Bus Price':d1[4],
									'Total Price':float(re.sub(',','',d1[4]))+local(a1[2])[1],
									'Local A': local(a1[2])[0],
									},
						'Package2':{'A':entry,
									'B':b1[0][0],
									'D':dest,
									'Type':'Cost Effective', 
									'Bus Details':d2,
									'Bus Price':d2[4],
									'Total Price':float(re.sub(',','',d2[4]))+local(b1[2])[1],
									'Local A': local(b1[2])[0]},
						'Package3':{'A':entry,
									'B':a1[0][0],
									'D':dest,
									'Type':'Time effective', 
									'Bus Details':dd1,
									'Bus Price':dd1[4],
									'Total Price':float(re.sub(',','',dd1[4]))+local(a1[2])[1],
									'Local A': local(a1[2])[0]},
						'Package4':{'A':entry,
									'B':b1[0][0],
									'D':dest,
									'Type':'Time Effective', 
									'Bus Details':dd2,
									'Bus Price':dd2[4],
									'Total Price':float(re.sub(',','',dd2[4]))+local(b1[2])[1],
									'Local A': local(b1[2])[0]},
						'Package5':{'A':entry,
									'B':c1[0][0],
									'D':dest,
									'Type':'Cost Effective', 
									'Bus Details':d3,
									'Bus Price':d3[4],
									'Total Price':float(re.sub(',','',d3[4]))+local(c1[2])[1],
									'Local A': local(c1[2])[0],
									},
						'Package6':{'A':entry,
									'B':c1[0][0],
									'D':dest,
									'Type':'Time Effective', 
									'Bus Details':dd3,
									'Bus Price':dd3[4],
									'Total Price':float(re.sub(',','',dd3[4]))+local(c1[2])[1],
									'Local A': local(c1[2])[0]}
						}
		else:
			a1, b1, c1 = nearby3(dest, [latDes, lonDes], Data)
			d1, dd1 = search_buses(majorCity1[0][0], a1[0][0], date, int(seats))
			d2, dd2 = search_buses(majorCity1[0][0], b1[0][0], date, int(seats))
			d3, dd3 = search_buses(majorCity1[0][0], c1[0][0], date, int(seats))
			cas=4
			packages = {'case':4,
						'Package1':{'A':entry,
									'C':a1[0][0],
									'D':dest,
									'Type':'Cost Effective', 
									'Bus Details':d1,
									'Bus Price':d1[4],
									'Total Price':float(re.sub(',','', d1[4]))+local(a1[2])[1],
									'Local B': local(a1[2])[0],
									},
						'Package2':{'A':entry,
									'C':b1[0][0],
									'D':dest,
									'Type':'Cost Effective', 
									'Bus Details':d2,
									'Bus Price':d2[4],
									'Total Price':float(re.sub(',','', d2[4]))+local(b1[2])[1],
									'Local B': local(b1[2])[0]},
						'Package3':{'A':entry,
									'C':a1[0][0],
									'D':dest,
									'Type':'Time effective', 
									'Bus Details':dd1,
									'Bus Price':dd1[4],
									'Total Price':float(re.sub(',','', dd1[4]))+local(a1[2])[1],
									'Local B': local(a1[2])[0]},
						'Package4':{'A':entry,
									'C':b1[0][0],
									'D':dest,
									'Type':'Time Effective', 
									'Bus Details':dd2,
									'Bus Price':dd2[4],
									'Total Price':float(re.sub(',','',dd2[4]))+local(b1[2])[1],
									'Local B': local(b1[2])[0]},
						'Package5':{'A':entry,
									'C':c1[0][0],
									'D':dest,
									'Type':'Cost Effective', 
									'Bus Details':d3,
									'Bus Price':d3[4],
									'Total Price':float(re.sub(',','',d3[4]))+local(c1[2])[1],
									'Local B': local(c1[2])[0],
									},
						'Package6':{'A':entry,
									'C':c1[0][0],
									'D':dest,
									'Type':'Time Effective', 
									'Bus Details':dd3,
									'Bus Price':dd3[4],
									'Total Price':float(re.sub(',','',dd3[4]))+local(c1[2])[1],
									'Local B': local(c1[2])[0]}
						}
	else:
		cas=1
		packages = {'case':1,
					'Package1':{'A':entry,
								'D':dest,
								'Type':'Cost Effective', 
								'Bus Details':d[0],
								'Bus Price':d[0][4],
								'Total Price':float(re.sub(',','', d[0][4]))},
					'Package2':{'A':entry,
								'D':dest,
								'Type':'Time effective', 
								'Bus Details':d[1],
								'Bus Price':d[1][4],
								'Total Price':float(re.sub(',','', d[1][4]))}
		}
	return jsonify(packages)





@APP.route('/flight', methods=['GET', 'POST'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def flight():
	global latEn, lonEn, latDes, lonDes
	data = request.json
	print(data)
	entry = data.get('entry')
	dest = data.get('dest')
	date = data.get('date')
	seats = data.get('seats')
	majorCity1 = majorCityFinder(entry, [latEn, lonEn], Data)
	majorCity2 = majorCityFinder(dest, [latDes, lonDes], Data)
	print(majorCity1)
	cas = -1
	if majorCity1[1]==-1 and majorCity2[1]==-1:
	### Implement msearch_flightsode
		print("HERE2")
		d1, dd1 = search_flights(majorCity1, majorCity2, date, int(seats))
		cas=1
		price_a_local = local(majorCity1[2])
		price_b_local = local(majorCity2[2])
		packages = {'case':1,
					'Package1':{'A':entry,
								'D':dest,
								'Type':'Cost Effective', 
								'Flight Details':d1,
								'Flight Price':d1[4],
								'Total Price':float(re.sub(',','',d1[4]))+price_a_local[1]+price_b_local[1],
								'Local A': price_a_local[0],
								'Local B': price_b_local[1]},
					'Package2':{'A':entry,
								'D':dest,
								'Type':'Time effective', 
								'Flight Details':dd1,
								'Flight Price':dd1[4],
								'Total Price':float(re.sub(',','',dd1[4]))+price_a_local[1]+price_b_local[1],
								'Local A': price_a_local[0],
								'Local B': price_b_local[1]}
					}

	elif majorCity1[1]!=-1 and majorCity2[1]!=-1:
		a1, b1, c1 = nearby3(entry, [latEn, lonEn], Data)
		a2, b2, c2 = nearby3(dest, [latDes, lonDes], Data)

		d1, dd1 = search_flights(a1, a2, date, int(seats))
		d2, dd2 = search_flights(a1, b2, date, int(seats))
		d3, dd3 = search_flights(b1, a2, date, int(seats))
		d4, dd4 = search_flights(b1, b2, date, int(seats))
		cas=2
		print("Here34")

		packages = {'case':2,
					'Package1':{'A':entry,
								'B':a1[0][0],
								'C':a2[0][0],
								'D':dest,
								'Type':'Cost Effective', 
								'Flight Details':d1,
								'Flight Price':d1[4],
								'Total Price':float(re.sub(',','',d1[4]))+local(a1[2])[1]+local(a2[2])[1],
								'Local A': local(a1[2])[0],
								'Local B': local(a2[2])[0]},
					'Package2':{'A':entry,
								'B':a1[0][0],
								'C':b2[0][0],
								'D':dest,
								'Type':'Cost Effective', 
								'Flight Details':d2,
								'Flight Price':d2[4],
								'Total Price':float(re.sub(',','',d2[4]))+local(a1[2])[1]+local(b2[2])[1],
								'Local A': local(a1[2])[0],
								'Local B': local(b2[2])[0]},
					'Package3':{'A':entry,
								'B':a1[0][0],
								'C':a2[0][0],
								'D':dest,
								'Type':'Time effective', 
								'Flight Details':dd1,
								'Flight Price':dd1[4],
								'Total Price':float(re.sub(',','',dd1[4]))+local(a1[2])[1]+local(a2[2])[1],
								'Local A': local(a1[2])[0],
								'Local B': local(a2[2])[0]},
					'Package4':{'A':entry,
								'B':a1[0][0],
								'C':b2[0][0],
								'D':dest,
								'Type':'Time Effective', 
								'Flight Details':dd2,
								'Flight Price':dd2[4],
								'Total Price':float(re.sub(',','',dd2[4]))+local(a1[2])[1]+local(b2[2])[1],
								'Local A': local(b1[2])[0],
								'Local B': local(b2[2])[0]},
					'Package5':{'A':entry,
								'B':b1[0][0],
								'C':a2[0][0],
								'D':dest,
								'Type':'Cost Effective', 
								'Flight Details':d3,
								'Flight Price':d3[4],
								'Total Price':float(re.sub(',','',d3[4]))+local(b1[2])[1]+local(a2[2])[1],
								'Local A': local(b1[2])[0],
								'Local B': local(a2[2])[0]},
					'Package6':{'A':entry,
								'B':b1[0][0],
								'C':a2[0][0],
								'D':dest,
								'Type':'Time Effective', 
								'Flight Details':dd3,
								'Flight Price':dd3[4],
								'Total Price':float(re.sub(',','',dd3[4]))+local(b1[2])[1]+local(a2[2])[1],
								'Local A': local(b1[2])[0],
								'Local B': local(a2[2])[0]},
					'Package7':{'A':entry,
								'B':b1[0][0],
								'C':b2[0][0],
								'D':dest,
								'Type':'Cost Effective', 
								'Flight Details':d4,
								'Flight Price':d4[4],
								'Total Price':float(re.sub(',','',d4[4]))+local(b1[2])[1]+local(b2[2])[1],
								'Local A': local(b1[2])[0],
								'Local B': local(b2[2])[0]},
					'Package8':{'A':entry,
								'B':b1[0][0],
								'C':b2[0][0],
								'D':dest,
								'Type':'Time Effective', 
								'Flight Details':dd4,
								'Flight Price':dd4[4],
								'Total Price':float(re.sub(',','',dd4[4]))+local(b1[2])[1]+local(b2[2])[1],
								'Local A': local(b1[2])[0],
								'Local B': local(b2[2])[0]}

					}
	elif majorCity1[1]!=-1:
		a1, b1, c1 = nearby3(entry, [latEn, lonEn], Data)
		print(a1, b1, c1)
		d1, dd1 = search_flights(a1, majorCity2, date, int(seats))
		d2, dd2 = search_flights(b1, majorCity2, date, int(seats))
		d3, dd3 = search_flights(c1, majorCity2, date, int(seats))
		cas=3
		print(d1)
		print(d2)
		packages = {'case':3,
					'Package1':{'A':entry,
								'B':a1[0][0],
								'D':dest,
								'Type':'Cost Effective', 
								'Flight Details':d1,
								'Flight Price':d1[4],
								'Total Price':float(re.sub(',','',d1[4]))+local(a1[2])[1],
								'Local A': local(a1[2])[0],
								},
					'Package2':{'A':entry,
								'B':b1[0][0],
								'D':dest,
								'Type':'Cost Effective', 
								'Flight Details':d2,
								'Flight Price':d2[4],
								'Total Price':float(re.sub(',','',d2[4]))+local(b1[2])[1],
								'Local A': local(b1[2])[0]},
					'Package3':{'A':entry,
								'B':a1[0][0],
								'D':dest,
								'Type':'Time effective', 
								'Flight Details':dd1,
								'Flight Price':dd1[4],
								'Total Price':float(re.sub(',','',dd1[4]))+local(a1[2])[1],
								'Local A': local(a1[2])[0]},
					'Package4':{'A':entry,
								'B':b1[0][0],
								'D':dest,
								'Type':'Time Effective', 
								'Flight Details':dd2,
								'Flight Price':dd2[4],
								'Total Price':float(re.sub(',','',dd2[4]))+local(b1[2])[1],
								'Local A': local(b1[2])[0]},
					'Package5':{'A':entry,
								'B':c1[0][0],
								'D':dest,
								'Type':'Cost Effective', 
								'Flight Details':d3,
								'Flight Price':d3[4],
								'Total Price':float(re.sub(',','',d3[4]))+local(c1[2])[1],
								'Local A': local(c1[2])[0],
								},
					'Package6':{'A':entry,
								'B':c1[0][0],
								'D':dest,
								'Type':'Time Effective', 
								'Flight Details':dd3,
								'Flight Price':dd3[4],
								'Total Price':float(re.sub(',','',dd3[4]))+local(c1[2])[1],
								'Local A': local(c1[2])[0]}
					}
	else:
		print("HERE")
		print(majorCity2)
		a1, b1, c1 = nearby3(dest, [latDes, lonDes], Data)
		d1, dd1 = search_flights(majorCity1, a1, date, int(seats))
		d2, dd2 = search_flights(majorCity1, b1, date, int(seats))
		d3, dd3 = search_flights(majorCity1, c1, date, int(seats))
		cas=4
		packages = {'case':4,
					'Package1':{'A':entry,
								'C':a1[0][0],
								'D':dest,
								'Type':'Cost Effective', 
								'Flight Details':d1,
								'Flight Price':d1[4],
								'Total Price':float(re.sub(',','', d1[4]))+local(a1[2])[1],
								'Local B': local(a1[2])[0],
								},
					'Package2':{'A':entry,
								'C':b1[0][0],
								'D':dest,
								'Type':'Cost Effective', 
								'Flight Details':d2,
								'Flight Price':d2[4],
								'Total Price':float(re.sub(',','', d2[4]))+local(b1[2])[1],
								'Local B': local(b1[2])[0]},
					'Package3':{'A':entry,
								'C':a1[0][0],
								'D':dest,
								'Type':'Time effective', 
								'Flight Details':dd1,
								'Flight Price':dd1[4],
								'Total Price':float(re.sub(',','', dd1[4]))+local(a1[2])[1],
								'Local B': local(a1[2])[0]},
					'Package4':{'A':entry,
								'C':b1[0][0],
								'D':dest,
								'Type':'Time Effective', 
								'Flight Details':dd2,
								'Flight Price':dd2[4],
								'Total Price':float(re.sub(',','',dd2[4]))+local(b1[2])[1],
								'Local B': local(b1[2])[0]},
					'Package5':{'A':entry,
								'C':c1[0][0],
								'D':dest,
								'Type':'Cost Effective', 
								'Flight Details':d3,
								'Flight Price':d3[4],
								'Total Price':float(re.sub(',','',d3[4]))+local(c1[2])[1],
								'Local B': local(c1[2])[0],
								},
					'Package6':{'A':entry,
								'C':c1[0][0],
								'D':dest,
								'Type':'Time Effective', 
								'Flight Details':dd3,
								'Flight Price':dd3[4],
								'Total Price':float(re.sub(',','',dd3[4]))+local(c1[2])[1],
								'Local B': local(c1[2])[0]}
					}

	return jsonify(packages)

if __name__ == '__main__':
    APP.debug=True
    APP.run( port=54545)
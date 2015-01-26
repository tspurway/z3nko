#Basic Python Server in Flask for showing reports
#Essentially put together from this page: http://flask.pocoo.org/docs/0.10/quickstart/
#Just run this like:
#> python server.py
#and then visit http://localhost:5000

from webbrowser import open as open_webpage
from flask import Flask, render_template
import redshift
app = Flask(__name__)

#set up database connection
cursor = redshift.cursor()
cache = redshift.build_tiles_cache(cursor)


@app.route('/impressions/<tile_id>')
def show_impressions(tile_id):
	"""Shows impressions for a tile_id"""
	
	#get a list of clients for the side bar
	clients = redshift.get_sponsored_client_list(cache)
	
	#get a list of possible locales and countries
	countries = redshift.get_countries_per_tile(cache, tile_id)
	
	#get some daily data for the last week
	impressions_data = redshift.get_impressions(cursor, "week", tile_id)
	
	#get some meta data about the tile from the tiles database
	meta_data = redshift.get_tile_meta_data(cache, tile_id)
	client = "{0} [{1}]".format([x[1] for x in meta_data if x[0] == 'title'][0], tile_id)
	
	#render the template
	return render_template("index.html", clients=clients, client=client, meta_data=meta_data, countries=countries, impressions_data=impressions_data, tile_id=tile_id)

@app.route('/impressions/<tile_id>/<country>')
def show_country_impressions(tile_id, country):
	"""Shows impressions for a tile_id"""
	
	#get a list of clients for the side bar
	clients = redshift.get_sponsored_client_list(cache)
	
	#get a list of possible locales and countries
	countries = redshift.get_countries_per_tile(cache, tile_id)
	
	#get some daily data for the last week
	impressions_data = redshift.get_impressions(cursor, "week", tile_id, country=country)
	
	#get some meta data about the tile from the tiles database
	meta_data = redshift.get_tile_meta_data(cache, tile_id)
	client = "{0} [{1}]".format([x[1] for x in meta_data if x[0] == 'title'][0], tile_id)
	
	#render the template
	return render_template("index.html", clients=clients, client=client, meta_data=meta_data, countries=countries, impressions_data=impressions_data, country=country, tile_id=tile_id)

@app.route('/countries_impressions/<tile_id>')
def show_countries_impressions(tile_id):
	"""Shows impressions for a tile_id"""
	
	#get a list of clients for the side bar
	clients = redshift.get_sponsored_client_list(cache)
	
	#get the country data
	countries_impressions_data = redshift.get_countries_impressions_data(cursor, tile_id) #start and end date coming soon
	
	#get some meta data about the tile from the tiles database
	meta_data = redshift.get_tile_meta_data(cache, tile_id)
	client = "{0} [{1}]".format([x[1] for x in meta_data if x[0] == 'title'][0], tile_id)
	
	#render the template
	return render_template("index.html", clients=clients, client=client, meta_data=meta_data, countries_impressions_data=countries_impressions_data, tile_id=tile_id)

@app.route('/tile/<client>/<locale>')
def show_creative_selection_page(client, locale):
	"""Shows a page that lets users select the specific creative"""
	
	#get a list of clients for the side bar
	clients = redshift.get_sponsored_client_list(cache)
	
	#get a list of possible locales and countries
	attributes = redshift.get_client_attributes(cursor, cache, client)
	
	#get a list of all the tiles in that locale
	tiles = redshift.get_tiles_from_client_in_locale(cache, client, locale)
	
	#render the template
	return render_template("index.html", clients=clients, attributes=attributes, client=client, creative=tiles, locale=locale)

@app.route('/tile/<client>')
def show_locale_selection_page(client):
	"""Shows a page that lets users select the specific locale and country"""
	
	#get a list of clients for the side bar
	clients = redshift.get_sponsored_client_list(cache)
	
	#get a list of possible locales and countries
	attributes = redshift.get_client_attributes(cursor, cache, client)
	
	#render the template
	return render_template("index.html", clients=clients, attributes=attributes, client=client)

@app.route('/')
def show_main_page():
	#get a list of clients for the side bar
	clients = redshift.get_sponsored_client_list(cache)
	#render the template
	return render_template("index.html", clients=clients, main_page=True)

if __name__ == '__main__':
	app.debug = True
	#open_webpage("http://localhost:5000/")
	app.run()





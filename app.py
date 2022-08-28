#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
import datetime

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

# TODO: connect to a local postgresql database
migrate = Migrate(app, db)

# RESOURCES - https://flask-migrate.readthedocs.io/en/latest/
# RESOURCES - https://www3.ntu.edu.sg/home/ehchua/programming/sql/PostgreSQL_GetStarted.html
# RESOURCES - https://www.digitalocean.com/community/tutorials/how-to-query-tables-and-paginate-data-in-flask-sqlalchemy
# flask db stamp head
# flask db migrate
# flask db upgrade

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    website = db.Column(db.String(500))
    seeking_talent = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(500))

    # def __repr__(self):
    #   #return {"Venue ID": self.id, "Venue Name":self.name}
    #   return 'Venue(' + str(self.id) + ',' + str(self.name) + ')'

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(500))
    seeking_venue = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(500))

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

class Show(db.Model):
    __tablename__ = 'show'

    id = db.Column(db.Integer, primary_key=True)
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'))
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'))
    start_time = db.Column(db.DateTime)


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(str(value))
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.

  data = Venue.query.all()
  venues = Venue.query.join(Show).filter(Show.start_time < datetime.datetime.now())
  
  return render_template('pages/venues.html', areas=data, venues=venues);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on venues with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"

  search_value = request.form.get('search_term', '')

  data = Venue.query.filter(Venue.name.ilike("%{}%".format(search_value)))

  response={
    "count": data.count(),
    "data": data
  }

  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id

  data = Venue.query.get(venue_id)

  # data = list(filter(lambda d: d['id'] == venue_id, [data1, data2, data3]))[0]
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  if request.method == 'POST':
    #print(request.form)
    try:
      venue = Venue(
        name = request.form['name'],
        genres = request.form['genres'],
        address = request.form['address'],
        city = request.form['city'],
        state = request.form['state'],
        phone = request.form['phone'],
        website = request.form['website_link'],
        facebook_link = request.form['facebook_link'],
        seeking_talent = True if request.form.get('seeking_talent', False) else False,
        seeking_description = request.form['seeking_description'],
        image_link = request.form['image_link'],
      )

      db.session.add(venue)
      db.session.commit()
      #print("SUCCESSFUL")

    # on successful db insert, flash success
      flash('Venue ' + request.form['name'] + ' was successfully listed!')
    
    except:
      # TODO: on unsuccessful db insert, flash an error instead.
      # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
      # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
      flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
    
    finally:
      return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  print("PRINTING DELETE REQUEST")
  try:
    del_obj = db.session.query(Venue).filter(Venue.id==venue_id)
    db.session.delete(del_obj)
    db.session.commit()

    flash('Venue record ' + del_obj.name + ' with ID: ' + del_obj.id + ' deleted successfully')

  except:
    flash('Error! Could not delete record ' + del_obj.name + ' with ID: ' + del_obj.id)

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage

  finally:
    return render_template('pages/venues.html')

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database

  data = Artist.query.all()

  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".

  search_value = request.form.get('search_term', '')
  data = Artist.query.filter(Artist.name.ilike('%{}%'.format(search_value)))

  response={
    "count": data.count(),
    "data": data
  }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id

  data = Artist.query.get(artist_id)

  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()

  artist = Artist.query.get(artist_id)

  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

    if request.method == 'POST':
        print(request.form)

    try:
      artist = Artist(
        name = request.form['name'],
        genres = request.form['genres'],
        #address = request.form['address'],
        city = request.form['city'],
        state = request.form['state'],
        phone = request.form['phone'],
        website = request.form['website_link'],
        facebook_link = request.form['facebook_link'],
        seeking_venue = True if request.form.get('seeking_venue', False) else False,
        seeking_description = request.form['seeking_description'],
        image_link = request.form['image_link'],       
      )
      db.session.add(artist)
      db.session.commit()

      flash('Record with id ' + artist_id + ' updated successfully')

    except:
      flash('Error occured. Record with id ' + artist_id + ' failed to update')

    finally:
      return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue = Venue.query.get(venue_id)

  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes

  if request.method == 'POST':
    print(request.form)

    try:
      venue = Venue(
        name = request.form['name'],
        genres = request.form['genres'],
        address = request.form['address'],
        city = request.form['city'],
        state = request.form['state'],
        phone = request.form['phone'],
        website = request.form['website_link'],
        facebook_link = request.form['facebook_link'],
        seeking_talent = True if request.form.get('seeking_talent', False) else False,
        seeking_description = request.form['seeking_description'],
        image_link = request.form['image_link'],       
      )
      db.session.add(venue)
      db.session.commit()

      flash('Record with id ' + venue_id + ' updated successfully')

    except:
      flash('Error occured. Record with id ' + venue_id + ' failed to update')

    finally:
      return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  if request.method == 'POST':
    print(request.form)
    try:
      artist = Artist(
        name = request.form['name'],
        genres = request.form['genres'],
        #address = request.form['address'],
        city = request.form['city'],
        state = request.form['state'],
        phone = request.form['phone'],
        website = request.form['website_link'],
        facebook_link = request.form['facebook_link'],
        seeking_venue = True if request.form.get('seeking_venue', False) else False,
        seeking_description = request.form['seeking_description'],
        image_link = request.form['image_link'],
      )

      db.session.add(artist)
      db.session.commit()
      print("SUCCESSFUL")

      # on successful db insert, flash success
      flash('Artist ' + request.form['name'] + ' was successfully listed!')

    except:
      # TODO: on unsuccessful db insert, flash an error instead.
      # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
      flash('An error occurred. Artist ' + request.form['name'].name + ' could not be listed.')

    finally:
      return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.

  data = Show.query.all()
  
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead

  if request.method == 'POST':
    print(request.form)
    if True:
    #try:
      show = Show(
        venue_id = request.form['venue_id'],
        artist_id = request.form['artist_id'],
        start_time = request.form['start_time']
      )

      db.session.add(show)
      db.session.commit()

      # on successful db insert, flash success
      flash('Show was successfully listed!')

    #except:
      # TODO: on unsuccessful db insert, flash an error instead.
      # e.g., flash('An error occurred. Show could not be listed.')
      # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/

      flash('An error occurred. Show could not be listed.')

    #finally:
      return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''

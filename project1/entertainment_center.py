import media
import fresh_tomatoes
import imdb
import re
import requests

class ImdbInfo(object):
  def __init__(self, title_query):
    """Create the object that will be used to access the IMDb's database"""
    internet_archive = imdb.IMDb()
    self.title_query = title_query
    self.media = internet_archive.search_movie(self.title_query)[0]
    self.media_details = internet_archive.get_movie(self.media.movieID)

  def title(self):
    """method to return the title of the movie"""
    return self.media_details['canonical title']

  def cast(self):
    """method to return the first 3 cast members for the movie"""
    # retreive all cast members
    full_cast = self.media_details['cast']

    # set a list of only 3 cast members
    top_five_cast = full_cast[0:3]

    # populate return_list with cast member name and imdb person ID
    # This will be used to create url links underneath the cover poster
    return_list = []
    for person in top_five_cast:
      return_list.append({person['name']: person.personID})
    return return_list

  def summary(self):
    """method to return summary of movie"""
    return self.media_details.summary()

  def cover_url(self):
    """method to return cover url for movie"""
    return self.media_details['full-size cover url']

  def trailer(self):
    """method to return trailer url for movie"""
    # google uri does not allow for spaces and uses plus signs instead
    title_no_spaces = re.sub(" ", "+", self.title())

    # Issue url request of google query for the movie title trailer
    request = requests.get('https://www.google.com/search?q=%s+trailer' % title_no_spaces)

    # Parse the output from the google search looking for the youtube url
    # The response from the google request is a wall of text
    # This grabs the entire youtube url we need for the trailer url
    index_start = re.search(r'http://www.youtube.com/watch%3Fv%3D\w+', request.text).start()
    index_end = re.search(r'http://www.youtube.com/watch%3Fv%3D\w+', request.text).end()

    # Splice out the url
    trailer_url = request.text[index_start:index_end]
    # Decode url
    trailer_url_decoded = re.sub('%3Fv%3D', '?v=', trailer_url)

    return trailer_url_decoded

# Create Imdb movie objects
american_sniper = ImdbInfo("american sniper")
toy_story = ImdbInfo("toy story")
avatar = ImdbInfo("avatar")
twister = ImdbInfo("twister")
transformers = ImdbInfo("transformers 1")
ex_machina = ImdbInfo("ex machina")

# Create movie objects with information from Imdb
toy_story = media.Movie(
    toy_story.title(),
    toy_story.summary(),
    toy_story.cover_url(),
    toy_story.trailer(),
    toy_story.cast()
    )
avatar = media.Movie(
    avatar.title(),
    avatar.summary(),
    avatar.cover_url(),
    avatar.trailer(),
    avatar.cast()
    )
american_sniper = media.Movie(
    american_sniper.title(),
    american_sniper.summary(),
    american_sniper.cover_url(),
    american_sniper.trailer(),
    american_sniper.cast()
    )
twister = media.Movie(
    twister.title(),
    twister.summary(),
    twister.cover_url(),
    twister.trailer(),
    twister.cast()
    )
transformers = media.Movie(
    transformers.title(),
    transformers.summary(),
    transformers.cover_url(),
    transformers.trailer(),
    transformers.cast()
    )
ex_machina = media.Movie(
    ex_machina.title(),
    ex_machina.summary(),
    ex_machina.cover_url(),
    ex_machina.trailer(),
    ex_machina.cast())

#list of movie objects
movies = [twister, toy_story, avatar, transformers, ex_machina, american_sniper]

# Launch web browser with movies
fresh_tomatoes.open_movies_page(movies)

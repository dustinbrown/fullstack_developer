import webbrowser

class Movie():
  def __init__(self, title, storyline, poster_image, trailer, cast):
    self.title = title
    self.storyline = storyline
    self.poster_image_url = poster_image
    self.trailer_youtube_url = trailer
    self.cast = cast

  def show_trailer(self):
    """method to open webbrowser with trailer of movie"""
    webbrowser.open(self.trailer)


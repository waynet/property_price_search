# The Model - MVC
from django.db import models


class SavedSearchLink(models.Model):
    """ The model for Saved Search Links
    """
    # User's email, this is not entered by user, it came from
    # authenticated user object.
    email = models.EmailField()
    # The name of the save search link
    search_link_name = models.CharField(max_length=250)
    # The save search link itself
    search_links = models.URLField(max_length=500)

    def __str__(self) -> str:
        # return self.search_link_name
        return f'{self.search_link_name} - {self.search_links}'

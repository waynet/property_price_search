# The View - MVC
import random

from django.core import exceptions, validators
from django.template import loader, Context
from django.http import HttpResponse, HttpResponseRedirect

from .models import SavedSearchLink

def index(request):
    """The Home view serving the main search page
    """ 
    # Load the search index template from static folder
    template = loader.get_template('search/index.html')

    # return HTTP response
    return HttpResponse(template.render(request=request))


def save_search(request):
    """Save the search senarios created by user
    """
    # Authenticated user - save the search url
    if request.user.is_authenticated:
        if request.method == 'POST':
            ### Save to the db
            # get the search_url
            search_url = request.POST.get('search_url', '')
            # get user email, create a random number and save it as search url name
            email = request.user.email
            name = f"Saved Search query {random.randint(1, 100000000000000000)}"
            
            # Validate the search url
            try:
                validators.URLValidator(search_url)
            except:
                # Raise a silent error, user/hacker would not know what went wrong
                # but admin can check the server logs and see the exception of
                # ValidationError was thrown.
                raise exceptions.ValidationError(
                    "Something went wrong, please contact the adimistrator!"
                )
            
            # All good, save the data
            SavedSearchLink.objects.create(
                email=email, search_link_name=name, search_links=search_url
            )

            return HttpResponseRedirect('/admin/property_map/savedsearchlink/')
    
    # To catch all fail cases here
    # 1) user is not authenticated
    # 2) http request is not POST
    # 
    # Most important of all, this link is a hidden link, only logged in user can see it.
    # Unless someone is trying to scan/hack the web server???
    #
    # Again, this is a silent error, user/hacker wouldn't know what went wrong.
    # System admin can check the server logs and see the exception.
    raise exceptions.SuspiciousOperation(
        "Something went wrong, please contact the administrator!"
    )


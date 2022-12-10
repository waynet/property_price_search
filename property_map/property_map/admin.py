# Custom Django Admin application

from django import forms
from django.contrib import admin
from .models import SavedSearchLink


class SavedSearchLinkAdminForm(forms.ModelForm):
    def clean_name(self):
        # do something that validates your data
        return self.cleaned_data["name"]


class SavedSearchLinkAdmin(admin.ModelAdmin):
    # May just validate user input data before
    # reaching the database layer.
    # Data validation
    # form = SavedSearchLinkAdminForm
    
    # Do not show email field
    exclude = ('email',)

    def view_on_site(self, obj):
        """ A button that can redirect user back to the
            home page.
        """
        url = obj.search_links
        return url
    
    def get_queryset(self, request):
        """Return user saved links only
        """
        # Return the whole queryset
        qs = super().get_queryset(request)

        # If user is superuser, return all
        # if request.user.is_superuser:
        #    return qs
        
        # Only return user's own search links
        return qs.filter(email=request.user.email)
    
    def save_model(self, request, obj, form, change):
        """Given a model instance save it to the database.
        """
        # Save user's email too
        obj.email = request.user.email
        obj.save()

# Register SavedSearchLink with Admin application
admin.site.register(SavedSearchLink, SavedSearchLinkAdmin)

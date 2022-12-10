# Extended OIDCAuthenticationBackend
# Works with Google OAuth API

from mozilla_django_oidc.auth import OIDCAuthenticationBackend


class PropertyPriceSearchAuthenticationBackend(OIDCAuthenticationBackend):
    def create_user(self, claims):
        """ Override superclass create_user method to suit this application
        """
        # Create an user based on email address
        # Please note the system will ONLY save customer's email address
        # no other information is stored locally
        # username is a hash value based on the email address

        # Get user's email from token claims
        email = claims.get("email")
        # Create an hashed username based on email address, 
        username = self.get_username(claims)
        # Call Django user model to create the user.
        return self.UserModel.objects.create_superuser(username, email=email)

    def update_user(self, user, claims):
        """ Override superclass update_user method to suit this application
        """
        # Update user if not a staff or superuser, so that they can access
        # the admin area.
        if not user.is_staff or not user.is_superuser:
            user.is_staff = True
            user.is_superuser = True
            user.save()
        return user
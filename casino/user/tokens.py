# Import necessary modules
from django.contrib.auth.tokens import PasswordResetTokenGenerator  # For generating password reset tokens
import six  # For Python 2/3 compatibility

# Define a custom account activation token generator
class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    # Define the hash value for the token
    def _make_hash_value(self, user, timestamp):
        # Concatenate the user's primary key, timestamp, and account activation status
        return (
            six.text_type(user.pk) + six.text_type(timestamp) + six.text_type(user.is_active)
        )

# Create an instance of the custom account activation token generator
account_activation_token = AccountActivationTokenGenerator()


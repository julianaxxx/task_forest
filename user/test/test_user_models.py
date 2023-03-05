
import pytest
from django.core.exceptions import ValidationError
from user.models import User


@pytest.mark.django_db
def test_user_model():
    # Test creating a user with valid data
    user = User.objects.create(
        username='johndoe',
        email='johndoe@example.com',
        password='mysecretpassword',
    )
    assert user.pk is not None  # Check if user was saved to the database
    assert str(user) == 'johndoe'  # Check __str__ method

    # Test creating a user with invalid data
    with pytest.raises(ValidationError):
        User.objects.create(
            username='johndoe',
            email='invalid_email',  # Invalid email format
            password='',
        )

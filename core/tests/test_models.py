from core import models
from unittest.mock import patch
from django.contrib.auth import get_user_model
from django.test import TestCase
from decimal import Decimal

class ModelTests(TestCase):

    def create_user(self, email='test@londonappdev.com', password='test123'):
        return get_user_model().objects.create_user(email, password)
    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = 'test@londonappdev.com'
        password = 'Testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        email = 'test@LONDONAPPDEV.COM'
        user = get_user_model().objects.create_user(email, 'test123')

        self.assertEqual(user.email, email.lower())
    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_create_new_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'test@londonappdev.com',
            'test123'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
    
    def test_create_recipe(self):
        user=get_user_model().objects.create_user(
            'test@londonappdev.com',
            'test123'
        )
        """Test creating a recipe is successful"""
        recipe = models.Recipe.objects.create(
            title='Test recipe',
            #link='http://example.com/recipe',
            price=Decimal(5.00),
            #description='Test recipe description',
            time_minutes=5,
            user=user,
        )
        self.assertEqual(str(recipe), recipe.title)
    
    def test_tag_str(self):
        """Test the tag string representation"""
        user=get_user_model().objects.create_user( email='test@londonappdev.com', password='test123')
        tag = models.Tag.objects.create(
            user=user,
            name='Tag1'
        )

        self.assertEqual(str(tag), tag.name)
    
    def test_ingredient_str(self):
        """Test the ingredient string respresentation"""
        user = self.create_user()
        ingredient = models.Ingredient.objects.create(
            user=user,
            name='Cucumber'
        )

        self.assertEqual(str(ingredient), ingredient.name)
    @patch('uuid.uuid4')
    def test_recipe_file_name_uuid(self, mock_uuid):
        """Test that image is saved in the correct location"""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.recipe_image_file_path(None, 'myimage.jpg')

        exp_path = f'uploads/recipe/{uuid}.jpg'
        self.assertEqual(file_path, exp_path)
    

        
    
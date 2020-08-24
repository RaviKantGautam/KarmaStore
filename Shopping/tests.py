from django.test import TestCase
from .models import Comment
# Create your tests here.
class BasicTest(TestCase):
    def test_comment(self):
        data = Comment(commentbody='this is amazing',user_id=3,pid_id=2)
        data.save()
        print(data.id)
        print('mydata:----->',data)
        self.assertEqual(data.id,data.id)

from django.test import TestCase, Client
from django.contrib.auth.models import User
from links.models import Links, Tags


class MyTest(TestCase):
    def setUp(self):
        self.client = Client()

        tag = Tags(title='Первый')
        tag.save()

        user = User(username='admin', password='admin')
        user.save()
        user = User.objects.get(username='admin')

        links = Links(
            user=user,
            title="Заголовок1",
            description="Описание1",
            original_url="https://ya.ru/",
            short_url="e6Yn8i"
        )
        links.save()
        links.tags.create(title="Второй")
        links.tags.create(title="Третий")

    def test1(self):
        test = Tags.objects.get(title="Первый")
        self.assertEqual(test.title, 'Первый')

    def test2(self):
        link = Links.objects.get(title="Заголовок1")
        self.assertEqual(link.title, 'Заголовок1')

    def test3(self):
        link = Links.objects.get(short_url='e6Yn8i')
        self.assertEqual(link.user.username, 'admin')

    def test4(self):
        link = Links.objects.get(title='Заголовок1')
        response = self.client.get("/link/" + str(link.id))
        self.assertEqual(response.status_code, 200)

    def test5(self):
        response = self.client.get("/link/100500")
        self.assertEqual(response.status_code, 404)

    def test6(self):
        test = Links.objects.filter(original_url="https://ya.ru/")
        self.assertTrue(test.exists())
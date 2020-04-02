# General Workflow
manage.py -we will be able to start a web server and helps making apps
settings.py contains databases and the basic templates
python manage.py migrate will gives us a default database
manage.py runserver will deploy the server , we have to enter the IP address on the browser
Django admin helps modifying database easily
manage.py createsuperuser gives you the admin access ip/admin username Meghaa
We can add more admins after going on the dashboard
# Apps in Django
## How to create apps in Django?
python manage.py startapp CoronaNews
# Serialization
before sending data to clint we need to convert it to json\
python manage.py shell\
        >>>from CoronaNews.models import Article\
        >>> from CoronaNews.serializers import ArticleSerializer\
        >>> from rest_framework.renderers import JSONRenderer\
        >>> from  rest_framework.renderers import JSONRenderer\
        >>> from rest_framework.parsers import JSONParser\
        >>> a=Article(title='Name',author='Megha Agarwal',email='meghaa105@gmail.com')\
        >>> a.save() # calls the create function in the serializers.py file\
        >>> serializer=ArticleSerializer(a)\
        >>> serializer.data\
        {'title': 'Name', 'author': 'Megha Agarwal', 'email': 'meghaa105@gmail.com'}\
        >>> content = JSONRenderer().render\
        >>> content = JSONRenderer().render(serializer.data)\
        >>> content\
        b'{"title":"Name","author":"Megha Agarwal","email":"meghaa105@gmail.com"}'\
        >>> serializer = ArticleSerializer(Article.objects.all(),many=True)\
        >>> serializer.data\
        [OrderedDict([('title', 'Name'), ('author', 'Megha Agarwal'), ('email', 'meghaa105@gmail.com')]), Order\
        edDict([('title', 'Hello_World'), ('author', 'Megha Agarwal'), ('email', 'meghaa105@gmail.com')])]\



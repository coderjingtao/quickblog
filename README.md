## A Quick and Technical Blog with Django
This is an enry-level preject about personal blog for Django learner. The sparrow may be small, but fully-equipped.
### Features
- Quick development
- Suitable for beginner to learn Django
- Blog article support Markdown language and Code snippet highlighting, especially for tech bloggers.
- Quick and Easy Deploy
### Technologies
- Use template to reduce HTML codes redundancy
- Use template tags to deal with public components and codes
- Use abosulte url to generate URL on page
- Use Django form to generate HTML Form
- Defind class Meta in model to reduce redundancy of query codes in business layer 
- Automaticlly generate excerpt of article 
- Use Class Generic Views to redunce codes redundancy in views
- Customized effect of Django pagination
### Functions
- Articles 
    - Article list page
    - Article detail page
- Comments
    - Submit comments
    - Comment list page
- Category
    - Category list
    - Display the number of articles under each category
- Recent articles
- Tags
- Statistic number of Article Views
- Pagination
- RSS subscription
- Support automatic display of article contents of Markdown 

### Software Required
- Ubuntu 16.04
- Nginx
- Gunicorn

Nginx configuration
```
sudo vim /etc/nginx/sites-enabled/default 

server {
    charset utf-8;
    listen 80;
    server_name jing.cf;

    location /static {
        alias /home/google/sites/jing.cf/quickblog/static; 
    }

    location / {
        proxy_set_header Host $host;
        proxy_pass http://unix:/tmp/jing.cf.socket;
        # proxy_pass http://127.0.0.1:8000
    }
}
```


### Deploy Steps
1. Connect your remote cloud server, enter into your website directory and activate virtual environment

```
google@myblog:~/sites/jing.cf$ source env/bin/activate
```

2. Pull the latest project codes from github under your project directory

```
# first time
git clone https://github.com/coderjingtao/quickblog.git

# daily update
(env) google@myblog:~/sites/jing.cf/quickblog$ git pull

```

3. Install new requirements if your project have referenced new third-party libs

```
(env) google@myblog:~/sites/jing.cf/quickblog$ pip install -r requirements.txt
```

4. Collect static files if the static files have changed.

```
(env) google@myblog:~/sites/jing.cf/quickblog$ python manage.py collectstatic
```

5. Migrate database if the database structure have changed.

```
(env) google@myblog:~/sites/jing.cf/quickblog$ python manage.py migrate
```
6. Restart Nginx and Gunicorn

```
sudo service nginx reload

gunicorn --bind unix:/tmp/jing.cf.socket mysite.wsgi:application

# gunicorn --bind 127.0.0.1:8000 mysite.wsgi:application
```
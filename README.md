Clone https://github.com/tkhutunishvili/REST-API-Flask.git repository.

Run Flask
 1. cd Flask
 2. python3 app.py

Connect to App using Postman # download link https://www.postman.com/downloads/
 1. To register go to http://127.0.0.1:5000/register select POST method from drop down menu and pass username/password:
 	{
    "username": "user",
    "password": "pass"

	}
 2. Go to login page http://127.0.0.1:5000/login, select POST method from drop down menu and pass username/password, you'll get token:
 	{
    "username": "user",
    "password": "pass"

	}
 3. To list animal select Get method and pass token to http://127.0.0.1:5000/animals/98?x-access-token={token} 
 4. Animal can be added by going to http://127.0.0.1:5000/animals select POST method and pass:
 	{
	    "centerid": 1,
	    "name": "name",
	    "description": "pet",
	    "age": 3,
	    "species": "specie",
	    "price": 1
	}
 5. Animal data can be updated on: http://127.0.0.1:5000/animals/{centerid}, replace centerid with animal id, select PUT and don't forget to pass token.
 6. Delete animal here: http://127.0.0.1:5000/delete/{centerid}, replace centerid with animal id, select DELETE and don't forget to pass token.
 7. User removal link: http://127.0.0.1:5000/remove/user, keep in mind to select DELETE from drop down menu.
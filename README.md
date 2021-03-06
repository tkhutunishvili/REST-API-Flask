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
	![register](screenshots/register.png)
 2. Go to login page http://127.0.0.1:5000/login, select POST method from drop down menu and pass username/password, you'll get token:
 	{
    "username": "user",
    "password": "pass"

	}
	![token](screenshots/token.png)
 3. Animal can be added by going to http://127.0.0.1:5000/animals select POST method and pass:
 	{
	    "centerid": 1,
	    "name": "name",
	    "description": "pet",
	    "age": 3,
	    "species": "specie",
	    "price": 1
	}
	![add_animal](screenshots/add_animal.png)
 4. To list animal select Get method and pass token to http://127.0.0.1:5000/animals/98 
	![find_animal](screenshots/find_animal.png)
 5. Animal data can be updated on: http://127.0.0.1:5000/animals/{centerid}, replace centerid with animal id, select PUT and don't forget to pass token.
	![update_animal](screenshots/update_animal.png)
 6. Delete animal here: http://127.0.0.1:5000/animals/{centerid}, replace centerid with animal id, select DELETE and don't forget to pass token.
	![delete_animal](screenshots/delete_animal.png)
 7. User removal link: http://127.0.0.1:5000/remove/user, keep in mind to select DELETE from drop down menu.
 	![remove_user](screenshots/remove_user.png)
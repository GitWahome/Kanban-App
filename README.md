# Kanban Flow
This is a simple Kanban app making use of Flask(And a couple of other flask modules and sqlite)
I have included a database that contains the correct table structure for the app's data storage.
## Installation

To use this template, your computer needs:
- [Python 2 or 3](https://python.org)
- [Pip Package Manager](https://pypi.python.org/pypi)

### Running the app
First of all install all dependancies from the requirements.txt file this way:
```bash
pip install -r requirements.txt
```
You do not have to set up a database as I have included a functional one for you in the app(kanbanapp.db)
But incase you want to set up you own, you can do so this way
```bash
sqlite3 kanbanapp.db

```
##CTRL-C to quit the sqlite3 terminal.
##Launch python terminal
```bash
python
```
```bash
from app import db
db.creae_all()
exit()
```
#Quit the python terminal using ctrl-c or exit()
#Then you can launch the app this way.
```bash
python app.py
```
##You will get out put as follows
```bash
C:\Program Files (x86)\Python36-32\lib\site-packages\flask_sqlalchemy\__init__.py:794: FSADeprecationWarning: SQLALCHEMY_TRACK_MODIFICATIONS adds significant overhead and will be disabled by default in the future.  Set it to True or False to suppress this warning.
  'SQLALCHEMY_TRACK_MODIFICATIONS adds significant overhead and '
 * Restarting with stat
C:\Program Files (x86)\Python36-32\lib\site-packages\flask_sqlalchemy\__init__.py:794: FSADeprecationWarning: SQLALCHEMY_TRACK_MODIFICATIONS adds significant overhead and will be disabled by default in the future.  Set it to True or False to suppress this warning.
  'SQLALCHEMY_TRACK_MODIFICATIONS adds significant overhead and '
 * Debugger is active!
 * Debugger PIN: 151-384-950
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```
##
##You can then launch the app from
```bash
http://127.0.0.1:5000/
``` 
##You can run unittests, run the following commands.
##You can add more tests in the test.py file
```bash
python tests.py
```


You will notice that as JSON API is included in the build. You can add multiple tasks enmass in the Upload JSON section:
You can also download your Data in JSON format below the dahsboard.
The following is an example of valid JSON data that can be processed by the app to add your tasks.
The format is that of a dictionary and is very intuitive.
```bash
{"1": {'title': 'Entry 1', 'body': 'This is the description for the first entry', 'category': 'TODO'},
"2": {'title': 'Entry 2', 'body': 'This is the description for the second entry', 'category': 'DOING'},
"3": {'title': 'Entry 3', 'body': 'This is the description for the third entry', 'category': 'DONE'}}
```

#NOTES:
Given the model I used, the articles are the tasks. 
The whole application is an extensive modification of the article built by traversity media in their intro to flask. 
They make use of mysql but I modified the system to make it work for me. The Kanban layout too is a modification of the 
linkedLayout on Codepen.
The following Links will get you to these:

##News App in FLASK:
https://www.youtube.com/watch?v=zRwy8gtgJ1A&list=PLillGF-RfqbbbPz6GSEM9hLQObuQjNoj_

##Simple KANBAN.
https://codepen.io/Aniboaz/pen/vKOXPa

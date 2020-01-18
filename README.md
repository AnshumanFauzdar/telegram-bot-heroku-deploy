# Intial Deploy to heroku
Intially I was not able to push a simple bot to heroku, but yeah googling a lot made it work!

### Step 1:
- Create your bot like we have bot.py and write any python code that is intially working on your local machine!
### Step 2:
- Make a folder like *telegram-bot* and put *bot.py* in the folder
### Step 3:
- Make a blank python file named 
   ```python
   __init__.py
### Step 4:
- Make a *Procfile* this should be without any extension like .txt, you can go to view -> tick file name extensions and remove any extension
   ```python
   worker: python bot.py
- Write this in Procfile by using notepad or any editor of your choice! Here bot.py is your python code!
### Step 5:
- Now we have to make a *requirements.txt* through which heroku will install the dependencies to make our bot work!
- What to add in requirements.txt
  - Mine looks like this:
  ```python
  future>=0.16.0
  certifi
  tornado>=5.1
  cryptography
  python-telegram-bot
 
 Add anything which you have included in the python code!

### Step 6:
- Change directory to where you have made these files
- now in git bash CLI, intialize a git
  ```python
  git init
  
### Step 7:
- Now install heroku CLI
- Next
  ```python
  heroku login
  heroku create app_name
- If you have already created app then select it:
  ```python
  heroku git:remote -a app_pname
- Or else continue:
  ```python
  git add -f bot.py Procfile requirements.txt __init__.py
- ```python
  git commit -m "Added Files"
- Push files to heroku:
  ```python
  git push heroku master
- If it is not working then try this one:
   ```python
   git push heroku master --force
### At this point your bot should be running, you can check by
-  ```python
    heroku ps
If it is not running then we have to reset dynos:
- ```python
  heroku ps:scale worker=0
- ```python
  heroku ps:scale worker=1
Now it should be running fine! Enjoy :)  
  

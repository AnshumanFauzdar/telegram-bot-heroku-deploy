# Intial Deploy to heroku
Intially I was not able to push a simple bot to heroku, but yeah googling a lot made it work!

## Very Initial Steps [NOOB Steps]
1. Install Telegram :)
2. Create a telegram bot by talking to [Bot Father](https://t.me/botfather)
3. Install python in your computer, if you are on windows follow [this](https://www.python.org/downloads/windows/)
4. Install git, follow [this](https://git-scm.com/download/win)
5. Install Heroku account [here](https://signup.heroku.com/login)
6. Install Heroku CLI from [here](https://devcenter.heroku.com/articles/heroku-cli)
7. Install editor of your choice, I preffer [Atom](https://atom.io)

### Step 0 [Optional]:

- Just git clone this repository and start working by editing the code
   ```shell
   git clone https://github.com/AnshumanFauzdar/telegram-bot-heroku-deploy.git
   cd telegram-bot-heroku-deploy
- Or follow steps below!   
   
### Step 1:

- Create your bot like we have bot.py and write any python code that is intially working on your local machine!
### Step 2:

- Make a folder like *telegram-bot* and put *bot.py* in the folder
### Step 3:

- Make a blank python file named 
   ```shell
   __init__.py
### Step 4:

- Make a *Procfile* this should be without any extension like .txt, you can go to view -> tick file name extensions and remove any extension
   ```shell
   worker: python bot.py
- Write this in Procfile by using notepad or any editor of your choice! Here bot.py is your python code!
### Step 5:

- Now we have to make a *requirements.txt* through which heroku will install the dependencies to make our bot work!
- What to add in requirements.txt
  - Mine looks like this:
  ```shell
  future>=0.16.0
  certifi
  tornado>=5.1
  cryptography
  python-telegram-bot
 
 Add anything which you have included in the python code!

### Step 6:
- Change directory to where you have made these files
- now in git bash CLI, intialize a git
  ```shell
  git init
  
### Step 7:
- Now install heroku CLI
- Next
  ```shell
  heroku login
  heroku create app_name
- If you have already created app then select it:
  ```shell
  heroku git:remote -a app_name
- Or else continue:
  ```shell
  git add -f bot.py Procfile requirements.txt __init__.py
- ```shell
  git commit -m "Added Files"
- Push files to heroku:
  ```shell
  git push heroku master
- If it is not working then try this one:
   ```shell
   git push heroku master --force
### At this point your bot should be running, you can check by
-  ```shell
    heroku ps
If it is not running then we have to reset dynos:
- ```shell
  heroku ps:scale worker=0
- ```shell
  heroku ps:scale worker=1
Now it should be running fine! Enjoy :)  

### If you are trying to lazy which you should not! (Deploying to Heroku)

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/AnshumanFauzdar/telegram-bot-heroku-deploy/blob/master)

Choose App name and deploy!
Follow from Step 7 and edit bot.py with your token!
And finally deploy!

### Want a video tutorial?
- Check It [Here!](https://github.com/AnshumanFauzdar/telegram-bot-heroku-deploy/issues/1)

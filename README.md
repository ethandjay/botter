# botter
Generate bot tweets for any user on Twitter from command line, as easy as pie:

1. Register botter as an app with your Twitter account
2. Create a config.py file in this directory with this information:
**LOAD OAUTH SETTINGS**  
Assumes Twitter OAuth settings, saved in a file
called OAuthSettings.py, saved in the following format:
	
    settings = {
      'consumer_key': 'xxxx',
      'consumer_secret': 'xxxx',
      'access_token_key': 'xxxx',
      'access_token_secret': 'xxxx'
    }
  
3. Have fun!

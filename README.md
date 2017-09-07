# botter
Generate bot tweets for any user on Twitter from command line, as easy as pie:

1. Register an app with your Twitter account
2. Create a config.py file in this directory with this information:

config.py:

    settings = {
      'consumer_key': 'xxxx',
      'consumer_secret': 'xxxx',
      'access_token_key': 'xxxx',
      'access_token_secret': 'xxxx'
    }

**Requires**: markovify, requests
**Usage**: python botter.py [Twitter handle (no @)]

**Have fun!**
import newspaper

# I'm not a bad guy. :-)
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'

config = newspaper.Config()
config.browser_user_agent = USER_AGENT
config.fetch_images = False


LOCALPOSTSERVER=True

#DATABASE settings
dbname = 'doomdbase'
user = 'doomd'
passw = 'doomdpsw'
dbase_init = f"dbname={dbname} user={user} password={passw} host=127.0.0.1"

#doomd/ddws/doomday/settings.py post registration sensitive parameters:
if LOCALPOSTSERVER:
    # run local server in a seperate window:
    # python3 -m smtpd -n -c DebuggingServer localhost:1025
    EMAIL_HOST = "localhost"
    EMAIL_USE_TLS = False
    EMAIL_PORT = 1025
    EMAIL_HOST_USER = None
    EMAIL_HOST_PASSWORD = None
else:
    #OUTER email password reset - link in the postbox:
    EMAIL_HOST = "smtp.mailgun.org"
    EMAIL_USE_TLS = True
    EMAIL_PORT = 587
    EMAIL_HOST_USER = 'postmaster@sandbox0e9e5873433049548eea568a33f7aa82.mailgun.org'    #os.environ.get("EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = "062454629376209991b96979c6317348-e438c741-f10739da"            #os.environ.get("EPSW")

SOCIAL_AUTH_GITHUB_KEY = "4e1a869be0aaa4fdf773"
SOCIAL_AUTH_GITHUB_SECRET = "82adeb072cb9eaa30ad0571efca96ed8d5c6c87a"


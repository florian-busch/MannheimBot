import os
from dotenv import load_dotenv
from mastodon import Mastodon
from createMastodonPosts import buildStatus

load_dotenv()

#create app
try:
    Mastodon.create_app(
        'MannheimBot',
        api_base_url = 'https://mas.to',
        to_file = 'mannheimBot_clientcred.secret'
    )
except:
    print("Error Mastodon.create_app")


try:
    mastodon = Mastodon(client_id = 'mannheimBot_clientcred.secret',)
    mastodon.log_in(
        os.getenv('user_email'),
        os.getenv('user_password'),
        to_file = 'mannheimBot_usercred.secret'
    )

    mastodon.access_token = mastodon.log_in (
        username = os.getenv('user_email'),
        password = os.getenv('user_password'),
        scopes=['read', 'write']
    )
except:
    print("Error loging in")


content = buildStatus()
mastodon.toot(content)


exit()


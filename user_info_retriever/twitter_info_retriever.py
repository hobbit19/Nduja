import json
from dao.personal_info import PersonalInfo
from user_info_retriever.abs_personal_info_retriever \
    import PersonalInfoRetriever
from twython import Twython


class TwitterInfoRetriever(PersonalInfoRetriever):
    twitter = None

    def setToken(app_key, app_secret, oauth_token, oauth_token_secret):
        if TwitterInfoRetriever.twitter is None:
            TwitterInfoRetriever.twitter = Twython(app_key, app_secret,
                                                   oauth_token,
                                                   oauth_token_secret)

    def formatURL(self, username):
        if (username is None):
            TwitterInfoRetriever.twitter.show_user(screen_name=username)
        else:
            return None

    def retrieveInfo(self, usernames):
        results = []
        [results.append(self.formatURL(username)) for username in usernames]
        return None

    def parseResults(self, results):
        infos = []
        for rx in results:
            if rx is not None:
                infos.append(PersonalInfo(rx["name"], rx["url"], "",
                                          json.dumps(rx)))
            else:
                infos.append(None)
        return infos

# TwitterInfoRetriever.setToken(
#     app_key="",
#     app_secret="",
#     oauth_token="",
#     oauth_token_secret="")
# print(TwitterInfoRetriever().retrieveInfo('asgadhghdfha'))

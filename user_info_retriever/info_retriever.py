import logging

from db.db_manager import DbManager
from user_info_retriever.bitbucket_info_retriever import BitbucketInfoRetriever
from user_info_retriever.github_info_retriever import GithubInfoRetriever
from user_info_retriever.twitter_info_retriever import TwitterInfoRetriever


class InfoRetriever:
    tokens = None

    def setTokens(tokens):
        try:
            GithubInfoRetriever.setToken(tokens['tokens']['github'])
        except KeyError:
            pass
        try:
            TwitterInfoRetriever.setToken(tokens)
        except KeyError:
            pass

    def retrieveInfoForAccountSaved(self):
        db = DbManager.getInstance()
        accounts = db.getAllAccounts()
        githubs = []
        bitbuckets = []
        twitters = []
        for account in accounts:
            if account.info is None:
                if "github" in account.host:
                    githubs.append(account)
                elif "bitbucket" in account.host:
                    bitbuckets.append(account)
                elif "twitter" in account.host:
                    twitters.append(account)
                else:
                    logging.warning(account.host + " not yet supported.")
        infos = []
        if len(githubs) > 0:
            infos = infos + GithubInfoRetriever().retrieveInfo(githubs)
        if len(bitbuckets) > 0:
            infos = infos + BitbucketInfoRetriever().retrieveInfo(bitbuckets)
        if len(twitters) > 0:
            infos = infos + TwitterInfoRetriever().retrieveInfo(twitters)
        accounts = []
        accounts = accounts + githubs + bitbuckets + twitters
        acc_infos = zip(accounts, infos)
        db.initConnection()
        for (account, info) in acc_infos:
            if info is not None:
                infoId = (db.insertInformation(info.name, info.website,
                                               info.email, info.json))
                db.addInfoToAccount(account.ID, infoId)
        db.saveChanges()

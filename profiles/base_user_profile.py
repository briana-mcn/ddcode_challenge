class UserProfile:
    """
    This class retrieves the required data pertinent for the code challenge and builds
    an appropriate response dictionary with the required
    """
    # this is not the best implementation as it's not clearly indicative of the state of the program.
    # a subclass could inherit this class, expecting the 'retrieved_data' dictionary to be identical,
    # but it could be out of sync if somewhere else in the program child classes were manipulating this dict
    retrieved_data = {
        "repos": {
            "original": {
                "names": [],
                "count": 0,
                "repo_watchers": 0,
                "commit_count": 0
            },
            "forked": {
                "names": [],
                "count": 0
            }
        },
        "open_issues_count": 0,
        "account_size": 0,
        "languages": {
            "names": [],
            "count": 0
        },
        "reputation": {
            "followers": 0,
            "following": 0
        },
        "stars": {
            "given": 0,
            "received": 0
        },
        "repo_topics": {
            "names": [],
            "count": 0
        }
    }

    def calculate_languages(self):
        self.retrieved_data['languages']['names'] = list(
            {lang.lower() for lang in self.retrieved_data['languages']['names']}
        )
        self.retrieved_data['languages']['count'] = len(self.retrieved_data['languages']['names'])

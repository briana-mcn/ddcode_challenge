class UserProfile:
    """
    This class retrieves the required data pertinent for the code challenge and builds
    an appropriate response dictionary with the required
    """
    def __init__(self):
        self.retrieved_data = {
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

    def calculate_total_profile_data(self):
        self.calculate_languages()
        self.retrieved_data['repos']['original']['count'] = len(
            self.retrieved_data['repos']['original']['names'])
        self.retrieved_data['repos']['forked']['count'] = len(
            self.retrieved_data['repos']['forked']['names']
        )
        return self.retrieved_data

    def calculate_languages(self):
        languages = set(self.retrieved_data['languages']['names'])
        self.retrieved_data['languages']['names'] = languages
        self.retrieved_data['languages']['count'] = len(languages)


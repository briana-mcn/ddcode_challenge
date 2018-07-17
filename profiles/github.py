from clients.github_client import GitHubClient
from profiles.base_user_profile import UserProfile


class GitHubProfile(UserProfile):
    def __init__(self, user):
        super(GitHubProfile, self).__init__()
        self.client = GitHubClient(user)
        self.original_repo_names = []
        self.all_repos_names = []

    def build_github_profile(self):
        """
        Delegates tasks to extract data from GitHub API endpoints
        :return:
        """
        # retrieve repository data
        repo_data = self.client.get_user_repo_data()
        self.parse_repo_data(repo_data)

        # retrieve data from the profile api
        profile_data = self.client.get_user_profile_data()
        self.retrieved_data['reputation']['followers'] += profile_data['followers']
        self.retrieved_data['reputation']['following'] += profile_data['following']

        # retrieve starred data and append to primary dictionary
        stars_given = self.client.get_user_starred_repository()
        self.retrieved_data['stars']['given'] += stars_given

        # get the number of commits for each repo
        commit_count = self.client.get_user_commits(self.original_repo_names)
        self.retrieved_data['repos']['original']['commit_count'] += commit_count
        # get the topics for each repo
        topics = self.client.get_repo_topics(self.original_repo_names)
        self.retrieved_data['repo_topics']['names'].extend(topics)
        self.retrieved_data['repo_topics']['count'] += len(topics)
        # add languages with no duplicates
        languages = self.client.get_repo_languages(self.all_repos_names)
        if languages:
            all_languages = self.retrieved_data['languages']['names'].extend(
                set([k for lang in languages for k, v in lang.items() if lang])
            )
            self.retrieved_data['languages']['count'] += len(all_languages)

        return self.retrieved_data

    def parse_repo_data(self, data):
        """Parses the JSON data from the call to GitHubs' Repositories API.

        Data parsed includes:
        - total number of original repos
        - total number of forked repos
        - total watchers on original repos
        - total number of stars received on original repos
        - total number of open issues on original repos
        - size of account

        :param data: All repositories forked or created by user
        :type data: list of dicts
        """
        forked_count = 0
        original_count = 0
        for repo in data:
            # add all repos names for other functions use
            self.all_repos_names.append(repo['name'])
            self.retrieved_data['account_size'] += repo['size']
            self.retrieved_data['stars']['received'] += repo['stargazers_count']
            self.retrieved_data['open_issues_count'] += repo['open_issues_count']
            # forked count
            if repo['fork'] is True:
                forked_count += 1
                self.retrieved_data['repos']['forked']['names'].append(repo['name'])
            # append name of repo for eventual calls to get commit history
            if repo['fork'] is False:
                original_count += 1
                # class variable for making other calls with the repos names
                self.original_repo_names.append(repo['name'])
                self.retrieved_data['repos']['original']['names'].append(repo['name'])
                self.retrieved_data['repos']['original']['repo_watchers'] += repo['watchers_count']
        self.retrieved_data['repos']['original']['count'] += original_count
        self.retrieved_data['repos']['forked']['count'] += forked_count

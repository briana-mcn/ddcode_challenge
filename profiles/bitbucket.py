from clients.bitbucket_client import BitBucketClient
from profiles.base_user_profile import UserProfile


class BitBucketProfile(UserProfile):
    def __init__(self, resource, resource_type='teams'):
        super(BitBucketProfile, self).__init__()
        self.client = BitBucketClient(resource, resource_type)
        self.all_repos_names = []
        self.original_repos = []

    def build_bitbucket_profile(self):
        # followers
        followers = self.client.get_followers()
        self.retrieved_data['reputation']['followers'] += followers['size']
        # following
        following = self.client.get_followings()
        self.retrieved_data['reputation']['following'] += following['size']
        # parse repositories
        repo_objects = self.client.get_repository_data()
        self.parse_repository_data(repo_objects)
        # get commit count
        commits = self.client.get_repo_commits(self.original_repos)
        self.retrieved_data['repos']['original']['commit_count'] += commits['count']
        # get watchers
        watchers = self.client.get_repo_watchers(self.all_repos_names)
        self.retrieved_data['repos']['original']['repo_watchers'] += watchers['count']
        # get issue count
        issues = self.client.get_repo_issues(self.original_repos)
        self.retrieved_data['open_issues_count'] += issues['count']

    def parse_repository_data(self, repos):
        languages = set()
        forked = []
        originals = []
        size = 0
        for repo in repos:
            # get all repo names
            languages.add(repo['language'].lower())
            # get all repos size
            size += repo['size']
            # determine if repo is forked
            if repo.get('parent'):
                forked.append(repo['slug'])
            else:
                originals.append(repo['slug'])

        self.retrieved_data['languages']['names'].append(languages)
        self.retrieved_data['repos']['original']['names'].extend(originals)
        self.retrieved_data['repos']['forked']['names'].extend(forked)
        self.retrieved_data['account_size'] += size
        self.all_repos_names.extend(forked)
        self.all_repos_names.extend(originals)
        self.original_repos.extend(originals)

from unittest import TestCase

from profiles.github import GitHubProfile


class GHProfileParseRepoDataTestCase(TestCase):
    def setUp(self):
        self.profile = GitHubProfile('user')
        self.test_repos = [
            {
                "name": 'Repo1',
                "private": False,
                "fork": False,
                "size": 10,
                "stargazers_count": 8,
                "watchers_count": 2,
                "language": "Python",
                "open_issues_count": 3
            },
            {
                "name": 'Repo2',
                "private": False,
                "fork": True,
                "size": 20,
                "stargazers_count": 2,
                "watchers_count": 4,
                "language": "Ruby",
                "open_issues_count": 3,
            },
            {
                "name": 'Repo3',
                "private": False,
                "fork": True,
                "size": 5,
                "stargazers_count": 2,
                "watchers_count": 3,
                "language": "Python",
                "open_issues_count": 3,
            },
        ]

    def test_forked_repo_adds_items_to_dict(self):
        self.profile.parse_repo_data(self.test_repos)

        self.assertCountEqual(self.profile.retrieved_data['repos']['forked']['names'], ['Repo2', 'Repo3'])

    def test_original_repo_creates_attributes(self):
        self.profile.parse_repo_data(self.test_repos)

        self.assertCountEqual(self.profile.retrieved_data['repos']['original']['names'], ['Repo1'])
        self.assertCountEqual(self.profile.original_repo_names, ['Repo1'])

    def test_original_and_forked_attribute_setting(self):
        self.profile.parse_repo_data(self.test_repos)

        self.assertEqual(self.profile.retrieved_data['account_size'], 35)
        self.assertCountEqual(self.profile.retrieved_data['languages']['names'], ['python', 'ruby'])
        self.assertEqual(self.profile.retrieved_data['languages']['count'], 2)
        self.assertEqual(self.profile.retrieved_data['stars']['received'], 12)
        self.assertEqual(self.profile.retrieved_data['follower_count'], 9)
        self.assertEqual(self.profile.retrieved_data['open_issues_count'], 9)
        self.assertEqual(self.profile.retrieved_data['repos']['original']['count'], 1)
        self.assertEqual(self.profile.retrieved_data['repos']['forked']['count'], 2)


class GHProfileSetDictionary(TestCase):
    def test_sets_retrieved_data_dict_values(self):
        self.profile = GitHubProfile('test')

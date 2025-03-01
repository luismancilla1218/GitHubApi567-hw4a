import unittest
from unittest.mock import patch, Mock
from github_api import get_repos, get_commits, get_repos_and_commits, print_repos_and_commits

class TestGitHubAPI(unittest.TestCase):
    
    @patch('github_api.requests.get')
    def test_get_repos(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = '[{"name": "repo1"}, {"name": "repo2"}]'
        mock_get.return_value = mock_response
        
        result = get_repos('testuser')
        self.assertEqual(result, ['repo1', 'repo2'])
    
    @patch('github_api.requests.get')
    def test_get_repos_not_found(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        
        with self.assertRaises(ValueError):
            get_repos('nonexistentuser')
    
    def test_get_repos_empty_input(self):
        with self.assertRaises(ValueError):
            get_repos('')
    
    @patch('github_api.requests.get')
    def test_get_commits(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = '[{"commit": "1"}, {"commit": "2"}, {"commit": "3"}]'
        mock_get.return_value = mock_response
        
        result = get_commits('testuser', 'testrepo')
        self.assertEqual(result, 3)
    
    @patch('github_api.requests.get')
    def test_get_commits_not_found(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        
        with self.assertRaises(ValueError):
            get_commits('testuser', 'nonexistentrepo')
    
    def test_get_commits_empty_input(self):
        with self.assertRaises(ValueError):
            get_commits('', 'repo')
        with self.assertRaises(ValueError):
            get_commits('user', '')
    
    @patch('github_api.get_repos')
    @patch('github_api.get_commits')
    def test_get_repos_and_commits(self, mock_get_commits, mock_get_repos):
        mock_get_repos.return_value = ['repo1', 'repo2']
        mock_get_commits.side_effect = [10, 20]
        
        result = get_repos_and_commits('testuser')
        self.assertEqual(result, [('repo1', 10), ('repo2', 20)])
    
    @patch('github_api.get_repos')
    @patch('github_api.get_commits')
    def test_get_repos_and_commits_with_error(self, mock_get_commits, mock_get_repos):
        mock_get_repos.return_value = ['repo1', 'repo2']
        mock_get_commits.side_effect = [10, ValueError("Error")]
        
        result = get_repos_and_commits('testuser')
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], ('repo1', 10))
        self.assertEqual(result[1][0], 'repo2')
    
    @patch('github_api.get_repos_and_commits')
    def test_print_repos_and_commits(self, mock_get_repos_and_commits):
        mock_get_repos_and_commits.return_value = [('repo1', 10), ('repo2', 20)]
        
        result = print_repos_and_commits('testuser')
        expected = "Repo: repo1 Number of commits: 10\nRepo: repo2 Number of commits: 20"
        self.assertEqual(result, expected)
    
    @patch('github_api.get_repos_and_commits')
    def test_print_repos_and_commits_empty(self, mock_get_repos_and_commits):
        mock_get_repos_and_commits.return_value = []
        
        result = print_repos_and_commits('testuser')
        self.assertEqual(result, "No repositories found")
    
    @patch('github_api.get_repos_and_commits')
    def test_print_repos_and_commits_error(self, mock_get_repos_and_commits):
        mock_get_repos_and_commits.side_effect = ValueError("Error")
        
        result = print_repos_and_commits('testuser')
        self.assertTrue("Error" in result)

if __name__ == '__main__':
    unittest.main()

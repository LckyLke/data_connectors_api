from github import Github, Auth
from github.GithubException import GithubException
import time
from data_connectors_api.config import GITHUB_TOKEN

class GitHubAPIClient:
    
    def __init__(self, owner, repo_name, token=GITHUB_TOKEN):
        """
        Initialize the fetcher with repository details and token
        
        :param owner: Repository owner username
        :param repo_name: Repository name
        :param token: GitHub personal access token (for rate limits)
        """
        self.owner = owner
        self.repo_name = repo_name
        self.token = token
        
        auth = Auth.Token(token) if token else None
        self.github = Github(auth=auth)
        self.repo = self.github.get_repo(f"{owner}/{repo_name}")

    def _handle_rate_limit(self):
        rate_limit = self.github.get_rate_limit()
        if rate_limit.core.remaining == 0:
            reset_time = rate_limit.core.reset
            sleep_time = reset_time - time.time() + 10  # Add buffer
            print(f"Rate limit exceeded. Sleeping for {sleep_time} seconds")
            time.sleep(max(sleep_time, 0))

    def get_basic_info(self):
        """Get core repository metadata"""
        return self.repo.raw_data

    def get_community_info(self):
        """Get community profile information"""
        return {
            'stargazers': self.repo.stargazers_count,
            'forks': self.repo.forks_count,
            'subscribers': self.repo.subscribers_count,
            'topics': self.repo.get_topics(),
            'contributors': [c.raw_data for c in self.repo.get_contributors()],
        }

    def get_code_data(self):
        """Fetch code-related information"""
        self._handle_rate_limit()
        return {
            'branches': [b.raw_data for b in self.repo.get_branches()],
            'tags': [t.raw_data for t in self.repo.get_tags()],
            'commits': [c.raw_data for c in self.repo.get_commits()],
            'languages': self.repo.get_languages(),
            'readme': self.repo.get_readme().raw_data if self.repo.get_readme() else None,
            'license': self.repo.get_license().raw_data if self.repo.license else None,
        }

    def get_activity_data(self):
        """Fetch repository activity information"""
        self._handle_rate_limit()
        return {
            'issues': [i.raw_data for i in self.repo.get_issues(state='all') if not i.pull_request],
            'pull_requests': [pr.raw_data for pr in self.repo.get_pulls(state='all')],
            'releases': [r.raw_data for r in self.repo.get_releases()],
            'milestones': [m.raw_data for m in self.repo.get_milestones()],
        }

    def get_statistical_data(self):
        """Fetch statistical information"""
        self._handle_rate_limit()
        return {
            'code_frequency': self.repo.get_stats_code_frequency(),
            'commit_activity': self.repo.get_stats_commit_activity(),
            'contributor_stats': self.repo.get_stats_contributors(),
            'participation': self.repo.get_stats_participation(),
        }

    def get_additional_info(self):
        """Fetch supplementary repository information"""
        return {
            'workflows': [w.raw_data for w in self.repo.get_workflows()],
            'events': [e.raw_data for e in self.repo.get_events()],
            'traffic': {
                'views': self.repo.get_views_traffic(),
                'clones': self.repo.get_clones_traffic(),
            },
        }

    def fetch_all_data(self):
        """
        Aggregates all available repository data into a single dictionary
        
        Note: This may make dozens of API calls and take significant time
        """
        return {
            'basic_info': self.get_basic_info(),
            'community_info': self.get_community_info(),
            'code_data': self.get_code_data(),
            'activity_data': self.get_activity_data(),
            'statistical_data': self.get_statistical_data(),
            'additional_info': self.get_additional_info(),
        }

from data_connectors_api.github_api import GitHubAPIClient

client = GitHubAPIClient(owner="dice-group", repo_name="Ontolearn")

print(client.get_basic_info()) 


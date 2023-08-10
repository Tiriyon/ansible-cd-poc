
import os
import time
import requests
import base64
import yaml

def read_vars_file(decoded_content):
    vars_dict = {}
    for line in decoded_content.splitlines():
        if '=' in line:
            key, value = line.split('=', 1)  # Split on the first '='
            vars_dict[key.strip()] = value.strip()
    return vars_dict

def fetch_repositories(access_token, github_username):
    # Fetch repository names using GitHub API search endpoint
    url = f'https://api.github.com/search/repositories?q=user:{github_username}'
    headers = {'Authorization': f'token {access_token}'}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception if the request is not successful
        search_results = response.json()
        return search_results['items']
    except requests.exceptions.RequestException as e:
        print(f"Error fetching repositories: {e}")
        return []

def main():
    # Read GitHub username and access token from environment variables
    github_username = os.environ.get('GITHUB_USR')
    access_token = os.environ.get('GITHUB_TOKEN')

    if not (github_username and access_token):
        print("Please set the GITHUB_USR and GITHUB_TOKEN environment variables.")
        return

    # Fetch repositories
    repos = fetch_repositories(access_token, github_username)
    if not repos:
        print("No repositories found or there was an error fetching repositories.")
        return

    print("Total repositories:", len(repos))

    # Create a list to hold project information
    projects = []

    for repo in repos:
        repo_name = repo['name']

        # Fetch the contents of .cd/vars file
        vars_url = f'https://api.github.com/repos/{github_username}/{repo_name}/contents/cd/vars'
        headers = {'Authorization': f'token {access_token}'}

        try:
            vars_response = requests.get(vars_url, headers=headers)
            vars_response.raise_for_status()  # Raise an exception if the request is not successful

            if vars_response.status_code == 200:
                vars_content = vars_response.json()['content']
                decoded_content = base64.b64decode(vars_content).decode('utf-8')

                # Read variables from decoded content
                vars_dict = read_vars_file(decoded_content)

                if vars_dict:
                    # Populate project information dynamically from vars_dict
                    project_info = {
                        'repo': repo_name,
                        'project': github_username,
                        **vars_dict  # Unpack the vars_dict into the project_info dictionary
                    }
                    projects.append(project_info)
                else:
                    print(f"No variables found in .cd/vars for {repo_name}.")

            else:
                print(f"Could not fetch .cd/vars for {repo_name}. Status code: {vars_response.status_code}")

        except requests.exceptions.RequestException as e:
            print(f"Error fetching .cd/vars for {repo_name}: {e}")

        time.sleep(2)  # Add a delay to avoid rate limiting

    # Create a YAML file
    yaml_data = {'projects': projects}
    with open('projects.yaml', 'w') as yaml_file:
        yaml.dump(yaml_data, yaml_file, default_flow_style=False, sort_keys=False)

    print("Projects YAML file created: projects.yaml")

if __name__ == "__main__":
    main()


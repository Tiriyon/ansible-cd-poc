import os
import yaml
import requests

def read_vars_file(repo_path):
    vars_path = os.path.join(repo_path, '.cd/vars')
    if os.path.exists(vars_path):
        with open(vars_path, 'r') as vars_file:
            lines = vars_file.readlines()
            srv = None
            dst = None
            for line in lines:
                if line.startswith('destination_server='):
                    srv = line.split('=')[1].strip()
                elif line.startswith('destination_path='):
                    dst = line.split('=')[1].strip()
                if srv and dst:
                    break
            return srv, dst
    return None, None

def main():
    # GitHub username and personal access token
    github_username = 'Tiriyon'
    access_token = 'your_personal_access_token'

    try:
        # Fetch repository names using GitHub API
        url = f'https://api.github.com/user/repos'
        headers = {'Authorization': f'token {access_token}'}
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        repos = response.json()

        # Create a list to hold project information
        projects = []

        for repo in repos:
            repo_name = repo['name']
            repo_path = f'./Tiriyon/{repo_name}'  # Adjust the path accordingly

            if os.path.exists(os.path.join(repo_path, '.cd')):
                srv, dst = read_vars_file(repo_path)

                if srv and dst:
                    project_info = {
                        'project': github_username,
                        'repo': repo_name,
                        'srv': srv,
                        'dst': dst
                    }
                    projects.append(project_info)

        # Create a YAML file
        yaml_data = {'projects': projects}
        with open('projects.yaml', 'w') as yaml_file:
            yaml.dump(yaml_data, yaml_file, default_flow_style=False)

    except requests.exceptions.RequestException as e:
        print("An error occurred during the request:", e)
    except Exception as e:
        print("An unexpected error occurred:", e)

if __name__ == "__main__":
    main()


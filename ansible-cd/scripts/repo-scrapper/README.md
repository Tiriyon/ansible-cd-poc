## GitHub CD Vars Scraper Documentation

### Introduction

The "GitHub CD Vars Scraper" script is designed to retrieve key-value pairs from the `cd/vars` file in GitHub repositories owned by a specific user, and create a structured YAML file (`projects.yaml`) containing the extracted information. This script makes use of the GitHub API to fetch repository details and the contents of the `cd/vars` file.

### Related Subjects

1.  **GitHub API**: The script interacts with the GitHub API to fetch repository details and file contents.
2.  **Environment Variables**: GitHub username and access token are read from environment variables, providing a secure way to handle credentials.
3.  **Rate Limiting**: The script incorporates a time delay to avoid hitting rate limits imposed by the GitHub API.
4.  **Data Serialization**: The script uses YAML as a data serialization format to create the `projects.yaml` file.

### Requirements

1.  Python 3.x
2.  Required Python libraries: `requests`, `base64`, `yaml`, `os`
3.  GitHub Personal Access Token: You need a GitHub Personal Access Token with appropriate permissions to access the repositories.

### How the Script Works

1.  **Environment Variable Setup**: Before running the script, ensure you have set the `GITHUB_USR` and `GITHUB_TOKEN` environment variables with your GitHub username and personal access token, respectively.
    
2.  **Fetching Repositories**: The script retrieves a list of repositories owned by the specified GitHub username using the GitHub API search endpoint. It filters the repositories using the provided username.
    
3.  **Fetching .cd/vars Files**: For each repository, the script checks if a `.cd/vars` file exists. If it does, the script fetches the contents of the file from GitHub.
    
4.  **Parsing .cd/vars Contents**: The script reads the content of the `.cd/vars` file, parsing it to extract key-value pairs. Each key-value pair is considered a variable.
    
5.  **Creating Projects List**: The script creates a list of projects, each with details such as repository name, GitHub username, and variables extracted from the `.cd/vars` file.
    
6.  **Creating YAML File**: The script takes the list of projects and generates a YAML file (`projects.yaml`) that represents the project information in the specified structure.
    

### How to Operate

1.  **Set Environment Variables**: Set the `GITHUB_USR` and `GITHUB_TOKEN` environment variables with your GitHub username and personal access token.
    
2.  **Install Required Libraries**: If you haven't already, install the required Python libraries using pip:
    

```
pip install requests pyyaml
```

3. **Run the Script**: Run the script using Python in the terminal:

```
python3 main.py
```

4. **Check Output**: After the script runs, you'll find a `projects.yaml` file in the current directory containing the project information extracted from the `cd/vars` files in your GitHub repositories.

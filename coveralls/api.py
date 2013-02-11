import json
from StringIO import StringIO
import requests


def post(url, repo_token, service_job_id, service_name, git, source_files):
    json_file = StringIO(json.dumps({
        'repo_token': repo_token,
        'service_job_id': service_job_id,
        'service_name': service_name,
        'git': git,
        'source_files': source_files,
    }))
    return requests.post(url, files={'json_file': json_file})

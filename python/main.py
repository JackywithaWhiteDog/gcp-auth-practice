from google_auth_oauthlib import flow
from google.cloud import bigquery
from google.oauth2 import service_account

SCOPES = ['https://www.googleapis.com/auth/cloud-platform']

QUERY_STRING = """
SELECT
    EXTRACT(YEAR FROM date) year,
    EXTRACT(MONTH FROM date) month,
    SUM(confirmed) num_reports
FROM `bigquery-public-data.covid19_open_data.compatibility_view`
WHERE country_region = 'Taiwan'
GROUP BY year, month
HAVING num_reports IS NOT NULL
ORDER BY year, month ASC
"""

def get_client_as_service_account(filepath):
    credentials = service_account.Credentials.from_service_account_file(
        filepath, scopes=SCOPES
    )
    return bigquery.Client(credentials=credentials, project=credentials.project_id)

def get_client_as_user_account(filepath, launch_browser=True):
    appflow = flow.InstalledAppFlow.from_client_secrets_file(
        filepath, scopes=SCOPES
    )
    if launch_browser:
        appflow.run_local_server(port=8081)
    else:
        appflow.run_console()
    credentials = appflow.credentials
    return bigquery.Client(credentials=credentials)

def get_client_with_ADC():
    return bigquery.Client()

def query():
    """
    TODO: add secret file and pass them to functions
    """
    # client = get_client_as_service_account('/path/to/service_secret.json')
    # client = get_client_as_user_account('/path/to/client_secret.json', False)
    client = get_client_with_ADC()
    query_job = client.query(QUERY_STRING)
    for row in query_job:
        print(f'{row["year"]}-{row["month"]}: {row["num_reports"]}')

if __name__ == '__main__':
    query()

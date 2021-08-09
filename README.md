# GCP-Auth-Practice

This is a practice project for the Google Cloud Platform (GCP) Authentication.

## Preparation

To interact with GCP via API or SDK, you need to authenticate the User Account or the Service Account first.

### Login

- Login with User Account

```shell
gcloud auth login
```

- Login with User Account using [Application Default Credentials](https://google.aip.dev/auth/4110) (ADC)

```shell
gcloud auth application-default login
```

- Login with Service Account

```shell
gcloud auth activate-service-account --key-file [KEY_FILE]
```

- Login with Service Account using [Application Default Credentials](https://google.aip.dev/auth/4110) (ADC)

```shell
export GOOGLE_APPLICATION_CREDENTIALS=[KEY_FILE]
```

### Revoke

```shell
gcloud auth revoke [ACCOUNT] # revoke User / Service Account
gcloud auth application-default revoke # revoke User Account with ADC
unset GOOGLE_APPLICATION_CREDENTIALS # revoke Service Account with ADC
```

## Usage

In this section, I will show you how to use BigQuery to query monthly reports for COVID-19 in Taiwan using Cloud API, Cloud SDK and Client Libraries (Python).

### Cloud API

Put the access token into request header. ([example script](https://github.com/JackywithaWhiteDog/gcp-auth-practice/tree/main/api))

```shell
gcloud auth login
gcloud config set project [PROJECT_ID]
wget "https://github.com/JackywithaWhiteDog/gcp-auth-practice/raw/main/api/body.json"
curl -X POST "https://bigquery.googleapis.com/bigquery/v2/projects/$(gcloud config get-value project)/queries" \
-H "Authorization: Bearer $(gcloud auth print-access-token)" \
-H "Content-Type: application/json" \
-d @body.json
```

### Cloud SDK

Using bq command. ([example script](https://github.com/JackywithaWhiteDog/gcp-auth-practice/tree/main/sdk))

```shell
gcloud auth login
gcloud config set project [PROJECT_ID]
wget "https://github.com/JackywithaWhiteDog/gcp-auth-practice/raw/main/sdk/num_reports.sql"
bq query --nouse_legacy_sql --flagfile num_reports.sql
```

### Client Libraries (Python)

Requirements:

```text
google-auth==1.34.0 # Service Account Authentication
google-auth-oauthlib==0.4.5 # User Account Authentication
google-cloud-bigquery==2.23.2 # BigQuery interface
```

Although you can explicitly use the secret file for User Account / Service Account, using ADC can make things easier. ([example code](https://github.com/JackywithaWhiteDog/gcp-auth-practice/tree/main/python))

- Explicitly using Service Account

```python
def get_client_as_service_account(filepath):
    credentials = service_account.Credentials.from_service_account_file(
        filepath, scopes=SCOPES
    )
    return bigquery.Client(credentials=credentials, project=credentials.project_id)
```

- Explicitly using User Account

```python
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
```

- Implicit way with ADC

```python
def get_client_with_ADC():
    return bigquery.Client()
```

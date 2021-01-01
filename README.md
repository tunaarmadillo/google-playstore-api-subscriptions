# Google PlayStore API (Subscriptions)

A very basic script to serve as an example/guide on how to authenticate and then consume Google / Android PlayStore APIs, with managing user subscriptions through a "server-to-server" integration as the main use-case.

Hopefully this will be helpful for anyone trying to use these APIs as the documentation from is quite disjointed and doesn't provide any complete examples of executing API calls to the Android Publisher v3 services.

It also all relies on authentication based upon correct setup of a "Service Account" inside Gloud Cloud Platform (and subsequent configuration in the Android PlayStore Developer Account) which hopefully is clearly set out in this README.

## Installation

1. Clone this repository or download it.
2. Install Python 3 (<https://www.python.org/downloads/>)
3. Install the dependencies from the requirements.txt.

Assuming you already have Python installed, the following commands executed within the root of this repository should ensure the necessary dependencies are installed into a virtual environment as required. Using virtualenv is preferred, as it will not require system level install permissions, and will avoid clashes with system dependencies.

```bash
pip install virtualenv
virtualenv <your-env-name>
source <your-env-name>/bin/activate
pip install -r requirements.txt
```

## Other Inputs and Pre-Requisites

### 1. Config File (credentials JSON for authentication)

The scripts will look for a 'config.json' file within a /config subdirectory from the root. This file is donwloaded from Google by following the instructions on setting up and granting permissions for a "Service Account" for accessing the APIs.

#### 1a) Setting up a Google Cloud "Service Account"

<https://developers.google.com/android-publisher/getting_started#using_a_service_account> & here <https://developers.google.com/identity/protocols/oauth2/service-account#creatinganaccount>*
You will get a JSON file that you can rename "config.json" and place inside the /config/ directory where the script will pick it up and use it to authenitcate all API calls.

#### 1b) Grant "Service Account" necessary permissions

Based on the documentation here, the account will need to be able to view financial data for your applications: <https://support.google.com/googleplay/android-developer/answer/9844686?hl=en>

### 2. **CSV File (containing data for 1 or more PlayStore subscriptions)**

The sample scripts take a CSV files as inputs.

- **subscriptions_get.py** - is set to use './inputs/subs_to_get.csv' as its input by default.
- **subscriptions_cancel.py** - is set to use './inputs/subs_to_cancel.csv' as its input by default.

Multiple subscriptions can be added into the CSV files (one row per subscription). The CSV contains 3 fields that must ALL be provided for EACH subscription (row) in the file in order to make API calls for Android PlayStore (they serve as input arguments to the subscription management API calls):

- **PlayStore_token** - *string*, The token provided to the user's device when the subscription was purchased. (required)
- **PlayStore_subscriptionId** - *string*, The purchased subscription ID (for example, 'monthly001'). (required)
- **PlayStore_packageName** - *string*, The package name of the application for which this subscription was purchased (for example, 'com.some.thing'). (required)

This is as per the documentation here: <https://googleapis.github.io/google-api-python-client/docs/dyn/androidpublisher_v3.purchases.subscriptions.html#get>

## Usage

Make sure your virtual environment is activated:

```bash
source <your-env-name>/bin/activate
```

If all other pre-requisites above have also been met, you should be able to execute the scripts accordingly.

1. To retrieve information for list of subscriptions in /inputs/subs_to_get.csv:

    ```bash
    python subscriptions_get.py
    ```

2. To cancel subscriptions in /inputs/subs_to_cancel.csv:

    ```bash
    python subscriptions_cancel.py
    ```

The script will iterate through all rows in the relevant input CSV and record the results at the end into a timestamped csv into the "/outputs/" directory.

FYI - in case of the cancellation script, there is currently no response from the Google API (as per the specification). So it is advisable if cancelling subscription to call the "cancel" API first, and then checking if it has been effective by making a subsequent "get" request.

There is a LOT of printing enabled in the script for debugging. Further debugging is even possible if desired (see <https://github.com/googleapis/google-api-python-client/blob/master/docs/logging.md>).

## Further Documentation

There are many more resources available - full spec for the API here:
<https://googleapis.github.io/google-api-python-client/docs/dyn/androidpublisher_v3.html>
Some of them may require granting of further permissions to the Service Account in the Android PlayStore Developer Account before being able to access them. The developer account owner or admins should be able to enable that as required.

More documentation on Pandas which is used in a very basic way in this script for reading and writing to CSV files and iterating through data using Pandas dataframe):
<https://pandas.pydata.org/docs/user_guide/io.html#csv-text-files>
<https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html#pandas.DataFrame>
<https://realpython.com/python-csv/#reading-csv-files-with-pandas>

There's obviously loads that could be done to improve, but this was really just a PoC to understand the server-to-server API implementation.

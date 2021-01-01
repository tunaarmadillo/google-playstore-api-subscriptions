# Google Client libraries for authentication and API calls
from google.oauth2 import service_account
from googleapiclient.discovery import build
# Pandas library, used for loading csv into process and then adding data based on API response. 
import pandas
# For timestamping during processing
import time

timestr = time.strftime("%Y%m%d-%H%M%S")
print(timestr)

# INITIALISE GOOGLE CREDENTIALS
SCOPES = ['https://www.googleapis.com/auth/androidpublisher']
SERVICE_ACCOUNT_FILE = './config/config.json'

credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# INITIALISE CSV
df = pandas.read_csv('./inputs/subs_to_get.csv')
# ADD ADDITIONAL COLUMNS TO PANDAS DATAFRAME, WILL BE POPULATED USING THE GOOGLE CLIENT API
df['start_time'] = ''
df['end_time'] = ''
df['google_response_countryCode'] = ''
df['google_response_expiryTime'] = ''
df['google_response_paymentState'] = ''
df['google_response_autoRenewing'] = ''
df['google_response_cancelReason'] = ''
df['google_response_cancelSurveyResult'] = ''
df['google_response'] = ''

print('Source Data DF')
print(df)

for i in df.index:

        startTime = time.strftime("%Y%m%d-%H%M%S")

        PlayStore_subscriptionId = df.loc[i,'PlayStore_subscriptionId'] 
        PlayStore_packageName = df.loc[i,'PlayStore_packageName']
        PlayStore_token = df.loc[i,'PlayStore_token']

        androidPublisherService = build('androidpublisher', 'v3', credentials=credentials)

        try:
                response = androidPublisherService.purchases().subscriptions().cancel(
                        subscriptionId = PlayStore_subscriptionId,
                        packageName = PlayStore_packageName,
                        token = PlayStore_token,
                        x__xgafv = '1'
                        ).execute()
                
                endTime = time.strftime("%Y%m%d-%H%M%S")
                df.loc[i,'start_time'] = startTime
                df.loc[i,'end_time'] = endTime

                df.loc[i,'google_response'] = str(response)

                if 'countryCode' in response:
                        df.loc[i,'google_response_countryCode'] = response['countryCode']
                if 'expiryTimeMillis' in response:
                        df.loc[i,'google_response_expiryTime'] = response['expiryTimeMillis']
                if 'paymentState' in response:
                        df.loc[i,'google_response_paymentState'] = response['paymentState']
                if 'autoRenewing' in response:
                        df.loc[i,'google_response_autoRenewing'] = response['autoRenewing']
                if 'cancelReason' in response:
                        df.loc[i,'google_response_cancelReason'] = response['cancelReason']
                if 'cancelSurveyResult' in response:
                        df.loc[i,'google_response_cancelSurveyResult'] = str(response['cancelSurveyResult'])

                print(str(i) + " - Start:" + startTime + " - End:" + endTime + " - response: " + str(response)) 

        except:
                endTime = time.strftime("%Y%m%d-%H%M%S")
                print(str(i) + " - Start:" + startTime + " - End:" + endTime + " - response: " + 'ERROR OCCURRED')

print('Output Data DF')
print(df)

timestr = time.strftime("%Y%m%d-%H%M%S")
df.to_csv('./outputs/output-' + timestr + '.csv')
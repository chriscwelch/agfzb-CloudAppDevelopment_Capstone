import json
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions
from ibm_watson.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions

apikey = "s_TkKnbbGIAZ9n74bm47iQ3xij3xrtoDquIoRLUWhWfa"

authenticator = IAMAuthenticator(apikey)
natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2021-08-01',
    authenticator=authenticator
)

url = "https://api.eu-gb.natural-language-understanding.watson.cloud.ibm.com/instances/5a78596d-caca-44ca-a7e2-514384bae147"

natural_language_understanding.set_service_url(url)

# response = natural_language_understanding.analyze(
#     url='www.wsj.com/news/markets',
#     features=Features(sentiment=SentimentOptions(targets=['covid-19']))).get_result()

# response = natural_language_understanding.analyze(text="Great service!",
#     features=Features(sentiment=SentimentOptions(document=True), entities=EntitiesOptions(emotion=True,
#     sentiment=True,
#     limit=2))).get_result()

response = natural_language_understanding.analyze(text="great service!", language="en",
    features=Features(sentiment=SentimentOptions(document=True))).get_result()

print(json.dumps(response, indent=2))

import os
from dotenv import load_dotenv
from Vectara.query import *
import requests

load_dotenv()

url = "https://api.vectara.io/v1/query"
query_prompt = 'Who is the Dragon of Dojima?'

VECTARA_CUSTOMER_ID = os.getenv('VECTARA_CUSTOMER_ID')
VECTARA_CORPUS_ID  = os.getenv('VECTARA_CORPUS_ID')

#approach 1

# VECTARA_JWT_TOKEN  = os.getenv('VECTARA_JWT_TOKEN')
# response = query_vectara(VECTARA_CUSTOMER_ID, VECTARA_CORPUS_ID, url, VECTARA_JWT_TOKEN, query_prompt)
# print(response)


#approach 2
VECTARA_YAKUZA_WIKI_API_KEY = os.getenv('VECTARA_YAKUZA_WIKI_API_KEY')

payload = json.dumps({
  "query": [
    {
      "query": query_prompt,
      "start": 0,
      "numResults": 10,
      "contextConfig": {
        "sentencesBefore": 3,
        "sentencesAfter": 3,
        "startTag": "<b>",
        "endTag": "</b>"
      },
      "corpusKey": [
        {
          "corpusId": VECTARA_CORPUS_ID,
          "semantics": "DEFAULT",
          "dim": [
            {
              "name": "relevance",
              "weight": 1.5
            }
          ],
          "lexicalInterpolationConfig": {
            "lambda": 0.7
          }
        }
      ],
      "rerankingConfig": {
        "rerankerId": 272725718,
        "mmrConfig": {
          "diversityBias": 0.4
        }
      },
      "summary": [
        {
          "summarizerPromptName": "vectara-summary-ext-v1.3.0",
          "maxSummarizedResults": 3,
          "responseLang": "en",
          "promptText": "[\n  {\"role\": \"system\", \"content\": \"You are an expert in summarizing information from the Yakuza video game series.\"},\n  #foreach ($result in $vectaraQueryResults)\n    {\"role\": \"user\", \"content\": \"What are the key points in result number $vectaraIdxWord[$foreach.index]?\"},\n    {\"role\": \"assistant\", \"content\": \"In result number $vectaraIdxWord[$foreach.index], the key points are: ${result.getText()}\"},\n  #end\n  {\"role\": \"user\", \"content\": \"Can you generate a comprehensive summary that answers the question?\"}\n]\n",
          "responseChars": 500,
          "modelParams": {
            "maxTokens": 1024,
            "temperature": 0.6,
            "frequencyPenalty": 0.2,
            "presencePenalty": 0.1
          },
          "factualConsistencyScore": True
        }
      ]
    }
  ]
})
headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json',
  'customer-id': VECTARA_CUSTOMER_ID,
  'x-api-key': VECTARA_YAKUZA_WIKI_API_KEY
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)

import os
import json
import requests
from dotenv import load_dotenv
#from query import *

class VectaraAPI:
    def __init__(self):
        load_dotenv()
        self.url = "https://api.vectara.io/v1/query"
        self.customer_id = os.getenv('VECTARA_CUSTOMER_ID')
        self.corpus_id = os.getenv('VECTARA_CORPUS_ID')
        self.api_key = os.getenv('VECTARA_YAKUZA_WIKI_API_KEY')
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'customer-id': self.customer_id,
            'x-api-key': self.api_key
        }
        self.conversation_id = ""

    def query(self, query_prompt):
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
                          "corpusId": self.corpus_id,
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
                          "summarizerPromptName": "vectara-summary-ext-v1.2.0",
                          "maxSummarizedResults": 3,
                          "responseLang": "en",
                          #"promptText": "[\n  {\"role\": \"system\", \"content\": \"You are an expert in summarizing information from the Yakuza video game series.\"},\n  #foreach ($result in $vectaraQueryResults)\n    {\"role\": \"user\", \"content\": \"What are the key points in result number $vectaraIdxWord[$foreach.index]?\"},\n    {\"role\": \"assistant\", \"content\": \"In result number $vectaraIdxWord[$foreach.index], the key points are: ${result.getText()}\"},\n  #end\n  {\"role\": \"user\", \"content\": \"Can you generate a comprehensive summary that answers the question?\"}\n]\n",
                        }
                      ]
                    }
                  ]
        })
        response = requests.request("POST", self.url, headers=self.headers, data=payload)
        return json.loads(response.text)

    def save_responses(self, response_json, save_to_file = False):
        top_responses = {resp['text']: resp['score'] for resp in response_json['responseSet'][0]['response']}
        summary_text = response_json['responseSet'][0]['summary'][0]['text']
        if save_to_file is True:
          with open('response_data.txt', 'w', encoding="utf-8") as f:
              f.write("Top Responses:\n")
              for text, score in top_responses.items():
                  f.write(f"Text: {text}, Score: {score}\n")
              f.write("\nSummary:\n")
              f.write(summary_text)
        return summary_text, top_responses

    def chat(self, query_prompt):
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
                          "corpusId": self.corpus_id,
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
                              "chat": {
                                  "store": True,
                                  "conversationId": self.conversation_id
                              },
                              "maxSummarizedResults": 3,
                              "responseLang": "en",
                          }
                      ]
                    }
                  ]
        })

        response = requests.request("POST", self.url, headers=self.headers, data=payload)
        response_json = json.loads(response.text)
        if not self.conversation_id:
            self.conversation_id = response_json['responseSet'][0]['summary'][0]['chat']['conversationId']
        return response_json

# Usage
# vectara_api = VectaraAPI()
# query_prompt = 'Who is the Dragon of Dojima?'
# query_prompt2 = 'Who are the daughter and brother of Kiryu??'
# response_json = vectara_api.query(query_prompt2)
# vectara_api.save_responses(response_json)
# conversation_id = ""
# chat_response_json = vectara_api.chat(conversation_id)

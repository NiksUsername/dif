import argparse
import json

from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan
import requests

import config

header= {
    'Content-Type': 'application/json'
}

def analyze_container_logs(email, container_names):
    es = Elasticsearch([{'host': config.ELASTIC_IP, 'port': config.ELASTIC_PORT, 'scheme': "http"}])
    index_name = "docker-logs"

    for container_name in container_names:
        query = {
            "query": {
                "match": {
                    "container.image.name": container_name
                }
            }
        }

        try:
            hits = scan(es, query=query, index=index_name)
            grouped_hits = []

            for hit in hits:
                grouped_hits.append(hit["_source"])
                if len(grouped_hits) == config.GROUP_SIZE:
                    try:
                        data = {
                            "logs": json.dumps(grouped_hits),
                            "email": email
                        }
                        response = requests.post(url=config.URL,headers=header, json=data)
                    except requests.exceptions.RequestException as e:
                        print(f"Error sending request for container {container_name}: {e}")
                    grouped_hits = []

            if grouped_hits:
                try:
                    data = {
                        "logs": json.dumps(grouped_hits),
                        "email": email
                    }
                    response = requests.post(url=config.URL, headers=header, json=data)
                except requests.exceptions.RequestException as e:
                    print(f"Error sending request for container {container_name}: {e}")

        except Exception as e:
            print(f"Error querying Elasticsearch for container {container_name}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Analyze Docker container logs from Elasticsearch.")
    parser.add_argument("email", help="Email address to send analysis results.")
    parser.add_argument("-c", "--containers", nargs="+", required=True, help="List of container names to analyze.")

    args = parser.parse_args()
    analyze_container_logs(args.email, args.containers)

if __name__ == "__main__":
    main()
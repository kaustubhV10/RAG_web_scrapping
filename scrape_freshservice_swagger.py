# scrape_freshservice_swagger.py
import requests
import json
from getpass import getpass

OUTFILE = "freshservice_docs.jsonl"

def fetch_swagger_json():

    print("Enter your Freshservice domain (e.g., 'yourcompany.freshservice.com'):")
    domain = input().strip()
    
    print("Enter your Freshservice API key:")
    api_key = getpass()
    
    url = f"https://{domain}/api/v2/swagger.json"
    
    headers = {
        "Content-Type": "application/json"
    }
    
    response = requests.get(url, headers=headers, auth=(api_key, "X"))
    response.raise_for_status()
    return response.json()


def parse_swagger(swagger_json):
    docs = []
    
    paths = swagger_json.get("paths", {})
    for path, methods in paths.items():
        for method, info in methods.items():
            heading = f"{method.upper()} {path}"
            
            # Collect description
            desc = info.get("description", "")
            
            # Collect parameters
            params = info.get("parameters", [])
            params_text = "\n".join([
                f"{p.get('name')} ({p.get('in')}): {p.get('description','')}" 
                for p in params
            ])
            
            # Collect responses
            responses = info.get("responses", {})
            resp_text = "\n".join([
                f"{code}: {r.get('description','')}" for code,r in responses.items()
            ])
            
            # Combine all text
            text = "\n".join(filter(None, [desc, "Parameters:\n"+params_text if params_text else "", 
                                           "Responses:\n"+resp_text if resp_text else ""]))
            
            if text.strip():  
                docs.append({
                    "url": path,
                    "heading": heading,
                    "text": text
                })
    return docs


def save_docs_jsonl(docs, outfile=OUTFILE):
    with open(outfile, "w", encoding="utf8") as f:
        for doc in docs:
            f.write(json.dumps(doc, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    swagger_json = fetch_swagger_json()
    docs = parse_swagger(swagger_json)
    save_docs_jsonl(docs)
    print(f"Saved {len(docs)} API docs to {OUTFILE}")

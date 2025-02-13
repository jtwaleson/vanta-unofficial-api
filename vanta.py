import argparse
import json
import requests

class VantaGraphqlAPI:
    def __init__(self, host, connect_sid_cookie_value):
        self.host = host
        session = requests.session()
        session.cookies.set('connect.sid', connect_sid_cookie_value)
        session.headers.update({
            "x-csrf-token": "this_csrf_header_is_constant",
            "content-type": "application/json",
            "accept": "application/json",
        })
        self.session = session

    def enumerate_custom_task_status(self, task_title):
        cursor = None
        has_next_page = True
        
        while has_next_page:
            operation = {
                "operationName": "fetchUsersForPeopleTableV2",
                "variables": {
                    "filters": {
                        "includeNonHumanUsers": False,
                        "includeRemovedUsers": False,
                        "groupFilters": {"groups": []},
                    },
                    "sortParams": {"field": "name", "direction": 1},
                    "first": 100,
                    "after": cursor
                },
                "query": """query fetchUsersForPeopleTableV2($first: Int!, $after: String, $sortParams: sortParams!, $filters: UserFilters!) {
                  organization {
                    people(first: $first, after: $after, sortParams: $sortParams, filters: $filters) {
                      edges {
                        node {
                          id
                          displayName
                          email
                          employmentStatus
                          employeeChecklistTaskCompletions {
                            extraInformation
                            checklistTask {
                              title
                            }
                          }
                        }
                      }
                      pageInfo {
                        endCursor
                        hasNextPage
                      }
                    }
                  }
                }"""
            }

            response = self.session.post(f"https://{self.host}/graphql?operation=fetchUsersForPeopleTableV2", json.dumps(operation))
            response.raise_for_status()
            data = response.json()
            
            # Extract the people data
            people = data["data"]["organization"]["people"]["edges"]
            for person in people:
                node = person["node"]
                # Find the laptop usage information
                answer = None
                if "employeeChecklistTaskCompletions" in node:
                    for completion in node["employeeChecklistTaskCompletions"]:
                        if completion["checklistTask"]["title"] == task_title:
                            answer = completion["extraInformation"]
                            break
                
                yield {
                    "id": node["id"],
                    "name": node["displayName"],
                    "email": node["email"],
                    "status": node["employmentStatus"],
                    "answer": answer
                }
                
            # Update pagination info
            page_info = data["data"]["organization"]["people"]["pageInfo"]
            cursor = page_info["endCursor"]
            has_next_page = page_info["hasNextPage"]



def main():
    args = argparse.ArgumentParser()
    args.add_argument("--host", type=str, default="app.eu.vanta.com")
    args.add_argument("--connect-sid", type=str, required=True)
    args.add_argument("--task-title", type=str, required=True)
    args = args.parse_args()

    
    client = VantaGraphqlAPI(args.host, args.connect_sid)
    for person in client.enumerate_custom_task_status(args.task_title):
        if person["status"] != "CURRENTLY_EMPLOYED":
            continue
        print(f"{person['name']}\t{person['email']}\t{person['answer']}")


if __name__ == "__main__":
    main()

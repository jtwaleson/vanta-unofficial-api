Unofficial Vanta API client for Python.

## About

This is a tiny unofficial API client for Vanta. It is not affiliated with Vanta and is not supported by Vanta. Vanta uses a GraphQL API that is not documented. For some things that are not exposed over the regular REST API, this client may be useful.

Personally I use it to track the status of people who have completed custom tasks. There is no overview in the Vanta UI to see or export this data.

Using your browser inspector, you can find some endpoints and get more info out of it. I found that the endpoints are quite flexible.

Interestingly, the only necessary cookie is the `connect.sid` cookie.

I've confirmed this to work on the EU Vanta instance in February 2025.

## Usage

```bash
python vanta.py --connect-sid <connect-sid> --task-title "Using other laptop/desktop computers" --host app.eu.vanta.com
```

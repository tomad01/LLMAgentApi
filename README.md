# LLMAgentApi
This api is meant to receive chat like or email like requests from a certain domain and deal with them using langchain agents


## How to use:
generate a solution for a query
```
curl -X POST http://0.0.0.0:8000/generate -H "Content-Type: application/json" -d '{"query":"how do you turn this on","query_type":"chat"}'
```

retrieve similar querys
```
curl -X POST http://0.0.0.0:8000/retrieve -H "Content-Type: application/json" -d '{"query":"how do you turn this on","query_type":"chat"}'
```

before commiting, run 
 - src/llm_agent_api/start_fastapi_server.sh
 - pytest
 - black . 
 - pylint src/llm_agent_api
curl https://api.anthropic.com/v1/messages \
    --header "x-api-key: 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" \
    --header "anthropic-version: 2023-06-01" \
    --header "content-type: application/json" \
    --data \
'{
    "model": "claude-3-5-sonnet-20241022",
    "max_tokens": 1024,
    "messages": [
        {"role": "user", "content": "Hello, world"}
    ]
}'
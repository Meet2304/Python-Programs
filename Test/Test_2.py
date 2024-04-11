def parse_parameters(url):
    params = {}
    if '?' in url:
        query_string = url.split('?')[1]
        parameters = query_string.split('&')
        for param in parameters:
            key, value = param.split('=')
            params[key] = value
    return params

def getResponses(valid_auth_tokens, requests):
    responses = []
    for request in requests:
        method, url = request
        params = parse_parameters(url)
        
        if 'token' not in params:
            responses.append("INVALID")
            continue
        
        auth_token = params['token']
        if auth_token not in valid_auth_tokens:
            responses.append("INVALID")
            continue
        
        if method == 'POST':
            if 'csrf' not in params or not params['csrf'].isalnum() or len(params['csrf']) < 8:
                responses.append("INVALID")
                continue
        
        response_string = "VALID"
        for key, value in params.items():
            if key != 'token' and (method == 'GET' or (method == 'POST' and key != 'csrf')):
                response_string += f", {key}, {value}"
        
        responses.append(response_string)
    
    return responses

# Example usage:
valid_auth_tokens = ["ah37j2ha483u", "safh34ywb0p5", "ba34wyi8t902"]
requests = [
    ["GET", "https://example.com/?token=347sd6yk8iu2&name=alex"],
    ["GET", "https://example.com/?token=safh34ywb0p5&name=sam"],
    ["POST", "https://example.com/?token=safh34ywb0p5&name=alex"],
    ["POST", "https://example.com/?token=safh34ywb0p5&csrf=ak2sh32dy&name=chris"]
]

responses = getResponses(valid_auth_tokens, requests)
print(responses)

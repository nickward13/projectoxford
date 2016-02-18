# Project Oxford speech authorization module

import urllib.parse, http.client, json

def auth(clientId, clientSecret):
    """Retrieves access token to set up an authorized Project Oxford speech API session
    """
    
    # Setup REST API call details
    ttsHost = "https://speech.platform.bing.com"
    params = urllib.parse.urlencode({'grant_type': 'client_credentials', 'client_id': clientId,
        'client_secret': clientSecret, 'scope': ttsHost})
    headers = {"Content-type": "application/x-www-form-urlencoded"}
    AccessTokenHost = "oxford-speech.cloudapp.net"
    path = "/token/issueToken"

    # Connect to REST API to get the Oxford Access Token
    conn = http.client.HTTPSConnection(AccessTokenHost)
    conn.request("POST", path, params, headers)
    response = conn.getresponse()
    
    # Retrieve the response to local data variable
    data = response.read()
    conn.close()
    accesstoken = data.decode("UTF-8")
    
    #decode the token object from json
    ddata=json.loads(accesstoken)
    access_token = ddata['access_token']
    
    # Return the token
    return access_token;

def synthesize(access_token, clientId, text_to_synthesize):
    """Converts text to a WAV data stream that can be written to a file
    """
    
    # Setup REST API call details (note used of Australian voice request in the body)
    headers = {"Content-type": "application/ssml+xml", 
			"Authorization": "Bearer " + access_token,
            "X-Microsoft-OutputFormat": "riff-8khz-8bit-mono-mulaw",
            "User-Agent": clientId}
    body="""<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" \
        xmlns:mstts="http://www.w3.org/2001/mstts" xml:lang="en-AU">\
        <voice name="Microsoft Server Speech Text to Speech Voice (en-AU, Catherine)">"""
    body = body + text_to_synthesize 
    body = body + '</voice></speak>'
    
    # Connect to REST API to get synthesized audio
    conn = http.client.HTTPSConnection("speech.platform.bing.com")
    conn.request("POST", "/synthesize", body, headers)
    response = conn.getresponse()
    
    if response.status != 200:
        conn.close()
        return 0
    
    # read response data and return to caller
    responsedata = response.read()
    conn.close()
    return responsedata
    

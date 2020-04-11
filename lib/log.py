import re
from lib.statuses import available, taken, manual
from lib.ConfigHelper import ConfigHelper, DOMAIN

ch = ConfigHelper()

def log_result(response, word, link, matches=None):
    service = re.search(DOMAIN, link).group(1)
    if matches != None:
        if matches[0] != []:
            available(word, service, link)
        elif matches[1]:
            taken(word, service)
        elif matches[2]:
            taken(word, service)
        else:
            manual(response, word, service)
        
    elif response.status_code == 200:
        if ch.getSite() == 3: # Twitter
            obj = response.json()
            if obj['valid'] == True:
                available(word, service, link)
            else:
                err = obj['msg']
                taken(word, service, error=err)
        elif ch.getSite() == 4: # Instagram
            obj = response.json()
            if obj['dryrun_passed']:
                available(word, service, link)
            else:
                taken(word, service)
        elif ch.getSite() == 2: # Minecraft
            obj = response.json()
            if 'name' in obj:
                taken(word, service)
                if 'errorMessage' in obj:
                    print(obj['errorMessage'])
            else:
                available(word, service, None)
        elif ch.getSite() == 9: # Mixer
            obj = response.json()
            if 'statusCode' in obj:
                available(word, service, link)
            else:
                taken(word, service)
        elif ch.getSite() == 8: # Twitch
            taken(word, service)
        elif ch.getSite() == 15: # Reddit
            text = response.text
            if text == "true":
                available(word, service, link)
            else:
                taken(word, service)
        elif ch.getSite() == 12: # YouTube via checkerapi.com
            obj = response.json()
            if obj["status"] == "available":
                available(word, "YouTube", link)
            else:
                taken(word, "YouTube")
        else:
            taken(word, service)
    elif response.status_code == 204:
        if ch.getSite() == 2:
            available(word, service, link)
        elif ch.getSite() == 8:
            available(word, service, link)
        else:
            manual(response, word, service)
    elif response.status_code == 404:
        available(word, service, link)
    else:
        manual(response, word, service)
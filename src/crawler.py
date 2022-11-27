from src.urls import baseParams, apiUrl, rolesUrl

import requests
import re

titleParams = {**baseParams, 'list':'search', 'srwhat':'title', 'srsearch':'role'}
pageParams = {**baseParams, 'prop':'categories|revisions', 'rvprop':'content', 'titles':'title'}

REDIRECT_CAPTURE = r"#REDIRECT \[\[(.*)\]\]"

def getRolePage(role):
    title = searchRoleTitle(role)
    return searchRolePage(title)

def searchRoleJsonWiki(role):
    r = requests.get(url=apiUrl, params={**titleParams, 'srsearch':role})
    if r.status_code != requests.codes.ok:
        r.raise_for_status()
    return r.json()['query']['search']

def searchRoleTitle(role):
    data = searchRoleJsonWiki(role)
    if len(data) == 0:
        raise ValueError("not found")
    return data[0]['title']

def searchRolePage(title):
    r = requests.get(url=apiUrl, params={**pageParams, 'titles':title})
    data = r.json()['query']
    if not '-1' in data:
        page = data['pages'][next(iter(data['pages'].keys()))]
        redirect = re.match(REDIRECT_CAPTURE, page['revisions'][0]['*'])
        if redirect:
            return searchRolePage(redirect.groups()[0])
        return page

def getRoles():
    r = requests.get(rolesUrl)
    return r.json()
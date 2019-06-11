import functools
print_flush = functools.partial(print, flush=True)

from mantis_utils.mantis.Connector import Connector

import timer_wraps
import requests

types = {
    "ISSUE_ADD": { "name": "mc_issue_add" },
    #"ISSUE_DELETE": { "name": "mc_issue_delete" },
    "ISSUE_GET": { "name": "mc_issue_get"},
    "ISSUE_UPDATE" : { "name": "mc_issue_update" },

    "ISSUE_NOTE_ADD": { "name": "mc_issue_note_add" },
    #"ISSUE_NOTE_DELETE": { "name": "mc_issue_note_delete" },
    #"ISSUE_NOTE_UPDATE": { "name": "mc_issue_note_update" },
    "WEB_ISSUE_ACCESS": { "name": "web_issue_access" },
}

def mantis_login(url, username, password):
    global connector
    global accountData
    global issue
    global issueUrl
    global requestData
    global mantisSession
    global issueReq

    # connect soap api
    soapUrl = '{}/api/soap/mantisconnect.php?wsdl'.format(url)
    connector = Connector(soapUrl, username, password)
    connector.connect()

    # prepare soap api type
    accountType = connector._mc.client.get_type('ns0:AccountData')
    accountData = accountType(id = 909, name = '10079186', real_name = '王\u3000詩博', email = 'sibo_wang@ot.olympus.co.jp')

    issueType = connector._mc.client.get_type('ns0:IssueData')

    projectId = connector.getProjectId('TEST')

    objType = connector._mc.client.get_type('ns0:ObjectRef')
    project = objType(id = projectId)

    issue = issueType(
        project = project,
        category = 'General',
        summary = 'summary',
        description = 'description',
        reporter = accountData)

    # HTTP request session
    mantisSession = requests.Session()
    issueUrl = '{}/view.php?id=30123'.format(url)
    loginUrl = '{}/login.php'.format(url)

    requestData = { 'username': username, 'password': password }

    # get issue request
    issueReq = requests.Request('GET', issueUrl)

    # login request
    loginReq = requests.Request('POST', loginUrl, data=requestData)

    # do login
    res = sendRequest(loginReq)

def sendRequest(request):
    mantisSession.prepare_request(request)
    prepped = mantisSession.prepare_request(request)
    return mantisSession.send(prepped)

@timer_wraps.measure_time
def mc_issue_add_perf():
    connector._mc.client.service.mc_issue_add(
        connector._mc.user_name,
        connector._mc.user_passwd,
        issue)

@timer_wraps.measure_time
def mc_issue_delete_perf():
    pass

@timer_wraps.measure_time
def mc_issue_get_perf():
    connector.getIssue(38990)

@timer_wraps.measure_time
def mc_issue_update_perf():
    connector._mc.client.service.mc_issue_update(
        connector._mc.user_name,
        connector._mc.user_passwd,
        33604,
        issue)


@timer_wraps.measure_time
def mc_issue_note_add_perf():
    connector.addNote(33604, accountData, 'Hello')

@timer_wraps.measure_time
def mc_issue_note_delete_perf():
    pass

@timer_wraps.measure_time
def mc_issue_note_update_perf():
    pass

@timer_wraps.measure_time
def web_issue_access_perf():
    res = sendRequest(issueReq)

def print_types():
    for k, v in types.items():
        print_flush("type: {},\t\tAPI: {}".format(k, v))

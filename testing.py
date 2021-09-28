import argparse
import csv
import json
import re
import time
import datetime
import os
import jenkinsapi
import pytz
import requests
import subprocess

import urllib3
from jenkinsapi.jenkins import Jenkins

parser = argparse.ArgumentParser()
parser.add_argument(
    '-u',
    '--username',
    type=str,
    required=True,
    help="Username of Jenkins")
parser.add_argument(
    '-p',
    '--password',
    type=str,
    required=True,
    help="Password of the username")
args = parser.parse_args()


def rest_api_call(url):
    response = requests.get(url, auth=(args.username, args.password), verify=False)
    return response

def was_aborted(text):
    occ = re.findall(r"Finished: ABORTED", text)
    if not occ:
        return False
    return True
J = Jenkins('http://localhost:8080/', username=args.username, password=args.password, ssl_verify=False, timeout=10)

PARENT_BUILD_NUMBER = int(os.environ['BUILD_NUMBER'])
job_name = os.environ['JOB_BASE_NAME']
print("-------"+job_name)
job_url = J[os.environ['JOB_NAME']]
# job_status = J[os.environ['currentBuild']]
# job_status_second = J[os.environ['result']]
build_info = J[jenkins.Jenkins.get_build_info(job_url,PARENT_BUILD_NUMBER)]
job_status = build_info['result']
print(job_status)
# print(job_status_second)
print("------------------"+str(job_url))

# print(os.environ['BUILD_URL'])
# print(job_url.get_downstream_builds())
# print(job_url.get_downstream_job_names())
# print(job_url.get_downstream_jobs())
print("----------------")
bld = job_url.get_build(PARENT_BUILD_NUMBER)
bld_console = bld.get_console()
bldState = "Pass"
isGood = bld.is_good()
if not isGood:
    bldState = "FAIL"
    if was_aborted(bld_console):
        bldState = "ABORTED"
    else:
        if bld.is_running():
                bldState = "RUNNING"
print(bldState)
bld_time = bld.get_duration().total_seconds()
print(bld_time)
# info = J.get_job_info(os.environ['JOB_NAME'])
# print(info)

# print(bld.get_downstream_builds())
# print(bld.get_downstream_job_names())
# print(bld.get_downstream_jobs())
# print(bld.get_result_url())
JOB_BASE_NAME = os.environ['JOB_BASE_NAME']
print("-------------"+JOB_BASE_NAME)
bld_console = bld.get_console()


stage_occ = re.findall(r"testStage:.*",bld_console)
for stage in stage_occ:
    item = re.split(":",stage)
    item1 = item[1]
    item2 = re.split(",", item1)
    item3 = item2[0]

    print(item3)
else:
    stage_occ = re.findall(r"STAGE_NAME=.*", bld_console)
    for stage in stage_occ:
        item = re.split("=", stage)
        item1 = item[1]
        print(item1)

node_occ = re.findall(r"NODE_NAME=.*",bld_console)
for node in node_occ:
    item = re.split("=",node)
    build_bot = item[1]
    print(build_bot)

version_occ = re.findall(r"androidVersion --- .*",bld_console)
for version in version_occ:
    item = re.split("--- ",version)
    android_version = item[1]
    print(android_version)


# print(occ)
myDict = {}
occ = re.findall(r"Starting building: testing_folder.*", bld_console)
print("---------------{}---------".format(occ))
for entry in occ:
    # extract integer build number
    # items = re.split("Â» ", entry)
    # split_value = items[1]
    # print(split_value)
    items_2 = re.split("#", entry)
    bldNumber = int(items_2[1])

    # extract job name
    tmp = items_2[0].strip()
    items2 = re.split(" ", tmp)
    bldJobName = items2[len(items2) - 1]

    # job numbers need to be in a list because Testing Pipeline uses exact name multiple times
    print("Adding Job: " + bldJobName + " : " + str(bldNumber))
    buildNumbers = myDict.get(bldJobName)

    # job numbers need to be in a list because Testing Pipeline uses exact name multiple times

    # if it doesnt exist, create new list
    if buildNumbers is None:
        buildNumbers = []
    buildNumbers.append(bldNumber)
    myDict[bldJobName] = buildNumbers


# down_stream_job = J.get_job_name()
# print(down_stream_job)
# print(myDict)
# doen_job = J["testing_folder/"+ bldJobName]
# print(doen_job)
#
#
# print(doen_job.baseurl)
# print_job =str(doen_job.baseurl)+"/"+str(bldNumber)+"/wfapi"
# print(print_job)
# bld_con = bld_down.get_console()
# print(bld_con)
for down_job in myDict.keys():
    # access job, did this job run at all?
    builds = myDict.get(down_job)
    # print(down_job)
    # print(myDict.keys())
    # print(builds)
Parent_build_url = os.environ['BUILD_URL']
wfapi_vale = Parent_build_url + "/wfapi"
pipeline_data = rest_api_call(wfapi_vale)
pipeline_data = pipeline_data.json()
for stage in pipeline_data["stages"]:
    if stage["name"] == "AOSP build":
        AOSP_durtion = stage["durationMillis"]
        print(AOSP_durtion)
        
        # print(AOSP_durtion.total_seconds() * 1000)
        # mydate = datetime.timedelta(AOSP_durtion)
        # mseconds = (AOSP_durtion % 1000)
        # seconds = (AOSP_durtion / 1000) % 60
        # seconds = int(seconds)
        # minutes = (AOSP_durtion / (1000 * 60)) % 60
        # minutes = int(minutes)
        # hours = (AOSP_durtion / (1000 * 60 * 60)) % 24
        # hours = int(hours)

        # mytime = datetime.datetime.strptime("{}:{}:{}.{}".format(hours, minutes, seconds, mseconds), '%H:%M:%S.%f')
        #
        # print ("{} hours {} minutes {} seconds {} milliseconds".format(hours, minutes, seconds, mseconds))


#         mytime = datetime.timedelta(milliseconds=AOSP_durtion)
#
#         s = mytime.strftime('%H:%M:%S.%f')
#         mytimeget = s[:-4]
#         print("----------------")
#         # mytime = datetime.datetime.fromtimestamp(AOSP_durtion / 1000.0)
#
#         # mytime1 =datetime.datetime.strptime(string(AOSP_durtion),"%H:%M:%S.%f")
#         # mytime2 = datetime.datetime.strptime(mytime,"%H:%M:%S.%f")
#         print(mytimeget)
#         # print(mytime1)
#         # print(mytime2)
#         # AOSP_BUILD_TIME =mydate. +" hours, "+mydate.getUTCMinutes()+" minutes and "+mydate.getUTCSeconds()+" second(s)";
#         # print(AOSP_BUILD_TIME)
#
# occ_domain = re.findall(r"Domain:.*", bld_console)
#
# # print(occ_domain)
# domain_value = []
# # print(domain_value)
# change_Type_value = []
# bld_result = {}
# for entry in occ_domain:
#     # occ_change_type = re.findall(r"Change-Type:.*", entry)
#     items = entry.split()
#     # print(items)
#     domain_index = items.index("Domain:")
#     change_type_index = items.index("Change-Type:")
#     domain_value.append(items[domain_index + 1])
#     change_Type_value.append(items[change_type_index + 1])
#     # print(domain_value)
#     # print(change_Type_value)
#
# if len(domain_value) == 0 and len(change_Type_value) == 0:
#     bld_result["chang-type"] = "-"
#     bld_result["domain"] = "-"
# else:
#     bld_result["chang-type"] = change_Type_value
#     bld_result["domain"] = domain_value
#
# print(bld_result)
#
# # split_value= items[1]
# # print(items[1])
# # print(items[0])
# # value = re.split(" ", split_value)
# # domain_value = value[1]
# # print(domain_value)
# #
# # for entry in occ_change_type:
# #     items = re.split(":", entry)
# #     split_value= items[1]
# #     value = re.split(" ", split_value)
# #     change_type_value = value[1]
# #     print(change_type_value)
dict_1 = {"a":1,"b":2}
dict_list=[]
dict_list.append(dict_1)
error_1 = {"a":1,"b":2}
error_list=[]
error_list.append(error_1)

result_dict = dict_ex = {}
error_ex = {}
dict_ex["dict_key"]=dict_list
error_ex["errror_key"]=error_list

result_dict.update(error_ex)
print(dict_ex)
lines = subprocess.check_output(
       ['git', 'log'], stderr=subprocess.STDOUT
       ).decode("utf-8").split("\n")


# print(lines)
stream = os.popen('git log')
output = stream.read()
# print(output)


result = re.findall(r'.*' + 'CHANGELIST_local:' + '.*(?:.*\n){' + str(1) + '}.*', bld_console)
print(result)
for res in result:
    first_split = res.split()
    print(first_split)
#     res_1 = re.split("]\s[", res)
#     print("res_1")
#     print(res_1)
#     split_1 = res_1[1]
#     print("split_1")
#     print(split_1)
    res_2 = re.split(":", first_split[3])
    print("res_2")
    print(res_2)
    res_0 = re.split("\[", res_2[0])
    print("res_0")
    print(res_0)
    project = res_0[1]
    print("project")
    print(project)
    res_3 = re.split("]",res_2[1])
    print("res_3")
    print(res_3)
    res_4 = re.split(",",res_3[0])
    print("res_4")
    print(res_4)
    changelist = res_4[0]
    print("changelist")
    print(changelist)
    patchset = res_4[1]
    print("patchset")
    print(patchset)
    
    
    
    
    
    


with open('data.json', 'w') as json_file:
    data = []
    json.dump(result_dict, json_file)

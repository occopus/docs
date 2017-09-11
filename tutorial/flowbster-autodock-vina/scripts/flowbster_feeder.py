import requests
import yaml
import sys
import uuid
from datetime import datetime

def printhelp():
    print "Usage: flowbster-feeder.sh [file] [url]"
    print "  file: containing flowbster definition"
    print "  url : endpoint of a flowbster receiver component"

def parse_arguments():
    if len(sys.argv) < 3:
        print "Wrong number of arguments!"
        printhelp()
        return (False,False)
    return (sys.argv[1],sys.argv[2])

def add_time_stamp_to_wfid(content):
    timestamp = datetime.now().strftime('%Y-%m-%d-%H-%M-%S-%f')
    content['wfid'] = timestamp+'-'+content['wfid']
    print "Workflow instance id: "+content['wfid']
    return content

(path,url) = parse_arguments()
if path:
    try:
        file = open(path,'r')
        content = yaml.load(file)
    except Exception as e:
        print "Error when reading file: {0!s}".format(e)
        sys.exit(1)

    content = add_time_stamp_to_wfid(content)

    files = {}
    for arg in sys.argv[3:]:
        print "Adding input file: " + arg
        files[arg] = open(arg, 'rb')
    print 'Files: ' + str(files)
    yaml_id = str(uuid.uuid4())
    payload = {'yaml': yaml_id}
    files[yaml_id] = yaml.dump(content)

    try:
        requests.post(url, files=files, params=payload)
    except requests.exceptions.RequestException as e:
        print "Error when posting message: {0!s}".format(e)
        sys.exit(1)

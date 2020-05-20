import yaml
import os,sys,stat
from flask import Flask
from flask import request
import logging as log

DEF_HOST = '0.0.0.0'
DEF_PORT = 5001
DEF_RESDIR = '/tmp/flowbster/results'
DEF_ROUTEPATH = "/flowbster"
DEF_LOGFILE = "flowbster-gather.log"
DEF_LOGLEVEL = log.DEBUG
DEF_LOGFORMAT = '%(asctime)s\t%(name)s\t%(levelname)s\t%(message)s'


def create_dir(path):
    if not os.path.exists(path): os.makedirs(path)

def gen_filename_by_index(name,indexlist):
    filename = name
    for i in indexlist:
        filename = filename + "_" + str(i)
    return filename

def create_input_files(confjob,directory):
    for d in confjob['inputs']:
        log.debug("- indexes: normal: "+str(d['index'])+" list: "+str(d['index_list']))
        filename = gen_filename_by_index(d['name'],d['index_list'])
        #filename = d['name']+"_"+str(d['index'])
        log.debug("- file to save: \""+filename+"\"")
        if os.path.exists(os.path.join(directory,filename)):
            log.warning("- file \""+filename+"\" already exists! Renaming...")
            ind = 1
            while os.path.exists(os.path.join(directory,filename+"."+str(ind))):
                ind+=1
            filename = filename+"."+str(ind)
        f = request.files[d['name']]
        f.save(os.path.join(directory,filename))
        log.debug("- file saved as \""+filename+"\"")

def deploy(confjob):
    wfidstr = confjob['wfid']
    log.debug("- wfid: "+wfidstr)

    wfiddir = os.path.join(DEF_RESDIR,wfidstr)
    if os.path.exists(wfiddir):
        log.debug("- directory already exists...")
    else:
        create_dir(wfiddir)
    create_input_files(confjob,wfiddir)
    log.info("File collection finished.")


log.basicConfig(filename=DEF_LOGFILE,
		level=DEF_LOGLEVEL,
		format=DEF_LOGFORMAT)
app = Flask(__name__)

@app.route(DEF_ROUTEPATH,methods=['POST'])
def receive():
    log.info("New file(s) arrived.")
    yaml_param = request.args.get('yaml', '')
    rdata = request.files[yaml_param].read()
    confjob = yaml.load(rdata)
    deploy(confjob)
    return "ok"

log.info("Storing results into directory: "+DEF_RESDIR)
log.info("Listening on port "+str(DEF_PORT)+", under url \""+DEF_ROUTEPATH+"\"")

if __name__ == "__main__":
    app.run(host=DEF_HOST,port=DEF_PORT)

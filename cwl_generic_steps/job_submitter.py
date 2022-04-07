import maapypy
import requests
import os
from jinja2 import Environment, FileSystemLoader
import logging

log_format = "[%(asctime)s: %(levelname)s/%(name)s/%(funcName)s] %(message)s"
logging.basicConfig(format=log_format, level=logging.INFO)
logger = logging.getLogger(os.path.splitext(os.path.basename(__file__))[0])

api_dps_url = "https://api.imgspec.org/api/dps/job"


def norm_path(path):
    """Normalize path."""
    return os.path.abspath(os.path.normpath(path))


def create_execute_payload(execute_info):
    # Read in jinja template
    tmpl_file_dir = norm_path(os.path.join(os.path.dirname(__file__), "..", "api_interface_templates"))
    file_loader = FileSystemLoader(tmpl_file_dir)
    env = Environment(loader=file_loader)
    template = env.get_template("wps_execute_request.jinja2.tmpl")
    request = template.render(data=execute_info)
    return request


def parse_execute_response(resp):
    return

def wps_execute(job_info):
    job_id = None
    try:
        # TODO: change this to maappy
        headers = {"Content-type: application/xml"}
        payload = create_execute_payload(execute_info=job_info)
        response = requests.request("POST", api_dps_url, headers=headers, data=payload)
    except Exception as ex:
        raise()
    try:
        # parse response and find job id
        job_id = parse_execute_response(response)
    except Exception as ex:
        raise()
    return job_id


def wps_poll_for_status(job_id):
    # TODO: Implement new maap py handler for polling and use it here
    return

def wps_get_result(job_id):
    # TODO: Call maap py get result
    # check if product generated
    # if nothing then return None
    # else return URL(s)
    return

def main():
    # identify inputs - name of algorithm:version, inputs dictionary
    # parse / read in inputs
    # create the dictionary for execution
    job_info = dict()
    """
        {
            "job_type":"",
            "username":"",
            "resource":"",
            "inputs":{
                  "key":"values"
            }
        }
    """
    # call execute
    job_id = wps_execute(job_info)
    job_status = wps_poll_for_status(job_id)
    if job_status == "successful":
        # get job's result
        result = wps_get_result(job_id)
    elif job_status in ["failed", "dismissed"]:
        raise()
    # formulate output of cwl step
    return output


if __name__ == "__main__":
    main()
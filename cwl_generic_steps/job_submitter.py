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


def wps_execute(job_info):
    headers = {"Content-type: application/xml"}
    payload = create_execute_payload(execute_info=job_info)
    response = requests.request("POST", api_dps_url, headers=headers, data=payload)
    print(response.text.encode('utf8'))


def main():
    # identify inputs - name of algorithm:version, inputs dictionary
    # parse / read in inputs
    # create the dictionary for execution
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
    wps_poll_for_job_status(job_id)


if __name__ == "__main__":
    main()
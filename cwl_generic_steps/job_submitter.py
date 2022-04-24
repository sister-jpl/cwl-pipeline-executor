from maap.maap import MAAP
import requests
import os
import json
from jinja2 import Environment, FileSystemLoader
import logging


log_format = "[%(asctime)s: %(levelname)s/%(name)s/%(funcName)s] %(message)s"
logging.basicConfig(format=log_format, level=logging.INFO)
logger = logging.getLogger(os.path.splitext(os.path.basename(__file__))[0])

api_dps_url = "https://api.imgspec.org/api/dps/job" # TODO: Move this to a config file
maap = MAAP(not_self_signed=False)


def norm_path(path):
    """Normalize path."""
    return os.path.abspath(os.path.normpath(path))


def job_execute(job_info):
    """
    Submit a PGE job and return job id
    :param job_info:
    :return:
    """
    try:
        # get details of job
        algo = job_info.get("job_type").split(":")
        algo_id = algo[0]
        algo_version = algo[1]
        inputs = job_info.get("inputs")
        logger.info("Submitting job {} of version {} \nto queue {} \nwith inputs \n {}".format(
            algo_id, algo_version, job_info.get("resource"), json.dump(inputs)
        ))
        # submit job
        job = maap.submitJob(
            algo_id=algo_id,
            version=algo_version,
            queue=job_info.get("resource"),
            **inputs
        )
        logging.info("Job submission response:\n{}".format(job))
        return job
    except Exception as ex:
        # TODO: Update with chain of exceptions
        raise("Caught Exception submitting job. {}".format(ex))


def wps_poll_for_status(job_id):
    # TODO: Implement new maap py handler for polling and use it here
    job_status = maap.waitForJobCompletion(job_id)
    status = job_status.get("status")
    return status


def wps_get_result(job_id):
    """
    Get the result of a job
    :param job_id:
    :return:
    """
    logger.info("Getting Job Result for job {}".format(job_id))
    job_result = maap.getJobResult(job_id)
    # check if product generated
    logger.info("Result:\n{}".format(job_result))
    outputs = job_result.get("outputs")
    # if nothing then return None
    if len(outputs) > 0:
        return outputs
    else:
        logger.info("No products generated from job")
        return[]


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
    job = job_execute(job_info)
    job.waitForJobCompletion()
    if job.status.lower() == "succeeded":
        # get job's result
        job.getJobResult()
        outputs = job.outputs
        # if nothing then return None
        if len(outputs) == 0:
            logger.info("No products generated from job")
    else:
        if job.status.lower() == "failed":
            raise RuntimeError("Job failed. Traceback:\n{}".format(job.traceback))
        else:
            raise RuntimeError("Job was not successfully completed. Status of job is {}.".format(job.status.lower()))
    # formulate output of cwl step
    result = dict()
    return result


if __name__ == "__main__":
    main()
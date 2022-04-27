import json
import argparse
from maap.maap import MAAP
import os
import json
import logging


log_format = "[%(asctime)s: %(levelname)s/%(name)s/%(funcName)s] %(message)s"
logging.basicConfig(format=log_format, level=logging.INFO)
logger = logging.getLogger(os.path.splitext(os.path.basename(__file__))[0])


maap = MAAP(maap_host="api.imgspec.org")


def job_execute(job_info):
    """
    Sample job_info:
    {
         "algorithm_id": "isofit_ubuntu",
         "version": "v2.9.0",
         "queue": "sister-job_worker-32gb",
         "params": {
          "l1_granule": null,
          "surface_reflectance_spectra": "surface_reflectance_spectra",
          "vegetation_reflectance_spectra": "vegetation_reflectance_spectra",
          "water_reflectance_spectra": "water_reflectance_spectra",
          "snow_and_liquids_reflectance_spectra": "snow_and_liquids_reflectance_spectra",
          "radiance_factors_file": "radiance_factors_file"
         },
         "output_filter": ""
    }
    Submit a PGE job and return job id
    :param job_info:
    :return:
    """
    try:
        # get details of job
        algo_id = job_info.get("algorithm_id")
        algo_version = job_info.get("version")
        inputs = job_info.get("params")
        logger.info("Submitting job {} of version {} \nto queue {} \nwith inputs \n {}".format(
            algo_id, algo_version, job_info.get("queue"), json.dumps(inputs)
        ))
        # submit job
        job = maap.submitJob(
            algo_id=algo_id,
            version=algo_version,
            queue=job_info.get("queue"),
            **inputs
        )
        logging.info("Job submission response:\n{}".format(job))
        return job
    except RuntimeError as err:
        raise ("Runtime error while submitting job. {}".format(err))
    except Exception as ex:
        raise("Caught Exception submitting job. {}".format(ex))


def main(context):
    """
    :param context:
    :return:
    """
    print(f"Running algorithm with params {json.dumps(context, indent=1)}")
    try:
        # call execute
        job = job_execute(context)
        job.waitForJobCompletion()
        if job.status.lower() == "succeeded":
            # get job's result
            job.getJobResult()
            outputs = job.outputs
            # check if any products were created
            if len(outputs) == 0:
                logger.info("No products generated from job")
        else:
            if job.status.lower() == "failed":
                raise RuntimeError("Job failed. Traceback:\n{}".format(job.traceback))
            else:
                raise RuntimeError("Job was not successfully completed. Status of job is {}.".format(job.status.lower()))
        # Create output json of job result
        output_json = {"products": [outputs]}
        # output_json = {"products": ["f130612t01p00r05_rfl.tar.gz"]}
        output_json.update({"output_filter": context.get("output_filter", "")})
        json.dump(output_json, open("output_context.json", 'w'), indent=1)
    except Exception as ex:
        raise Exception("Caught Exception submitting job. {}".format(ex))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run PGE step')
    parser.add_argument("--input_context", dest="input_context", required=True)
    args = parser.parse_args()
    input_context_file = args.input_context
    context = json.load(open(input_context_file, 'r'))
    main(context)

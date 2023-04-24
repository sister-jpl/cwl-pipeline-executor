import argparse
import json
import os
import sys
import logging
import boto3
import re


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)
if LOGGER.hasHandlers():
    LOGGER.handlers.clear()


def evaluate(metadata: list, snow_cover=0.5, veg_cover=0.5, min_pixels=100, soil_cover=0.5, water_cover=0.5, **kwargs):
    LOGGER.info("Evaluating router config")
    algorithms = []
    for meta_file_path in metadata:
        LOGGER.info(f"Processing {meta_file_path}")
        with open(meta_file_path, 'r') as meta_file:
            metadata = json.load(meta_file)

        snow_run = metadata['cover_percentile_counts']['snow'][str(snow_cover)] >= min_pixels
        veg_run = metadata['cover_percentile_counts']['vegetation'][str(veg_cover)] >= min_pixels
        water_run = metadata['cover_percentile_counts']['water'][str(water_cover)] >= min_pixels

        # Vegetation biochemistry PGE
        if veg_run:
            LOGGER.info("Adding veg to pges_to_run")
            algorithms.append("veg")

        # # Snow grain size PGE
        if snow_run & ("DESIS" not in meta_file_path):
            LOGGER.info("Adding snow to pges_to_run")
            algorithms.append("snow")

        if water_run:
            LOGGER.info("Adding water to pges_to_run")
            algorithms.append("water")

    return algorithms


def get_metadata(product_locations):
    metadata = []
    for product_location in product_locations:
        dataset_name = os.path.basename(product_location)
        metadata_file = os.path.join(product_location, f"{dataset_name}.met.json")
        pattern = re.compile(r"s3:\/\/[^\/]+amazonaws.com:80\/(?P<bucket>.*?)\/(?P<key>.+FRCOV.*)")
        match = re.search(pattern, metadata_file)
        if match:
            LOGGER.info(f"Getting metadata file for product {product_location}")
            bucket = match.group("bucket")
            key = match.group("key")
            s3 = boto3.resource("s3")
            metadata_file_path = os.path.join(os.getcwd(), os.path.basename(key))
            LOGGER.info(f"Downloading metfile from bucket: {bucket} key: {key} to location {metadata_file_path}")
            s3.Bucket(bucket).download_file(key, metadata_file_path)
            metadata.append(metadata_file_path)
    return metadata


def main(args):
    pges_to_run = []
    if args.workflow_context is not None:
        workflow_context = json.load(open(args.workflow_context, 'r'))
        config_key = os.path.splitext(os.path.basename(__file__))[0]  # Get filename without extension
        config = workflow_context.get(config_key)
        if args.input_context is not None:
            input_context = json.load(open(args.input_context, 'r'))
            metadata = get_metadata(input_context.get("products", []))
            pges_to_run = evaluate(metadata=metadata, **config)
    LOGGER.info(f"PGEs to run {pges_to_run}")
    print("".join(pges_to_run))


if __name__ == "__main__":
    agrparse = list()
    desc = "SISTER Algorithm router"
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('--workflow_context',
                        help='Workflow Context')
    parser.add_argument('--input_context',
                        help='Input context')
    args = parser.parse_args()
    main(args)

"""
Patch to add missing distance entry on all 0m recordings.
The to_insert object is added to the matching jsons.
"""
import glob
import json
import logging
import sys

to_insert = {
    "distance": {
        "version": "1",
        "distanceKey": "0m",
        "distanceKeys": [
            "50cm",
            "0m",
            "CREDIT_H",
            "CREDIT_V",
            "A4_H",
            "A4_V",
            "SMALL_PERSON_SHOULDER_MAX",
            "MEDIUM_PERSON_SHOULDER_MAX",
            "SMALL_PERSON_ARM_MAX",
            "MEDIUM_PERSON_ARM_MAX"
        ]
    }
}

DIRECTORY = '/home/michigg/GIT/uni/2021-MA-Michael-Goetz-data/data/FrogsCalibration/Test3/Original/DistanceKey_0m'

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s]:\n %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)


def patch(directory: str):
    file_paths = glob.glob(f'{directory}/**/*.json', recursive=True)
    logger.info(f'load_analysis: Found {len(file_paths)} files.')
    for path in file_paths:
        logger.info(f'load_analysis: load: {path}')
        with open(path) as file:
            json_data = json.load(file)
            logger.info(f'load_analysis: loaded: {path}')
            json_data["distance"] = to_insert["distance"]
            with open(path, mode='w', encoding='utf-8') as write_file:
                json.dump(json_data, write_file, ensure_ascii=False, indent=2)
                logger.info(f'load_analysis: saved: {path}')


if __name__ == '__main__':
    patch(DIRECTORY)

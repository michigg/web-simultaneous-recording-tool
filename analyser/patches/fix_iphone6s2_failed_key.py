"""
Patch to fix recordings with the wrong device key IPHOSE6S2.
The deviceName entry is changed from IPHOSE6S2 to IPHONE6S2.
"""
import glob
import json
import logging
import sys

DIRECTORY = '/home/michigg/GIT/uni/2021-ma-michael-goetz-data/FrogsCalibration/Test2/Original'

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s]:\n %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(f"{DIRECTORY}/patch2.log", mode='w'),
    ]
)


def patch(directory: str):
    file_paths = glob.glob(f'{directory}/**/*.json', recursive=True)
    logger.info(f'load_analysis: Found {len(file_paths)} files.')
    for path in file_paths:
        # logger.info(f'load_analysis: load: {path}')
        with open(path) as file:
            json_data = json.load(file)
            if json_data["local"]["deviceName"] == "IPHOSE6S2":
                logger.info(f'load_analysis: wrong device name found: {path}')
                json_data["local"]["deviceName"] = "IPHONE6S2"

                with open(path, mode='w', encoding='utf-8') as write_file:
                    json.dump(json_data, write_file, ensure_ascii=False, indent=2)
                    logger.info(f'load_analysis: saved: {path}')


if __name__ == '__main__':
    patch(DIRECTORY)

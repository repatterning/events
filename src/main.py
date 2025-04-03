"""Module main.py"""
import datetime
import logging
import os
import sys

import boto3


def main():
    """
    Entry Point

    :return:
    """

    logger: logging.Logger = logging.getLogger(__name__)
    logger.info('Starting: %s', datetime.datetime.now().isoformat(timespec='microseconds'))

    # Assets
    src.assets.Assets(s3_parameters=s3_parameters).exc()

    specifications_ = src.data.interface.Interface(s3_parameters=s3_parameters).exc()
    src.drift.interface.Interface(arguments=arguments).exc(specifications_=specifications_)
    src.predictions.interface.Interface().exc(specifications_=specifications_)

    # Transfer
    src.transfer.interface.Interface(
        connector=connector, service=service, s3_parameters=s3_parameters).exc()

    # Delete Cache Points
    src.functions.cache.Cache().exc()


if __name__ == '__main__':

    # Paths
    root = os.getcwd()
    sys.path.append(root)
    sys.path.append(os.path.join(root, 'src'))

    # Logging
    logging.basicConfig(level=logging.INFO,
                        format='\n\n%(message)s\n%(asctime)s.%(msecs)03d\n',
                        datefmt='%Y-%m-%d %H:%M:%S')

    # Modules
    import src.assets
    import src.data.interface
    import src.drift.interface
    import src.elements.service as sr
    import src.elements.s3_parameters as s3p
    import src.functions.cache
    import src.predictions.interface
    import src.preface.interface
    import src.transfer.interface

    connector: boto3.session.Session
    s3_parameters: s3p
    service: sr.Service
    arguments: dict
    connector, s3_parameters, service, arguments = src.preface.interface.Interface().exc()

    main()

"""Module metrics.py"""
import json
import os

import numpy as np
import pandas as pd

import config
import src.elements.parts as pr
import src.elements.specifications as se
import src.functions.objects


class Metrics:
    """
    Metrics
    """

    def __init__(self):
        """
        Constructor
        """

        self.__configurations = config.Config()
        self.__path = os.path.join(self.__configurations.points_, 'errors')

        self.__objects = src.functions.objects.Objects()

    @staticmethod
    def __root_mse(data: pd.DataFrame) -> pd.DataFrame:
        """
        This function calculates
            square root (mean ( a set of square errors ) )
        per set of square errors.

        :param data:
        :return:
        """

        square_error: np.ndarray = np.power(data['error'].to_numpy(), 2)
        mse: np.ndarray = np.expand_dims(
            np.sum(square_error, axis=0)/square_error.shape[0], axis=0)

        frame = pd.DataFrame(data=np.sqrt(mse),
                             columns=['errors'], index=['r_mse'])

        return frame

    @staticmethod
    def __pe(data: pd.DataFrame) -> pd.DataFrame:
        """

        :param data:
        :return:
        """

        er: np.ndarray = data['p_error'].to_numpy()
        tiles: np.ndarray = np.percentile(a=er, q=[10, 25, 50, 75, 90], axis=0)
        frame = pd.DataFrame(data=tiles, columns=['errors'],
                             index=['l_whisker', 'l_quarter', 'median', 'u_quarter', 'u_whisker'])

        return frame

    def __get_metrics(self, data: pd.DataFrame) -> dict:
        """

        :param data:
        :return:
        """

        frame = pd.concat((self.__root_mse(data=data), self.__pe(data=data)),
                          axis=0, ignore_index=False)
        string = frame.to_json(orient='split')

        return json.loads(string)

    def exc(self, parts: pr.Parts, specifications: se.Specifications) -> str:
        """

        :param parts:
        :param specifications:
        :return:
        """

        nodes = {
            'training': self.__get_metrics(data=parts.training),
            'testing': self.__get_metrics(data=parts.testing)}

        spe = specifications._asdict()
        for value in ['station_id', 'catchment_id', 'ts_id']:
            spe[value] = int(spe.get(value))
        nodes.update(spe)

        message = self.__objects.write(nodes=nodes, path=os.path.join(self.__path, f'{specifications.ts_id}.json'))

        return message

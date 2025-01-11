import dask
import pandas as pd

import config
import src.elements.partitions as prt


class Partitions:

    def __init__(self, data: pd.DataFrame):
        """
        'station_id', 'catchment_id', 'catchment_name', 'ts_id', 'ts_name', 'from', 'to',
        'stationparameter_no', 'parametertype_id', 'station_latitude', 'station_longitude', 'river_id',
        'catchment_size', 'gauge_datum'

        :param data:
        """

        self.__data = data

        # Fields
        self.__fields = ['ts_id', 'period', 'catchment_size', 'gauge_datum', 'on_river']

        # Configurations
        self.__configurations = config.Config()

    @dask.delayed
    def __matrix(self, period: str) -> list:
        """

        :param period:
        :return:
        """

        data = self.__data.copy()

        data = data.assign(period = str(period))
        records: pd.DataFrame = data[self.__fields]
        objects: pd.Series = records.apply(lambda x: prt.Partitions(**dict(x)), axis=1)

        return objects.tolist()

    def exc(self) -> list:
        """

        :return:
        """

        frame = pd.date_range(start=self.__configurations.starting, end=self.__configurations.at_least, freq='MS'
                              ).to_frame(index=False, name='date')
        periods: pd.Series = frame['date'].apply(lambda x: x.strftime('%Y-%m-%d'))

        computations = []
        for period in periods.values:
            matrix = self.__matrix(period=period)
            computations.append(matrix)
        calculations = dask.compute(computations, scheduler='threads')[0]

        return sum(calculations, [])

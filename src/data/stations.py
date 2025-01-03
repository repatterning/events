
import logging

import src.elements.text_attributes as txa
import src.functions.objects
import src.functions.streams


class Stations:

    def __init__(self):

        self.__uri = (
            'https://timeseries.sepa.org.uk/KiWIS/KiWIS?service=kisters&type=queryServices&datasource=0'
            '&request=getstationlist&returnfields=station_no,station_name,stationparameter_name,'
            'stationparameter_no,catchment_id,catchment_no,catchment_name,station_latitude,station_longitude,'
            'station_carteasting,station_cartnorthing,river_id,river_name,ca_sta&'
            'ca_sta_returnfields=CATCHMENT_SIZE,GAUGE_DATUM,GROUND_DATUM,GWREF_DATUM&object_type=General&format=csv')

        self.__streams = src.functions.streams.Streams()

    def exc(self):
        """
        logging.info(data[['catchment_id', 'catchment_no', 'catchment_name']].drop_duplicates())

        :return:
        """

        text = txa.TextAttributes(uri=self.__uri, header=0, sep=';')
        data = self.__streams.api(text=text)
        data.info()

        frequency = data[['catchment_id', 'catchment_no', 'catchment_name']].groupby(
            by=['catchment_id', 'catchment_no', 'catchment_name']).value_counts()
        logging.info(frequency)

        logging.info(data.loc[data['catchment_no'] == 83, :])

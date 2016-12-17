#-- Libraries --
import os, sys
import json
import os.path as osp

# -- Configuration base, for all environments --
class Config(object):
    ###############################################################################
    # Configuration Overall
    #
    # :param object:                The application object
    ###############################################################################

    ##########################################
    # DB
    ##########################################
    DB_PATH = 'mongodb://localhost:27017/'
    DB_DATE_FORMAT = '%Y-%m-%d'  #All field values have to be str in DB, 
                                 #  so data format has to be defined here.
    DB_COL_DAILY_STOCK = 'dailyStock'

    ##########################################
    # Directory to store data
    ##########################################
    ROOT_DIR = osp.dirname(__file__)
    DATA_DIR = osp.join(ROOT_DIR, "../data")

    ##########################################
    # Module dirs
    ##########################################
    MODULE_DIRS =  [
        osp.join(ROOT_DIR, './data_gainers'), 
        osp.join(ROOT_DIR, './utils'       ),
        osp.join(ROOT_DIR, './controllers' ),
        osp.join(ROOT_DIR, './test'        )
    ]

    ##########################################
    # Parameters for each gainers
    # [Causion]
    #   - All fields in each line have to be str 
    #       when they inserted into DB.
    ##########################################
    GAINER_PARAMS = {
        'geocities': {
            'data_gainers': 'data_gainer_geocities',
            'db_id': 'geocities',
            'db_columns': {   #(Key in Program) : (Key in DB)
                'dayily_stock': {
                    'stock_id'   : {'order': 0, 'field_name': 'stock_id'},
                    'date'       : {'order': 1, 'field_name': 'date'    },
                    'open_price' : {'order': 2, 'field_name': 'open'    },
                    'high_price' : {'order': 3, 'field_name': 'high'    },
                    'low_price'  : {'order': 4, 'field_name': 'low'     },
                    'close_price': {'order': 5, 'field_name': 'close'   },
                    'adjusted'   : {'order': 6, 'field_name': 'adjusted'}
                    }
                },
            # 'raw_data_keys': {
            #     'dayily_stock': [
            #         'stock_id',
            #         'date',
            #         'open',
            #         'high',
            #         'low',
            #         'close',
            #         'adjusted'
            #         ]
            #     },
            'test_module_name': 'test_geocities'
            },
        'wikiPrices': {
            'data_gainers': 'data_gainer_wikiPrices',
            'db_id': 'wikiPrices',
            'db_columns': {   #(Key in Program) : (Key in DB) in order
                'dayily_stock': {  
                    'stock_id'   : {'order':  0, 'field_name': 'stock_id'    },
                    'date'       : {'order':  1, 'field_name': 'date'        },
                    'open_price' : {'order':  2, 'field_name': 'open'        },
                    'high_price' : {'order':  3, 'field_name': 'high'        },
                    'low_price'  : {'order':  4, 'field_name': 'low'         },
                    'close_price': {'order':  5, 'field_name': 'close'       },
                    'volume'     : {'order':  6, 'field_name': 'volume'      },
                    'ex-dividend': {'order':  7, 'field_name': 'ex-dividend' },
                    'split_ratio': {'order':  8, 'field_name': 'split_ratio' },
                    'adj_open'   : {'order':  9, 'field_name': 'adj_open'    },
                    'adj_high'   : {'order': 10, 'field_name': 'adj_high'    },
                    'adj_low'    : {'order': 11, 'field_name': 'adj_low'     },
                    'adj_close'  : {'order': 12, 'field_name': 'adj_close'   },
                    'adj_volume' : {'order': 13, 'field_name': 'adj_volume'  }
                    }
                },
            # 'raw_data_keys': {   #Key of columns in CSV file in order
            #     'dayily_stock': [
            #         'ticker',
            #         'date',
            #         'open',
            #         'high',
            #         'low',
            #         'close',
            #         'volume',
            #         'ex-dividend',
            #         'split_ratio',
            #         'adj_open',
            #         'adj_high',
            #         'adj_low',
            #         'adj_close',
            #         'adj_volume'
            #         ]
            #     },
            'test_module_name': 'test_wikiPrices'
            }
        }

    ##########################################
    # Others
    ##########################################
    DEBUG = False



# -- Production Configuration --
class ProductionConfig(Config):
    ###############################################################################
    # Configuration for Production
    #
    # :param object:                The application object
    ###############################################################################
    DEBUG = False


# -- Development Configuration --
class DevelopmentConfig(Config):
    ###############################################################################
    # Configuration for Development
    #
    # :param object:                The application object
    ###############################################################################
    DEBUG = True

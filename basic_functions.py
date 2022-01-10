import yaml

try:
    credentials_file = '../credentials.yaml'
    paths_file = '../source_path.yaml'
except:
    credentials_file = 'credentials.yaml'
    paths_file = 'source_path.yaml'

credentials = yaml.safe_load(open(credentials_file))

class telegram_msg():
    def __init__(self):
        import requests
        import os
        import json


        cred_type = 'twitter_musk'
        self.bot_token =  credentials[cred_type]['bot_token']
        self.bot_chat_id = credentials[cred_type]['bot_chat_id']
        self.bearer_token = credentials[cred_type]['bearer']

    def create_headers(bearer_token):
        headers = {"Authorization": "Bearer {}".format(bearer_token)}
        return headers


    def telegram_bot_sendtext(self,bot_message):
        print('bot message:' + bot_message)
        send_text = 'https://api.telegram.org/bot' + self.bot_token + '/sendMessage?chat_id=' + self.bot_chat_id + '&parse_mode=Markdown&text=' + bot_message
        response = self.requests.get(send_text)
        return response.json()
class use_db:
    def __init__(self):
        import sqlalchemy
        credentials = yaml.safe_load(open(credentials_file))
        self.paths = yaml.safe_load(open(paths_file))
        cred_type = 'db_import'
        db = credentials[cred_type]['db']
        user = credentials[cred_type]['user']
        host = credentials[cred_type]['host']
        pw = credentials[cred_type]['pw']
        self.engine = sqlalchemy.create_engine("postgresql://{user}:{pw}@{host}/{db}"
                                          .format(host=host,
                                                  db=db,
                                                  user=user,
                                                  pw=pw))

        try:
            self.connection = self.engine.connect()
 #           logger.debug('connected to server')
            print('connected to server')
        except Exception as e:
  #          logger.error('not connected to server '+ str(e))
            print('not connected to server ' + str(e))
            raise
    def execute_insert(self,sql_str, vals):
        self.connection.execute(sql_str, vals)
    def send_to_db(self, dataset, etl_process):

        try:
            table_name = self.paths[etl_process]['dwh_table_name']
        except:
            table_name = etl_process
   #         logger.info('using etl_process as name ' + etl_process)

        try:
            dataset.to_sql('load_' + table_name, schema='etl', con=self.engine, if_exists='replace', chunksize=10000,
                           index=False)
    #        logger.debug('sucessfully updated')
            print('sucessfully updated')
        except Exception as e:
            print(  ' refresh failed ' + str(e))
 #           logger.error(filename + ' refresh failed ' + str(e))
            raise
    def modify_in_db(self, table_name = 'classic'):
        print(table_name)
        modify_file =  self.paths[table_name]['modify_sql']
        with open("sql_part/"+ str(modify_file), "r") as f:
            modify = f.read()
        sql_text= modify.format(table_name)

        try:
            self.connection.execute(sqlalchemy.text(sql_text
                                               ).execution_options(autocommit=True))
#            logger.debug('sucessfully truncated')
            print('sucessfully truncated')
        except Exception as e:
            print( ' truncating failed ' + str(e))
#            logger.error(filename + ' truncating failed ' + str(e))
            raise

    def get_conn(self):
        return self.connection

    def read_db(self, sql_text):
        import pandas as pd
        df = pd.read_sql_query(sql_text, self.connection)
        return df
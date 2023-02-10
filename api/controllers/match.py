from flask_restful import Resource
from flask import request

import pandas as pd
from postgres_database_utils import PostgresCredentials, create_connection
import os
from dotenv import load_dotenv

load_dotenv()


class Match(Resource):
    def __init__(self: 'Match') -> None:
        pass

    def get(self: 'Match') -> dict:
        personality = request.args.get('personality')
        genre = request.args.get('genre')

        query_books = '''
            SELECT book_title
            FROM books
            WHERE personality = %s
            AND genre = %s;
        '''

        credentials = PostgresCredentials(
            host=os.environ.get('DATABASE_HOST'),
            database=os.environ.get('DATABASE_NAME'),
            user=os.environ.get('DATABASE_USER'),
            password=os.environ.get('DATABASE_PASSWORD'),
        )
        connection = create_connection(credentials)

        results = pd.read_sql(query_books, connection, params=(personality, genre))
        connection.close()
        return [book['title'] for book in results]

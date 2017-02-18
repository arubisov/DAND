#!/usr/bin/env python
''' Use these functions to interact with the MongoDB '''


def get_db(db_name):
    from pymongo import MongoClient
    client = MongoClient('localhost')
    db = client[db_name]
    return db


def make_pipeline():
    # complete the aggregation pipeline
    pipeline = [{'$match': {'name': {'$ne': None}}},
                {'$group': {'_id': '$name',
                            'count': {'$sum': 1}}},
                {'$sort': {'count': -1}},
                {'$limit': 1}]
    return pipeline


def aggregate(db, pipeline):
    return [doc for doc in db.toronto.aggregate(pipeline)]


if __name__ == '__main__':
    # The following statements will be used to test your code by the grader.
    # Any modifications to the code past this point will not be reflected by
    # the Test Run.
    db = get_db('udacity')
    pipeline = make_pipeline()
    result = aggregate(db, pipeline)
    import pprint
    pprint.pprint(result[0])
# Of the nodes in this dataset, which extends beyond the municipal boundaries
# of the City of Toronto, what proportion fall into which township?

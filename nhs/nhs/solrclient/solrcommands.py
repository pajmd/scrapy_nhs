#  python 3.4 >
from enum import Enum


class SolrOp(Enum):
    ADMIN = 1,
    CREATE_COLLECTION = 2
    DELETE_COLLECTION = 3
    SCHEMA = 10,
    ADD_FIELD = 11

OP = {
    SolrOp.ADMIN: [
        SolrOp.CREATE_COLLECTION,
        SolrOp.DELETE_COLLECTION
    ]
}
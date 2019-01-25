#
# Playground
#
from openpyxl import load_workbook
from parsers.parser import DrugPartMParser
import pymongo

VALIDATION_SCHEMA = {
    'validator': {
        '$jsonSchema': [
            {'bsonType': "object"},
            {'required': ["category", "Formulations", "Medicine", "unit", "period", "Pack_Size", "VMPP_Snomed_Code",
                          "Basic_Price"]},
            {'properties': {
                'Medicine': [
                    ('bsonType', "string"),
                    ('description', "must be a string and is required")
                ],
                'Basic_Price': [
                    ('bsonType', "float"),
                    ('description', "must be a float and is required")
                ]
            }
            }
        ]
    }
}

VALIDATION_SCHEMA = {
   "validator": {
    "$jsonSchema": {
      "bsonType": "object",
      "required": [ "name", "surname", "email" ],
          "properties": {
             "name": {
                "bsonType": "string",
                "description": "required and must be a string" },
             "surname": {
                "bsonType": "string",
                "description": "required and must be a string" },
             "email": {
                "bsonType": "string",
                "pattern": "^.+\@.+$",
                "description": "required and must be a valid email address" },
             "year_of_birth": {
                "bsonType": "int",
                "minimum": 1900,
                "maximum": 2018,
                "description": "the value must be in the range 1900-2018" },
             "gender": {
                "enum": [ "M", "F" ],
                "description": "can be only M or F" }
          }
       }
    }
}

def test_read_write_json():
    filename = '/home/pjmd/tmp/nhs/files/full/0e4dc9e7b9df4605cf22507649bed02d7b3cc541.xlsx'
    wb = load_workbook(filename=filename, read_only=True)
    active_sheet = wb.active
    # for row in active_sheet.rows:
    #     listrow = (cell.value for cell in active_sheet.rows)
    # for row in active_sheet.rows:
    arow = [[cell.value for cell in row] for row in active_sheet.rows]
    print(arow)


def test_parsing():
    s = ''
    ns = None
    rc = s is False
    rc = not s
    rc = ns is False
    rc = not ns

    filename = '/home/pjmd/tmp/nhs/files/full/0e4dc9e7b9df4605cf22507649bed02d7b3cc541.xlsx'
    parser = DrugPartMParser(filename)
    jobj = parser.parsexls()
    print(jobj)


# good read: https://www.percona.com/blog/2018/08/16/mongodb-how-to-use-json-schema-validator/
# db.getCollectionInfos( {name: "c1"} ) to show the schema
def test_mongo():
    client = pymongo.MongoClient('mongodb://127.0.0.1:27017/')
    db = client['myNewDB']
    collection_list = db.command('listCollections', filter={'name': 'myNewDB'}, nameOnly=True)
    # collection_list = db.command('listCollections', filter={'type': 'collection'}, nameOnly=True)
    print(collection_list)
    names = db.collection_names()
    print(names)
    collection_name = 'c1'
    if collection_name in db.list_collection_names():
        validate_col_cmd = {
            'collMod': collection_name
        }
        validate_col_cmd.update(VALIDATION_SCHEMA)
        db.command(validate_col_cmd)
    else:
        db.create_collection(collection_name, **VALIDATION_SCHEMA)

    print('stuff')


def test_ext():
    import os
    filename = '/home/pjmd/tmp/nhs/files/full/0e4dc9e7b9df4605cf22507649bed02d7b3cc541.xlsx'
    file, file_extension = os.path.splitext(filename)
    print(file, file_extension)

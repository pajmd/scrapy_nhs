FROM_PATH = '/home/pjmd/tmp/nhs/files/csv'
TO_PATH = '/home/pjmd/tmp/nhs/files/json'

FS = 'FS'
MONGO = 'MONGO'
MEDIUM = 'FS'
MONGO_CONNECTOR = 'MONGO_CONNECTOR'

SOURCE_DESTINATION = {
    FS: (FROM_PATH, TO_PATH,),
    MONGO: (FROM_PATH, MONGO_CONNECTOR,)
}

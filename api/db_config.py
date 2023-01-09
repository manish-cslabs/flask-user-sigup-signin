# mysql://username:password@host:port/database_name
env = "production"
# env = "local"


db_config = {
    "host": "localhost:3306",
    "username": "root",
    "password": "password",
    "database_name": "test_db_manish",
}


server_db = {
    "host": "los-test-db.mysql.database.azure.com",
    "username": "csladmin@los-test-db",
    "password": "csLabs$2019",
    # "database_name": "csl_ds_model_ai",
    "database_name": "testdb_manish",
    "port": 3306
}

if (env == "production"):
    db_config = server_db

db_uri = f"mysql+pymysql://{db_config['username']}:{db_config['password']}@{db_config['host']}/{db_config['database_name']}"



# db_uri = 'mysql+pymysql://root:password@localhost:3306/testDB'
# db_uri = f"mysql+pymysql://{username}:{password}@{host}/{database_name}"

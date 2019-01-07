# startup mongo server
mongod --dbpath .../mongodb/data/ishmael/db0

# shell access: connect server default port
mongo
use malwaredb

# start ishmael server
export ISHMAEL_CONFIG=ConfigDev
python ./run.py

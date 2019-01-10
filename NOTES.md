# startup mongo server
mongod --dbpath /path/to/mongodb  

# shell access: connect server default port
mongo  
use malwaredb  

# start ishmael server
export ISHMAEL_CONFIG=ConfigDev  
python ./run.py  

# server web console
http://localhost:28017/  

# browse Ishmael
http://localhost:5000  

# load records mongodb
mongod --dbpath /path/to/db  
cd /path/to/ishmael_repo/scripts  
export ISHMAEL_CONFIG=ConfigDev  
python make_random_urls.py NumberOfBaseRecords SourceID  


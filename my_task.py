def main(dateStart,dateEnd):
    
    ###########################################################################
    # User input for PostgreSQL database
    user = "michal"
    passwd = "Cl0udF3rr0!"
    host= "127.0.0.1" #localhost
    dbMainName = "SENTINEL_DATA"   
    ###########################################################################
    
    from psycopg2 import connect, OperationalError
    from requests import get
    from re import match
    from random import randint
    from hashlib import md5
    from os.path import join, expanduser, exists
    from zipfile import ZipFile 
    from shutil import rmtree
    from os import mkdir
    import dateutil.parser
    
    # Detect wrong date input if occurs
    pattern_date_time = '\d\d\d\d-\d\d-\d\dT\d\d:\d\d:\d\d.\d\d\dZ'
    if not match(pattern_date_time, dateEnd) and match(pattern_date_time, dateStart):
        print("Wrong date input. Please use ISO8601 format: yyyy-MM-ddThh:mm:ss.SSSZ.")
        return None
    elif (dateutil.parser.parse(dateEnd)-dateutil.parser.parse(dateStart)).days >= 4:
        print("Wrong date input. Daterange greater than maximum (max = 4 days).")
        return None
    
    # Create work folder
    workFolder = join(expanduser('~'),'CFdata')
    if exists(workFolder):
        rmtree(workFolder)
    mkdir(workFolder)       
    print("Work folder created...")
     
    # Connecting to PostgreSQL database
    try:
        cnx = connect(user=user, password=passwd, host=host, database=dbMainName)
        cursor = cnx.cursor()
        print("Database connection succeessful...")
    except OperationalError:
        print("Connection failed.")

    # Create table with results
    cursor.execute("""CREATE TABLE results (
        file_id SERIAL PRIMARY KEY,
        file_name VARCHAR(255) NOT NULL,
        file_path VARCHAR(255) NOT NULL,
        md5sum VARCHAR(32) NOT NULL
        );""")    
       
    # Download 3 random products
    userAndPassword = ('michal_rabinski','S3nt1nelD@t@R0cK!')
    for i in range(1,4):
        prodQuery = "https://scihub.copernicus.eu/dhus/search?start={}&rows={}&q=beginposition:[{} TO {}] AND endposition:[{} TO {}]".format(
                            randint(1,1000),1,dateStart,dateEnd,dateStart,dateEnd)
        dataQuery = get(prodQuery, auth=userAndPassword).text
        fileName = "Sentinel_product{}.xml".format(i)
        with open(join(workFolder,fileName), 'w+') as f:
            f.write(dataQuery)
            print("{} downloaded...".format(fileName))
            # Get md5 sum
            md5sum = md5(dataQuery.encode()).hexdigest()
            cursor.execute("""INSERT INTO results (file_name, file_path, md5sum)
            VALUES ('{}', '{}', '{}');""".format(fileName,prodQuery,md5sum))            
      
    # Commit the changes to database
    cnx.commit()
    
    # Export results.csv
    with open(join(workFolder,"results.csv"), "w+") as f:
        cursor.copy_expert("COPY results TO STDOUT WITH CSV DELIMITER ','", f)   
        print("results.csv exported...") 
    
    # Export timerange.txt
    with open(join(workFolder,"timerange.txt"), 'w+') as f:
        f.write("Log file.\n--Selected daterange:\nFrom {}\nTo {}".format(dateStart,dateEnd))
        print("timerange.txt exported...")
        
    # Create zip with source coude, results.csv and timerange.txt
    zf = ZipFile(join(workFolder,"Michal_Rabinski.zip"), "w")
    zf.write(__file__, arcname = "my_task.py")
    zf.write(join(workFolder,"results.csv"), arcname = "results.csv")
    zf.write(join(workFolder,"timerange.txt"), arcname = "timerange.txt")  
    print("Zip file ({}) created...".format("Michal_Rabinski.zip"))        

    # Close connection to database and cursor
    cursor.close()
    cnx.close()
    print("All tasks performed successfully.") 

if __name__ == "__main__":
    import sys
    main(sys.argv[1],sys.argv[2])
import sqlite3
import sys
import os

from numpy import dtype

def create_schema(df):
    schema = df.dtypes
    for i, _ in enumerate(schema):
        if _ == dtype('object'):
            schema[i] = 'TEXT'
        elif _ == dtype("int32") or _ == dtype("int64"):
            schema[i] = 'INT'
        elif _ == dtype('float32') or _ == dtype('float64'):
            schema[i] = 'FLOAT'
    return schema


def generate_colname_query(names, schema, tablename):
    name_schema_pair = zip(*(names, schema))
    name_schema_pair = [' '.join(pair) for pair in name_schema_pair]

    query = 'CREATE TABLE {} ({})'.format(tablename ,', \n'.join(name_schema_pair))
    return query


def generate_insert_query(tablename, line, schema):
    line = [str(line[i]) 
            if schema[i] != "TEXT" 
            else '"{}"'.format(str(line[i]))
            for i in range(len(line))]
    
    expr = "INSERT INTO {} VALUES ({})".format(tablename, ','.join(line))
    return expr



if __name__ == "__main__":

    from pandas import read_csv, read_excel
    import re

    filename = sys.argv[1]
    tablename = re.sub(r'\.csv|\.xlsx', '', filename)
    dbname = './db/project' + '.db'
    logfile = open(tablename+'.log', 'w', encoding='utf-8')

    if os.path.exists(dbname):
        if_recreate = input('db already exists, do you want to insert table [y/n]> ')
        if_recreate = if_recreate.lower()
        if if_recreate == 'y':
            pass
        else:
            raise(FileExistsError)



    if "csv" in filename:
        df = read_csv(filename)
    elif 'xlsx' in filename:
        df = read_excel(filename)

    else:
        print('filename error: should be csv or excel file')
        raise(FileNotFoundError)

    
    schema = create_schema(df)

    expr_create_db = generate_colname_query(df.columns, schema, tablename)
    logfile.write('./log/' + expr_create_db)
    logfile.write('\n'+'-'*40+'\n')

    #print(expr_create_db)
    conn = sqlite3.connect(dbname)
    cursor = conn.cursor()
    cursor.execute(expr_create_db)
    for i in range(len(df)):
        

        line = df.iloc[i, :]
        insert_expr = generate_insert_query(tablename, line, schema)
        logfile.write(insert_expr)
        
        print(insert_expr)
        try:
            cursor.execute(insert_expr)
        except sqlite3.OperationalError:
            logfile.write('\tERROR')
        logfile.write('\n')

        


    conn.commit()
    conn.close()


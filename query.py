import sqlite3
import pandas as pd

db = sqlite3.connect('./db/project.db')
conn = db.cursor()



if __name__ == "__main__":
    query = """
    SELECT h1.stock_title, h1.holding, h2.stock_title, h2.holding
    FROM holding as h1, holding as h2
    WHERE h1.abbrivate_funds = h2.abbrivate_funds AND h1.stock_title != h2.stock_title
    
    
    """


    conn.execute(query)
    data = conn.fetchall()
    print(data[0])
    df = pd.DataFrame(data, columns = ['stock_title1', 'holding1', 'stock_title2', 'holding2'])
    df.to_csv('co_investment_network_stock.csv')
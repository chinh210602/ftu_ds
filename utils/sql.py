import mysql.connector
from mysql.connector import Error
from datetime import datetime

class MySQL():
    def __init__(self, host_name, user_name, user_password):
        self.host_name = host_name
        self.user_name = user_name
        self.user_password = user_password

    def connect_database(self, db_name):
        self.connection = None
        try:
            self.connection = mysql.connector.connect(
            host = self.host_name,
            user = self.user_name,
            passwd = self.user_password,
            database = db_name
        )
            print("MySQL Database connection successful")
        except Error as err:
            print(f"Error: '{err}'")
            
    def execute_query(self, query):
        cursor = self.connection.cursor(buffered=True)
        try:
            cursor.execute(query)
            self.connection.commit()
            print("Query successful")
        except Error as err:
            print(f"Error: '{err}'")
    
    def read_query(self, query):
        cursor = self.connection.cursor()
        result = None
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except Error as err:
            print(f"Error: '{err}'")
    
    def execute_list_query(self, query, val):
        cursor = self.connection.cursor()
        try:
            cursor.executemany(query, val)
            self.connection.commit()
            print("Query successful")
        except Error as err:
            print(f"Error: '{err}'")

    def get_annually_spending(self, freq, from_, to):
        query_daily = f"""
                SELECT date, sum(amount)
                FROM spending
                WHERE date >= "{from_}" AND date <= "{to}"
                GROUP BY date
                """
        if freq == "Hằng Ngày":
            results = self.read_query(query_daily)
            amount = []
            date = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

            for result in results:
                amount.append(result[1]/1000)

            return date, amount

        else:
            return None
        
    def get_daily_expenses_by_type(self, date):
        query = f"""
                SELECT date, sum(amount), type
                FROM spending
                WHERE date = "{date}"
                GROUP BY type
                """
        results = self.read_query(query)
        amount = []
        type_ = []
        if results:
            for result in results:
                amount.append(result[1])
                type_.append(result[2])
            
            return amount, type_

        else: 
            type_.append("None")
            amount.append(0)

        return amount, type_
    
    def get_total_spending(self):
        today = datetime.strptime('2023-09-12','%Y-%m-%d')
        first_day = today.replace(day = 1)
        today = str(today).split()[0]
        first_day = str(first_day).split()[0]
        query_spending =    """
                            SELECT sum(amount) FROM spending
                            WHERE date >= 2023-09-11 and date <= 2023-09-12
                            """
        query_income =  f"""
                        SELECT sum(amount) FROM income
                        WHERE date >= "{first_day}" and date <= "{today}"
                        """
        return self.execute_query(query_spending), self.execute_query(query_income)

if __name__ == '__main__':
    my_sql = MySQL("localhost", "root", "chinh210602")
    my_sql.connect_database("ds_ftu")
    today = datetime.strptime('2023-09-12','%Y-%m-%d')
    print(my_sql.get_total_spending())
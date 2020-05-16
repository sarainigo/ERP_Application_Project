#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 12:19:29 2020

@author: Sara
"""

import psycopg2
from psycopg2 import Error
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import numpy as np
from datetime import date
import matplotlib.pyplot as plt
import seaborn as sns


def getValues(user, user_pw, table_name):
    try:
        connection = psycopg2.connect(user = user,
                                      password = user_pw,
                                      host = "localhost",
                                      port = "5432",
                                      database = "erpapplication")

        print("Using Python variable in PostgreSQL select Query")
        cursor = connection.cursor()
        postgreSQL_select_Query = "select * from "
        postgreSQL_select_Query = postgreSQL_select_Query + table_name

        cursor.execute(postgreSQL_select_Query)
        records = cursor.fetchall()
        names = cursor.description
        columns = []
        for i in range(0, len(names)):
            columns.append(names[i][0])
        df = pd.DataFrame(records, columns = columns)
        
        print(df)


    except (Exception, psycopg2.Error) as error:
        print("Error fetching data from PostgreSQL table: ", error)

    finally:
        # closing database connection
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed \n")

# getValues('admin','123_admin','Employee')
# getValues('sales','123_sales','Employee')


def InsertValues(user, user_pw, table_name, values):
    try:
        connection = psycopg2.connect(user = user,
                                      password = user_pw,
                                      host = "localhost",
                                      port = "5432",
                                      database = "erpapplication")
        cursor = connection.cursor()
        sql_insert_query = " insert into "
        sql_insert_query = sql_insert_query + table_name
        sql_insert_query = sql_insert_query + " values "
        sql_insert_query = sql_insert_query + str(values)
    
        cursor.execute(sql_insert_query)
        connection.commit()
        count = cursor.rowcount
        print (count, "Record inserted successfully into table")

    except (Exception, psycopg2.Error) as error :
        if(connection):
            print("Failed to insert record into table: ", error)
    
    finally:
        #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
            
# new_employee = (30, 'Sara', 'Inigo', 983645278, 'engineering')
# table_name = 'Employee'
# InsertValues('admin','123_admin', table_name, new_employee)


def UpdateTable(user, user_pw, table_name, update_variable, update_value, condition_variable, condition_value):
    try:
        connection = psycopg2.connect(user = user,
                                      password = user_pw,
                                      host = "localhost",
                                      port = "5432",
                                      database = "erpapplication")

        cursor = connection.cursor()

        # Update single record now
        sql_update_query = "Update " + str(table_name) + ' set ' + update_variable + ' = %s where ' + condition_variable + ' = %s' 
        
        cursor.execute(sql_update_query, (update_value, condition_value))
        connection.commit()
        count = cursor.rowcount
        print(count, "Record Updated successfully ")

    except (Exception, psycopg2.Error) as error:
        print("Error in update operation: ", error)

    finally:
        # closing database connection.
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

# id = 30
# last_name = 'Sanchez'
# UpdateTable('hr', '123_hr', 'Employee', 'Last_Name', last_name, 'Employee_ID', id)


def DeleteValue(user, user_pw, table_name, condition_variable, condition_value):
    try:
        connection = psycopg2.connect(user = user,
                                      password = user_pw,
                                      host = "localhost",
                                      port = "5432",
                                      database = "erpapplication")

        cursor = connection.cursor()

        # Update single record now
        sql_delete_query = "Delete from " + str(table_name) + " where " + str(condition_variable) + "  = %s"
        cursor.execute(sql_delete_query, (condition_value, ))
        connection.commit()
        count = cursor.rowcount
        print(count, "Record deleted successfully ")

    except (Exception, psycopg2.Error) as error:
        print("Error in Delete operation: ", error)

    finally:
        # closing database connection.
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

# id = 30
# DeleteValue('hr', '123_hr', 'Employee','employee_id' ,id)


def Query(user, user_pw, query, flag_select):
    try:
        connection = psycopg2.connect(user = user,
                                      password = user_pw,
                                      host = "localhost",
                                      port = "5432",
                                      database = "erpapplication")

        cursor = connection.cursor()

        # Update single record now
        cursor.execute(query)
        
        if flag_select ==1:
            records = cursor.fetchall()
            names = cursor.description
            columns = []
            for i in range(0, len(names)):
                columns.append(names[i][0])
            df = pd.DataFrame(records, columns = columns)
            
            # change this for a table
            print(df)
        
        connection.commit()
        count = cursor.rowcount
        print(count, "Query executed successfully ")

    except (Exception, psycopg2.Error) as error:
        print("Error in query execution: ", error)

    finally:
        # closing database connection.
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
            
    if flag_select ==1:
        return (df)
          
# flag_select = 0
# Query('hr', '123_hr', "insert into employee values (140, 'Blake', 'Anderson', 933847662, 'engineering')",flag_select)

# flag_select = 1
# Query('hr', '123_hr', "select * from Employee",flag_select)


def CreateOrder(user, pwd):
    # Insert New row to ord (with price 0)
    ord_id = int(input('Insert Order ID: '))
    customer = int(input('Insert Customer ID: '))
    print(customer)    
    
    today = date.today()
    d = str(today)
    
    new_order = (ord_id, 0, d, employee, customer)
    InsertValues(user, pwd, 'Ord', new_order)
    # Insert New row to includes for each model    
    while True:
        model_id = int(input('Insert Model ID: '))
        print('Insert quantity of Model ', model_id,': ')
        quantity = input()       
        new_includes = (ord_id, model_id, quantity)
        InsertValues(user,pwd, 'Includes', new_includes)
        
        flag_exit = input('Do you want to introduce other Model in the Order? y/n')       
        if flag_exit == 'n':
            break
    # Update price to ord
    query = 'select Quantity*Sale_Price as Total_model_price from Model natural join Includes where Order_ID = ' + str(ord_id)    
    df_price = Query(user, pwd, query, 1)
    total_price = sum(df_price['total_model_price'])

    UpdateTable(user, pwd, 'Ord', 'Total_Price', total_price, 'Order_ID', ord_id)

    
def ExpensesReport(user, pwd):
    df_salaryT = Query(user, pwd, "select * from report_expense_salaryT",1)
    df_salaryP = Query(user, pwd, "select * from report_expense_salaryP",1)
    df_salary = pd.concat([df_salaryT, df_salaryP])
    total_salary = sum(df_salary['salary'])

    df_inventory = Query(user, pwd, "select * from report_expense_inventory",1)
    total_inventory = sum(df_inventory['total_cost'])

    total = total_salary + total_inventory
    df_report = pd.DataFrame([[total_salary,total_inventory, total]],columns = ['Total_Salary_expenses', 'Total_Inventory_expenses', 'Total_expenses'])
    
    print('Table Reports:')
    print(df_salary)
    print()
    print(df_inventory)   
    print()
    print(df_report)  
    
    plt.figure()
    sns.set(style="whitegrid")    
    # Draw a nested barplot to show survival for class and sex
    g = sns.catplot(x="employee_id", y="salary", data=df_salary,
                    height=6, kind="bar", palette="muted")
    g.despine(left=True)
    g.set_ylabels("Salaries")
    plt.show()
    
    plt.figure()
    sns.set(style="whitegrid")    
    # Draw a nested barplot to show survival for class and sex
    h = sns.catplot(x="inventory_id", y="total_cost", data=df_inventory,
                    height=6, kind="bar", palette="muted")
    h.despine(left=True)
    h.set_ylabels("Inventory Total Costs")
    plt.show()
    
    plt.figure() 
    labels = ['Employee Cost', 'Inventory Cost']
    sizes = [(total_salary/total)*100, (total_inventory/total)*100]
    colors = ['lightskyblue', 'lightcoral']
    patches, texts = plt.pie(sizes, colors=colors, shadow=True, startangle=90)
    plt.legend(patches, labels, loc="best")
    plt.axis('equal')
    plt.tight_layout()
    plt.show()

    


def TrendsReport(user, pwd):
    df_ord = Query(user, pwd, "select model_id, date, quantity from Ord natural join includes",1)    
    df_trends = Query(user, pwd, "select * from report_trend",1)
    n_models = df_trends['model_id'].unique()
    n_customers = df_trends['customer_id'].unique()
    column_names = []
    for i in n_customers:
        column_names.append(str(i))
    
    df_model = pd.DataFrame(columns=column_names)
    for i in n_models:
        df_model_i = df_trends[df_trends['model_id']==i]
        
        customer_vector = np.zeros(len(n_customers))
        customer_df=pd.DataFrame([customer_vector],columns=column_names)
        for j in df_model_i['customer_id']:
            customer_df.iloc[0,j-1] = df_model_i[df_model_i['customer_id']==j]['total_quantity'].iloc[0]
        df_model = df_model.append(customer_df)
        
    # set width of bar
    barWidth = 0.25
         
    # Set position of bar on X axis
    r1 = np.arange(len(df_model.iloc[0]))
    r2 = [x + barWidth for x in r1]
    r3 = [x + barWidth for x in r2]
    r4 = [x + barWidth for x in r3]
    r5 = [x + barWidth for x in r4]
    
    plt.figure()
    
    # Make the plot
    plt.bar(r1, df_model.iloc[0], color='darkturquoise', width=barWidth, edgecolor='white', label='Model1')
    plt.bar(r2, df_model.iloc[1], color='cadetblue', width=barWidth, edgecolor='white', label='Model2')
    plt.bar(r3, df_model.iloc[2], color='powderblue', width=barWidth, edgecolor='white', label='Model3')
    plt.bar(r4, df_model.iloc[3], color='teal', width=barWidth, edgecolor='white', label='Model4')
    plt.bar(r5, df_model.iloc[4], color='darkslategrey', width=barWidth, edgecolor='white', label='Model5')
     
    # Add xticks on the middle of the group bars
    plt.xlabel('Customer ID', fontweight='bold')
    plt.xticks([r + barWidth for r in range(len(df_model.iloc[0]))], column_names)
     
    # Create legend & Show graphic
    plt.legend()
    plt.show()
    
    plt.figure()
    # OTHER PLOT
    ax = sns.lineplot(x="date", y="quantity",
                      hue="model_id", style="model_id",
                      markers=True, dashes=False, data=df_ord)
    plt.show()

def SalesReport(user, pwd):
    df_sales = Query(user, pwd, "select * from report_sales",1)

    plt.figure()
    sns.set(style="whitegrid")
    
    # Draw a nested barplot to show survival for class and sex
    g = sns.catplot(x="employee_id", y="total_sales", hue="customer_id", data=df_sales,
                    height=6, kind="bar", palette="muted")
    g.despine(left=True)
    g.set_ylabels("Total Sales")
    plt.show()

def InventoryReport(user, pwd):
    df_inv = Query(user, pwd, "select * from report_inventory",1)   
    plt.figure()
    sns.set(style="whitegrid")
    
    # Draw a nested barplot to show survival for class and sex
    g = sns.catplot(x="inventory_id", y="inventory_quantity", data=df_inv,
                    height=6, kind="bar", palette="muted")
    g.despine(left=True)
    g.set_ylabels("Total Inventory")
    plt.show()

def SalesHRview(user, pwd):
    df_sales = Query(user, pwd, "select * from report_sales_HR",1)
    plt.figure()
    sns.set(style="whitegrid")
    # Draw a nested barplot to show survival for class and sex
    g = sns.catplot(x="employee_id", y="total_sales", data=df_sales,
                    height=6, kind="bar", palette="muted")
    g.despine(left=True)
    g.set_ylabels("Total Sales")
    plt.show()



# ----------------------------------------------------------------------------



print('ERP APPLICATION')
print('Login:')

all_users = np.matrix([['sales1','admin', '123_admin',6],['sales2', 'sales','123_sales',7], ['sales3', 'sales','123_sales',8], ['sales4', 'sales','123_sales',9], ['sales5', 'sales','123_sales',10], ['engineer1', 'admin','123_admin',11], ['engineer2', 'engineer','123_engineer',12], ['engineer3', 'engineer','123_engineer',13], ['engineer4', 'engineer','123_engineer',14], ['engineer5', 'engineer','123_engineer',15], ['hr1', 'admin','123_admin',1], ['hr2','hr','123_hr',2], ['hr3','hr','123_hr',3], ['hr4','hr','123_hr',4], ['hr5','hr','123_hr',5]])

# Login loop
while True:
    login = input('Login user:')
    pwd = input('Password:')
    
    if login in all_users[:,0]:
        if pwd == all_users[np.where(all_users == login)[0],[2]]:
            user = all_users[np.where(all_users == login)[0],[1]][0,0]
            employee = int(all_users[np.where(all_users == login)[0],[3]])
            break
        else:
            print('Incorrect password')
               
    else:
        print('Incorrect user')

print('User and password correct') 
print('Welcome to the ERP application,',login)
# current date and time
now = datetime.now()
timestamp = datetime.timestamp(now)
start_time = str(datetime.fromtimestamp(timestamp))

while True:

    if user == 'admin':
        print('Select an option:')
        while True:
            print('Type "a" to Create a new employee')
            print('Type "b" to Grant/Revoke access to an employee')
            print('Type "c" to View business reports')
            print('EMERGENCY BUTTON: Type e to Introduce an SQL query')
            action = input()
            if action in ['a','b','c','e']:
                break
            else:
                print('Incorrect action')
        
        if action == 'a':
            print('Introduce new employee values:')
            value1 = int(input('Employee_ID:'))
            value2 = input('First_Name:')
            value3 = input('Last_Name:')
            value4 = int(input('SSN:'))
            value5 = input('Job_Type:')
            
            new_employee = (value1, value2, value3, value4, value5)
            InsertValues(user,pwd, 'Employee', new_employee)
            
        elif action == 'b':
            
            
            g_flag = input('Type "g" if you want to grant, or other key if you want to revoke:')
            print('Who do you want to grant/revoke access?')
            
            while True:
                print('Type "h" to give/revoke priveleges to Human Resources employee')
                print('Type "s" to give/revoke priveleges to Sales employee')
                print('Type "e" to give/rovoke priveleges to Engineer employee')
                action = input()
                if action in ['h','s','e']:
                    break
                else:
                    print('Incorrect action')
            if action == 'h':
                person = 'hr'
            elif action == 's':
                person = 'sales'
            elif action == 'e':
                person = 'engineer'

            table = input('Introduce Table Name:')            
            priv = input('Introduce privileges with comas:')

            if g_flag =='g':
                query = 'grant '+ priv +' on ' + table + ' to ' + person
            else:
                query = 'revoke '+ priv +' on ' + table + ' from ' + person
            
            Query(user, pwd, query, 0)
            
            
        elif action == 'c':
            while True:
                print('What report do you want to view?')
                print('Type "s" to View "Sales report"')
                print('Type "c" to View "Customer trends report"')
                print('Type "i" to View "Inventory stock report"')
                print('Type "e" to View "Expenses report"')
                action = input()
                if action in ['s','c','i','e']:
                    break
                else:
                    print('Incorrect action')
            
            if action == 's':
                SalesReport(user, pwd)
                
            if action == 'c':
                TrendsReport(user, pwd)
                
            if action == 'i':
                InventoryReport(user,pwd)
                
            if action == 'e':
                ExpensesReport(user, pwd)
                
                
        elif action == 'e':
            query = input('Introduce query:')
            flag_select = int(input('Is it a select query? 1/0:'))
            Query(user, pwd, query, flag_select)
            
            
            
            
    elif user == 'sales':
        print('Select an option:')
        while True:
            print('Type "a" to View a customer')
            print('Type "b" to Update a customer')
            print('Type "c" to Create an order')
            print('Type "d" to View "Sales report"')
            print('Type "f" to View "Trends report"')
            print('EMERGENCY BUTTON: Type e to Introduce an SQL query')
            action = input()
            if action in ['a','b','c','d', 'f', 'e']:
                break
            else:
                print('Incorrect action')
        
        if action == 'a':
            value1 = input('Introduce Customer_ID you want to view:')
            query = "select * from Customer where Customer_ID = " + value1
            Query(user, pwd, query, 1)
            
        elif action == 'b':
            value3 = input('Introduce the Customer_ID you want to update:')
            value1 = input('Introduce name of the Column to update:') 
            value2 = input('Introduce value:')
            
            UpdateTable(user, pwd, 'Customer', value1, value2, 'Customer_ID', value3)
            
        elif action == 'c':
            CreateOrder(user, pwd)
            
        elif action == 'd':
            SalesReport(user, pwd)
        
        elif action == 'f':
            TrendsReport(user, pwd)

        elif action == 'e':
            query = input('Introduce query:')
            flag_select = int(input('Is it a select query? 1/0:'))
            Query(user, pwd, query, flag_select)           

        
    elif user == 'engineer':
        print('Select an option:')
        while True:
            print('Type "a" to View Model')
            print('Type "b" to Update a Model')
            print('Type "c" to View Inventory')
            print('Type "d" to Update Inventory')
            print('Type "f" to View "Employee information"')
            print('Type "g" to View "Inverntory report"')
            print('Type "h" to Create a new Model')
            print('EMERGENCY BUTTON: Type e to Introduce an SQL query')
            action = input()
            if action in ['a','b','c','d', 'f', 'g','h', 'e']:
                break
            else:
                print('Incorrect action')
        
        if action == 'a':
            getValues(user,pwd,'Model')
            
        elif action == 'b':
            value3 = input('Introduce the Model_ID you want to update:')
            value1 = input('Introduce name of the Column to update:') 
            value2 = input('Introduce value:')
             
            UpdateTable(user, pwd, 'Model', value1, value2, 'Model_ID', value3)
            
        elif action == 'c':
            getValues(user,pwd,'Inventory')
            
        elif action == 'd':
            value3 = input('Introduce the Inventory_ID you want to update:')
            value1 = input('Introduce name of the Column to update:') 
            value2 = input('Introduce value:')
             
            UpdateTable(user, pwd, 'Inventory', value1, value2, 'Inventory_ID', value3)
            
        elif action == 'f':
            getValues(user,pwd,'employee_info')

        elif action == 'g':
                InventoryReport(user,pwd)

        elif action == 'h':
            print('Introduce new model values:')
            value1 = int(input('Model_ID:'))
            value2 = int(input('Sale Price:'))
            
            new_model = (value1, value2)
            InsertValues(user,pwd, 'Model', new_model)
        
        elif action == 'e':
            query = input('Introduce query:')
            flag_select = int(input('Is it a select query? 1/0:'))
            Query(user, pwd, query, flag_select)

        
        
        
    elif user == 'hr':
        print('Select an option:')
        while True:
            print('Type "a" to View Employee')
            print('Type "b" to Update an Employee')
            print('Type "c" to View Employee and sales numbers')
            print('Type "d" to Create a New Employee')
            print('EMERGENCY BUTTON: Type e to Introduce an SQL query')
            action = input()
            if action in ['a','b','c','d','e']:
                break
            else:
                print('Incorrect action')
        
        if action == 'a':
            getValues(user,pwd,'Employee')
        
        if action == 'b':
            value3 = input('Introduce the Employee_ID you want to update:')
            value1 = input('Introduce name of the Column to update:') 
            value2 = input('Introduce value:')
            
            UpdateTable(user, pwd, 'Employee', value1, value2, 'Employee_ID', value3)
                
        if action == 'c':
            SalesHRview(user,pwd)
            
        if action == 'd':
            print('Introduce new employee values:')
            value1 = int(input('Employee_ID:'))
            value2 = input('First_Name:')
            value3 = input('Last_Name:')
            value4 = int(input('SSN:'))
            value5 = input('Job_Type:')
            
            new_employee = (value1, value2, value3, value4, value5)
            InsertValues(user,pwd, 'Employee', new_employee)
                
        if action == 'e':
            query = input('Introduce query:')
            flag_select = int(input('Is it a select query? 1/0:'))
            Query(user, pwd, query, flag_select)

                        
    other = input('Do you want to make another action? Type y/n:')
    if other == 'n':
        print('Closing ERP application')
        # current date and time
        now = datetime.now()
        timestamp = datetime.timestamp(now)
        end_time = str(datetime.fromtimestamp(timestamp))
        
        new_login = (login, user, start_time, end_time, employee)
        table_name = 'Login'       
        InsertValues(user,pwd, table_name, new_login)        
        break
        









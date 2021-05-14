import json, requests, os, sys, time, datetime, json, pantab
from flask import Flask, request, render_template, redirect, url_for, flash, Response
from tableauhyperapi import *
import tableauserverclient as TSC
import pandas as pd
import numpy as np

# Set up vars for GET request
rest_url = os.environ['rest_url']
headers_str = str(os.environ['headers'])
headers = json.loads(headers_str)
json_object = os.environ['json_object']

# Set up vars for publishing
token_name = os.environ['token_name']
personal_access_token = os.environ['personal_access_token']
site_id = os.environ['site_id']
server_address = os.environ['server_address']
project_name = os.environ['project_name']

# Include .hyper
hyper_name = os.environ['hyper_name'] 

# Create our Flask app
app = Flask(__name__)


# Creates the index page.
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

# Sets the logic on button press to run our python code and return us to the index page.
@app.route('/create', methods=['GET','POST'])
def create():
    # Grab the data and create the hyper file
    get_data(rest_url)

    # Then publish to Online/Server
    publish_hyper()

    # Reload the index page with a success message :)
    return render_template('index.html', message=f"{hyper_name} was published to site: {os.environ['site_id']}!")

    


def get_data(rest_url):    
    '''This function pings a REST API and returns hardcoded fields as a flat, specifically ordered, nested list with values and no keys.'''
    
    '''
    THIS WILL NEED TO BE MODIFIED BASED ON YOUR API!
    THIS WILL NEED TO BE MODIFIED BASED ON YOUR API!
    THIS WILL NEED TO BE MODIFIED BASED ON YOUR API!
    '''


    # Get everything ready and create GET request
    query_string = "?per_page=100"
    print("Call: " + rest_url + query_string)
    
    # Use requests to grab the data and pull into JSON object
    json_call = requests.get(url=rest_url+query_string, headers=headers)    
    response = json.loads(json_call.text)
    
    # Load data into df
    df = pd.json_normalize(response[json_object])

    # Set the table name for the hyper file
    table_name = hyper_name.replace('.hyper', '')

    # Use pantab library to easily create hyper file
    pantab.frame_to_hyper(df=df, database=hyper_name, table=table_name)



def publish_hyper():
    '''Shows how to leverage the Tableau Server Client (TSC) to sign in and publish an extract directly to Tableau Online/Server'''

    # Sign in to server
    tableau_auth = TSC.PersonalAccessTokenAuth(
        token_name=token_name,
        personal_access_token=personal_access_token,
        site_id=site_id
    )
    server = TSC.Server(server_address, use_server_version=True)

    with server.auth.sign_in(tableau_auth):
        # Define publish mode - Overwrite, Append, or CreateNew
        publish_mode = TSC.Server.PublishMode.Overwrite
        
        # Get project_id from project_name
        all_projects, pagination_item = server.projects.get()
        for project in TSC.Pager(server.projects):
            if project.name == project_name:
                project_id = project.id
    
        # Create the datasource object with the project_id
        datasource = TSC.DatasourceItem(project_id)
        

        # Publish datasource
        datasource = server.datasources.publish(datasource, hyper_name, publish_mode)
        print("Datasource published. Datasource ID: {0}".format(datasource.id))

    


if __name__ == '__main__':
    app.run()
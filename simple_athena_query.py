#!/usr/bin/env python3
"""
Simple AWS Athena Query Example for flights table.
A minimal example showing how to query Athena.
"""

import boto3
import time
import pandas as pd

def simple_athena_query(database, query, s3_output_location, region='us-east-1'):
    """
    Execute a simple Athena query and return results.
    
    Args:
        database (str): Athena database name
        query (str): SQL query to execute
        s3_output_location (str): S3 path for query results
        region (str): AWS region
        
    Returns:
        pd.DataFrame: Query results
    """
    
    # Create Athena client
    athena = boto3.client('athena', region_name=region)
    
    print(f"Executing query: {query}")
    
    # Start query execution
    response = athena.start_query_execution(
        QueryString=query,
        QueryExecutionContext={'Database': database},
        ResultConfiguration={'OutputLocation': s3_output_location}
    )
    
    query_id = response['QueryExecutionId']
    print(f"Query ID: {query_id}")
    
    # Wait for completion
    while True:
        result = athena.get_query_execution(QueryExecutionId=query_id)
        status = result['QueryExecution']['Status']['State']
        
        if status == 'SUCCEEDED':
            print("✅ Query completed successfully!")
            break
        elif status in ['FAILED', 'CANCELLED']:
            error = result['QueryExecution']['Status'].get('StateChangeReason', 'Unknown error')
            raise Exception(f"Query failed: {error}")
        else:
            print(f"Status: {status}")
            time.sleep(2)
    
    # Get results
    results = athena.get_query_results(QueryExecutionId=query_id)
    
    # Convert to DataFrame
    data = []
    rows = results['ResultSet']['Rows']
    
    if not rows:
        return pd.DataFrame()
    
    # Get column names from first row
    columns = [col.get('VarCharValue', '') for col in rows[0]['Data']]
    
    # Get data from remaining rows
    for row in rows[1:]:
        row_data = [col.get('VarCharValue', '') for col in row['Data']]
        # Ensure row has same number of columns
        while len(row_data) < len(columns):
            row_data.append('')
        data.append(row_data)
    
    df = pd.DataFrame(data, columns=columns)
    print(f"Retrieved {len(df)} rows")
    
    return df

def main():
    """Example usage of the simple Athena query function."""
    
    # 🔧 CONFIGURATION - UPDATE THESE VALUES
    DATABASE = "flights"           # Your Athena database
    S3_BUCKET = "s3://is3600-cam/query_results/"   # Your S3 bucket for results
    REGION = "us-west-2"                      # Your AWS region
    
    print("=== Simple Athena Query Example ===")
    
    try:
        # Example 1: Get table schema
        print("\n1. Getting flights table schema...")
        schema_df = simple_athena_query(
            database=DATABASE,
            query="DESCRIBE flights;",
            s3_output_location=S3_BUCKET,
            region=REGION
        )
        print("Table Schema:")
        print(schema_df)
        
        # Example 2: Sample data
        print("\n2. Getting sample flight data...")
        sample_df = simple_athena_query(
            database=DATABASE,
            query="SELECT * FROM flights LIMIT 5;",
            s3_output_location=S3_BUCKET,
            region=REGION
        )
        print("Sample Data:")
        print(sample_df)
        
        # Example 3: Count total flights
        print("\n3. Counting total flights...")
        count_df = simple_athena_query(
            database=DATABASE,
            query="SELECT COUNT(*) as total_flights FROM flights;",
            s3_output_location=S3_BUCKET,
            region=REGION
        )
        print("Total Flights:")
        print(count_df)
        
        # Example 4: Flight statistics by date
        print("\n4. Flight statistics by date...")
        stats_df = simple_athena_query(
            database=DATABASE,
            query="""
                SELECT fl_date, 
                       COUNT(*) as flight_count,
                       AVG(dep_delay) as avg_dep_delay,
                       AVG(arr_delay) as avg_arr_delay
                FROM flights 
                GROUP BY fl_date 
                ORDER BY fl_date 
                LIMIT 10;
            """,
            s3_output_location=S3_BUCKET,
            region=REGION
        )
        print("Flight Statistics by Date:")
        print(stats_df)
        
        # Save results
        stats_df.to_csv("flight_statistics.csv", index=False)
        print("\n✅ Results saved to flight_statistics.csv")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n📋 Setup Checklist:")
        print("1. Configure AWS credentials (aws configure)")
        print("2. Update DATABASE and S3_BUCKET variables above")
        print("3. Ensure 'flights' table exists in Athena")
        print("4. Check IAM permissions for Athena and S3")

if __name__ == "__main__":
    main()

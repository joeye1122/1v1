from google.cloud import bigquery

client = bigquery.Client()

query = """
    SELECT name, SUM(number) as total_people
    FROM `bigquery-public-data.usa_names.usa_1910_2013`
    WHERE state = 'TX'
    GROUP BY name, state
    ORDER BY total_people DESC
    LIMIT 20
    """

query2 = """

"""

query3 ="""

"""

query_job1 = client.query(query)
query_job2 = client.query(query2)
query_job3 = client.query(query3)



results1 = query_job1.result()
results2 = query_job2.result()
results3 = query_job3.result()


for row in results1:
    print("{} : {} views".format(row.url, row.view_count))


import pandas as pd
import ast

def get_jobs():
    jobs1 = pd.read_csv('scrapper/jobs_csv/jobs1.csv')
    jobs2 = pd.read_csv('scrapper/jobs_csv/jobs2.csv')
    # tags is stored as string so, convert back to list of string
    jobs1['tags'] = jobs1['tags'].apply(lambda x: ast.literal_eval(x))
    jobs2['tags'] = jobs2['tags'].apply(lambda x: ast.literal_eval(x))
    # Convert pandas dataframe to list of dictionaries
    jobs_list = jobs1.to_dict(orient='records') + jobs2.to_dict(orient='records')
    return jobs_list


jobs = get_jobs()
print(jobs[10])
print(type(jobs), len(jobs))
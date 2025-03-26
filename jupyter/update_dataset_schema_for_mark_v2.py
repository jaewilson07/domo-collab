import domolibrary.client.DomoAuth as dmda
import domojupyter as dj
from typing import List
import domolibrary.utils.chunk_execution as dmce
import pandas as pd
import domolibrary.classes.DomoDataset as dmds
from pprint import pprint

async def generate_domo_auth(account_name: str, domo_instance: str, debug_prn: bool = False) -> dmda.DomoAuth:
    """
    Generates Domo authentication using a specified account name and Domo instance.

    Args:
        account_name (str): The name of the Domo account containing the access token.
        domo_instance (str): The Domo instance to authenticate against.
        debug_prn (bool): If True, prints debug information.

    Returns:
        dmda.DomoAuth: A DomoAuth object containing the authentication details.
    """
    account_properties = dj.get_account_property_keys(account_name)
    if debug_prn:
        print(account_properties)

    creds = {prop: dj.get_account_property_value(account_name, prop) for prop in account_properties}

    auth = dmda.DomoTokenAuth(domo_access_token=creds['domoAccessToken'], domo_instance=domo_instance)

    if debug_prn:
        print((await auth.who_am_i()).response)
    return auth

def generate_config_dataset(df : pd.DataFrame, debug_prn: bool = False) -> dict:
        """
        Organizes dataset information into a dictionary, grouping records by DatasetID.

        Args:
            df (pd.DataFrame): DataFrame containing dataset details with DatasetID, DatasetName, Column Name, and Description.
            debug_prn (bool): If True, prints the intermediate dictionary for debugging.

        Returns:
            dict: A dictionary where keys are DatasetIDs and values are lists of column details.
        """
        ls = df.to_dict(orient='records')
        if debug_prn:
            pprint(ls)

        res = {}
        for row in ls:
            dataset_id = row.pop('DatasetID')
            if dataset_id not in res:
                res[dataset_id] = []
            res[dataset_id].append(row)

        return res

async def get_dataset_and_schema(auth, dataset_id, debug_api: bool = False) -> dmds.DomoDataset:
        """
        Fetches dataset metadata and schema information from Domo.

        Args:
            auth (dmda.DomoAuth): Domo authentication object.
            dataset_id (str): ID of the dataset to fetch.
            debug_api (bool): If True, prints API call debug information.

        Returns:
            dmds.DomoDataset: A DomoDataset object containing dataset details and schema.
        """
        domo_dataset = await dmds.DomoDataset.get_by_id(dataset_id=dataset_id, auth=auth, debug_api=debug_api)
        await domo_dataset.Schema.get(debug_api=debug_api)
        return domo_dataset

def update_schema_description_text(col_id: str, new_description: str, schema_columns):
        """
        Updates the description of a specific column based on the provided data.

        Args:
            col_id (str): The ID of the column to update.
            new_description (str): The new description to apply to the column.
            schema_columns (list): A list of schema column objects from the Domo dataset.
        """
        for column in schema_columns:
            if column.id == col_id:
                column.description = new_description

async def update_schema(dataset_id: str, new_descriptions: List[dict], auth: dmda.DomoAuth, debug_api: bool = False) -> pd.DataFrame:
        domo_dataset = await get_dataset_and_schema(auth, dataset_id)

        for row in new_descriptions:
            update_schema_description_text(col_id=row['Column Name'], new_description=row['Description'], schema_columns=domo_dataset.Schema.columns)

        res = await domo_dataset.Schema.alter_schema_descriptions(debug_api=debug_api)
        return pd.DataFrame(res.response.get('columns', []))
                
async def main():
    # Generate authentication token for accessing Domo API using the provided account name and instance
    #Replace with token account name and Domo instance name
    auth = await generate_domo_auth('YOUR_DOMO_ACCESS_TOKEN_ACCOUNT', 'YOUR_DOMO_INSTANCE_NAME', debug_prn=False)
    auth.generate_auth_header()

    #Replace column names if needed
    columns = ['DatasetID', 'DatasetName', 'Column Name', 'Description']
    
    #Replace with your dataset name
    df = dj.read_dataframe('YOUR_DATASET_NAME', nrows=5000)
    
    df = df[columns]
    
    
    config_ls = generate_config_dataset(df, debug_prn=True)

    tasks = [
        update_schema(dataset_id=dataset_id, new_descriptions=new_descriptions, auth=auth)
        for dataset_id, new_descriptions in config_ls.items()
    ]

    dfs = await dmce.gather_with_concurrency(*tasks, n=10)

    if dfs:
        result_df = pd.concat(dfs)
        print(result_df)
    else:
        print("No dataframes to concatenate")

await main()

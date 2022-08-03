
import pandas as pd
import numpy as np

from sklearn.pipeline import Pipeline
from feature_engine.selection import DropDuplicateFeatures, DropConstantFeatures, SmartCorrelatedSelection
from sklearn.base import BaseEstimator, TransformerMixin


class RemoveColPercentage(BaseEstimator, TransformerMixin):
    def __init__(self, perc=90):
        self.perc = perc
    
    def fit(self, X, y=None):
        return self

    def find_missing_percentage(self, df):
        percent_missing = df.isnull().sum() * 100 / len(df)
        missing_value_df = pd.DataFrame({'column_name': df.columns, 'percent_missing': percent_missing})
        missing_value_df.sort_values('percent_missing', inplace=True)
        return missing_value_df
    
    def drop_emptyCol_percent(self, df, perc):
        percentage_missing_column = self.find_missing_percentage(df)
        print(f"Modifying DataFrame after removing const&quasi and duplicate features :  {df.shape}")
        #Remove the perc% empty columns.
        locate_missing_cols= df.loc[:,percentage_missing_column.percent_missing >= perc]
        df_drop = df.drop(locate_missing_cols,axis=1)
        print(f"Modified DataFramne after deleting missing col {perc}%:  {df_drop.shape}")
        return df_drop
    
    def transform(self, X, y=None):
        X = self.drop_emptyCol_percent(X, self.perc)
        return X

class RemoveSingularMatrix(BaseEstimator, TransformerMixin):
    def __init__(self):
        return None
    
    def fit(self, X, y=None):
        return self
    
    def drop_singularMatrix(self, df):
        Col_name = df.columns
        list_singular_matrix = []
        for i in range(len(Col_name)):
            if len(df[Col_name[i]].unique()) == 2:
                #print(f'Varable_name: {Col_name[i]}')
                list_singular_matrix.append(Col_name[i])
        df.drop(list_singular_matrix,inplace=True,axis=1)
        return df
      
    
    def transform(self, X, y=None):
        X = self.drop_singularMatrix(X)
        return X

class RemoveRowPercentage(BaseEstimator, TransformerMixin):
    def __init__(self, perc=90):
        self.perc = perc
    
    def fit(self, X, y=None):
        return self
    
    def drop_emptyRow_percent(self, df, perc):
        print(f"Modifying DataFrame after removing const&quasi, duplicate and missing col features:  {df.shape}")
        min_count =  int(((100-perc)/100)*df.shape[1] + 1)
        df_drop = df.dropna( axis=0, thresh=min_count)
        print(f"Modified DataFrame after deleting missing rows {perc}%:  {df_drop.shape}")
        return df_drop
    
    def transform(self, X, y=None):
        X = self.drop_emptyRow_percent(X, self.perc)
        return X

class CleanData(object):
    def __init__(self, *args):
        super(CleanData, self).__init__(*args)
        

    def find_missing_percentage(self, df):
        percent_missing = df.isnull().sum() * 100 / len(df)
        missing_value_df = pd.DataFrame({'column_name': df.columns, 'percent_missing': percent_missing})
        missing_value_df.sort_values('percent_missing', inplace=True)
        return missing_value_df

    def removeDuplicateColumns(self, df):
        '''
        Finding the duplicate columns in the data set

        Parameters
        ==========
        file: xlxs file.

        Returns
        ==========
        clean: Removing the duplicated columns.
        Sum: The number of duplicated columns.
        '''
        return list(df.loc[:,~df.columns.duplicated()]), df.columns.duplicated().sum()

    def convert_num_to_cat(self, df, var_name_list):
        # perform conversion
        for i in range(0, len(var_name_list)):
            df[var_name_list[i]] = df[var_name_list[i]].apply(str)
        return df

    def convert_cat_to_num(self, df, var_name_list):
        # perform conversion
        for i in range(0, len(var_name_list)):
            df[var_name_list[i]] = df[var_name_list[i]].astype(float)
        return df

    def change_datetime_format(self, name_var_org, name_var_new, df):
        df[name_var_new] = df[name_var_org].dt.date
        df[name_var_new] = pd.to_datetime(df[name_var_new], format='%Y-%m-%d')
        del df[name_var_org]
        return df

    def rename_col(self, df, name_var_org, name_var_new):
        return df.rename(columns={
        name_var_org:name_var_new}, inplace='True')
        


    def drop_const_quasi_dupl(self,df):
        #name =[x for x in globals() if globals()[x] is df][0]
        #name = print(f"{df}")
        pipe = Pipeline([
            ('singular_matrix', RemoveSingularMatrix()),
            ('constant', DropConstantFeatures(tol=0.998, variables=None, missing_values='include')),
            ('duplicated', DropDuplicateFeatures()),
            ('correlation', SmartCorrelatedSelection(threshold=0.8, selection_method='variance', method='pearson')),
            ('Remove Row%', RemoveRowPercentage(50)),
            ('Remove Col%', RemoveColPercentage(50)),
            ])
        pipe.fit(df)

        print(f"The length of the dropped feature: {len(pipe.named_steps['constant'].features_to_drop_)}")
        print(f"Name of the Features to drop: {pipe.named_steps['constant'].features_to_drop_} \n")

        print(f"The length of the duplicated feature: {len(pipe.named_steps['duplicated'].features_to_drop_)}")
        print(f"Name of the Duplicated features to drop: {pipe.named_steps['duplicated'].features_to_drop_} \n")

        print(f"The length of the correlated feature: {len(pipe.named_steps['correlation'].features_to_drop_)}")
        print(f"Name of the correlated features to drop: {pipe.named_steps['correlation'].features_to_drop_} \n")
        print(f"groups of correlated features to drop: {pipe.named_steps['correlation'].correlated_feature_sets_} \n") # groups of correlated features
        
        print(f"Before Modifying Dataframe the very Orginal DataSet:  {df.shape}")
        df_mod = pipe.transform(df)
        print(f"The final Modified DataFrame after dropping duplicated,constant,quasi, Missing values (R&C) and correlated features:  {df_mod.shape} \n")
        return df_mod

    def drop_emptyRow_percent(self, df, perc):
        #name =str([x for x in globals() if globals()[x] is df][0])
        print(f"Before Modifying DataFrame:  {df.shape}")
    #perc = 80.0
        min_count =  int(((100-perc)/100)*df.shape[1] + 1)
        df_drop = df.dropna( axis=0, thresh=min_count)
        print(f"Modified DataFrame after deleting missing rows {perc}%:  {df_drop.shape}")
        return df_drop


    #calculate the percentage of the missing values in each column
    def drop_emptyCol_percent(self, df, perc):
        percentage_missing_column = self.find_missing_percentage(df)
        #name =[x for x in globals() if globals()[x] is df][0]
        print(f"Before Modifying DataFrame:  {df.shape}")

        #Remove the perc% empty columns.
        locate_missing_cols= df.loc[:,percentage_missing_column.percent_missing >= perc]
        df_drop = df.drop(locate_missing_cols,axis=1)
        print(f"Modified DataFramne after deleting missing rows {perc}%:  {df_drop.shape}")
        return df_drop
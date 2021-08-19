def fill_na_median_area(df, num_col):
    """
    Attempts to fill NaN's with median of observations with same region 
    and district. If unable then fills NaN's with median of region. If unable 
    then fills NaN's with median of dataset.
        
        Params: df as dataframe, num_col as string representing a numerical feature
        
        Returns: nothing, edits df in place
    """
    region_district_groupby_table = df.groupby(['region', 'district_code'])[num_col].transform('median')
    df[num_col].fillna(region_district_groupby_table, inplace=True)

    region_groupby_table = df.groupby(['region'])[num_col].transform('median')
    df[num_col].fillna(df.groupby(['region'])[num_col].transform('median'), inplace=True)

    dataset_median = df[num_col].median()
    df[num_col].fillna(dataset_median, inplace=True)


def fill_na_mean_area(df, num_col):
    """
    Attempts to fill NaN's with mean of observations with same region 
    and district. If unable then fills NaN's with mean of region. If unable 
    then fills NaN's with mean of dataset.
        
        Params: df as dataframe, num_col as string representing a numerical feature
        
        Returns: nothing, edits dataframe in place
    """
    region_district_groupby_table = df.groupby(['region', 'district_code'])[num_col].transform('mean')
    df[num_col].fillna(region_district_groupby_table, inplace=True)

    region_groupby_table = df.groupby(['region'])[num_col].transform('mean')
    df[num_col].fillna(df.groupby(['region'])[num_col].transform('mean'), inplace=True)

    dataset_mean = df[num_col].mean()
    df[num_col].fillna(dataset_mean, inplace=True)


def single_occurences_to_other(df, col):
    """
    Converts text feature that occurs only once to 'other'
    
        Params: df as a dataframe, col as a string representing col in dataframe
        
        Returns: nothing, edits dataframe in place
        
        Note for improvement: is there a way to do this using only pandas commands?
    """
    
    value_counts = df[col].value_counts() == 1
    single_occurences = set([i for i in value_counts.index if value_counts[i] == True])
    df.loc[df[col].isin(single_occurences), col] = 'other'


def replace_na_region_district_mode(df, text_col):
    """
    Replaces null values in text column with mode of that feature in its 
    region/district group
        
        Params: df as dataframe, text_col as string of col of a text feature
        
        Returns: nothing, fills null values in df's text_col in place
    """

    text_col_region_district = df[[text_col, 'region', 'district_code']]
    groupby_table = text_col_region_district.groupby(['region', 'district_code'])[text_col].value_counts()

    for region in REGIONS:
        for district in DISTRICTS:
            try:
                mode = groupby_table[(region, district)].index[0]
                
                match_region = df['region'] == region
                match_district = df['district_code'] == district
                is_na = df[text_col].isna()
                
                df.loc[match_region & match_district & is_na, text_col] = mode
            except:
                continue


def replace_na_region_mode(df, text_col):
    """
    Replaces null values in text column with mode of that feature in its 
    region group
        
        Params: df as dataframe, text_col as string of col of a text feature
        
        Returns: nothing, fills null values in df's text_col in place
    """

    text_col_region_district = df[[text_col, 'region']]
    groupby_table = text_col_region_district.groupby(['region'])[text_col].value_counts()

    for region in REGIONS:
        try:
            mode = groupby_table[(region)].index[0]

            match_region = df['region'] == region
            is_na = df[text_col].isna()

            df.loc[match_region & is_na, text_col] = mode
        except:
            continue
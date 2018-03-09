import numpy as np
import pandas as pd


class Eda:
    """Pandas EDA tool"""

    def __init__(self, df):
        self.df = df

    def analysis(self, sort=False):
        """Get stats for data frame. To sort by null count change sort to True"""
        dict_list = []
        for col in self.df.columns:
            data = self.df[col]
            dict_ = {}
            # The null count for a column. Columns with no nulls are generally more interesting
            dict_.update({"null_count": data.isnull().sum()})
            # Counting the unique values in a column
            # This is useful for seeing how interesting the column might be as a feature
            dict_.update({"unique_count": len(data.unique())})
            # Finding the types of data in the column
            # This is useful for finding out potential problems with a column having strings and ints
            dict_.update({"data_type": set([type(d).__name__ for d in data])})
            # dict_.update({"score" : match[1]})
            try:
                dict_.update({"mean": data.mean()})
                dict_.update({"std": data.std()})
                dict_.update({"ptp": data.ptp()})
                dict_.update({"min": data.min()})
                dict_.update({"max": data.max()})
                dict_.update({"kurt": data.kurtosis()})

            except:
                dict_.update({"mean": '-'})
                dict_.update({"std": '-'})
                dict_.update({"ptp": '-'})
                dict_.update({"min": '-'})
                dict_.update({"max": '-'})
                dict_.update({"kurt": '-'})
            dict_list.append(dict_)
        eda_df = pd.DataFrame(dict_list)
        eda_df.index = self.df.columns
        if sort:
            eda_df = eda_df.sort_values(['null_count', 'unique_count'], ascending=[True, False])
        return eda_df

    def remove_full_null_cols(self):
        """Returns DataFrame of null columns"""
        drop_col_df = pd.DataFrame()
        for col in self.df.columns:
            data = self.df[col]
            if data.isnull().sum() == self.df.shape[0]:
                print('Dropping {} because null values equals length of DataFrame.'.format(col))
                drop_col_df[col] = self.df[col]
                data.drop(1, inplace=True)
        return drop_col_df

    def remove_col_name_spaces(self, spaces=True, capitalization=False):
        """Removes spaces and changes them to underscores"""

        # cols.replace(' ', '_').lower
        if spaces:
            columns = [str(cols).replace(' ', '_') for cols in self.df.columns]
            self.df.columns = columns

        if capitalization:
            columns_caps = [str(cols).lower() for cols in self.df.columns]
            self.df.columns = columns_caps

        return self.df

    def to_float(self, num_ratio=0.25, stop_words=[]):
        """Remove extra characters from columns given
        ratio of numbers to strings,include stop words if necessary.
        removed characters are added to column name to preserve lost info """
        new_col_list = []
        delete_string = ''
        for col in self.df.columns:

            float_list = []

            for item in self.df[col]:
                count_int = 0
                count_list = []
                count_str = 0
                remove_list = []
                try:
                    item_length = len(item)
                    for char in item:
                        try:
                            char = int(char)
                            count_int += 1
                            count_list.append(count_int)
                        except:
                            count_str += 1
                            count_list.append(count_str)
                            remove_list.append(char)
                    delete_string = ''
                    if np.mean(count_int) / item_length >= num_ratio:
                        for delete in remove_list:
                            if delete != '.':
                                for stop_word in stop_words:
                                    for stop_char in stop_word:
                                        if delete != stop_char:
                                            item = item.replace(delete, '')
                                delete_string += delete

                        float_list.append(float(item))
                    else:
                        float_list.append(item)
                except:
                    float_list.append(item)
            if delete_string == '':
                new_col_list.append(col)
            else:
                new_col_list.append(col + '_' + delete_string)
            self.df[col] = float_list
        self.df.columns = new_col_list
        return self.df

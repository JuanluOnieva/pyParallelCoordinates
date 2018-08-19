"""
    Class Parallel Coordinates.
    Contain the necessary functions to plot and save a parallel coordinates graph
    author: Juan L. Onieva
"""

import pandas as pd
import bokeh.plotting as bk
import bokeh.io.export as be
import os
from math import pi
from bokeh.palettes import viridis
from bokeh.io.saving import save
from bokeh.models import Label
from bokeh.models.widgets import Panel, Tabs
from bokeh.core.enums import enumeration
from bokeh.io import output_notebook, output_file


class ParallelCoordinates(object):

    def __init__(self, file_name: str, header=None, my_delimiter=',')->None:
        """
        Initial constructor. It calls two function in order to read the file and preprocces the
        data frame. Contain the attributes
            - my_df: the data frame that is obtain from the file
            - dict_categorical_var: empty dictionary that will contain the variables which are categorical
            - my_df_normalize: the my_df data frame which will be normalize if it is necessary
            - parallel_plot: the final plot
        :param file_name: the corresponding name (with the path, if it isn´t at the source root)
        :param header: it can be 'None' (as default) or 'infer' if the file contain the header in the firs line
        :param my_delimiter: the type of delimiter that split the data in the file. As default is ','
        """
        self. my_df = self.read_file(file_name, header, my_delimiter)
        self.dict_categorical_var = dict()
        self.convert_categorical_to_number()
        self.my_df_normalize = None
        self.parallel_plot = None

    def read_file(self, file_name: str, header, my_delimiter: str)-> pd.DataFrame:
        """
        This function read the file and compute the data frame. Also, use the function 'dropna' in the case
        that there are missing values in all of the columns. Moreover, if there are no header, it creates some names
        for the variables with the following structure --> 'Var-N'
        :param file_name: the corresponding name (with the path, if it isn´t at the source root)
        :param header: it can be 'None' (as default) or 'infer' if the file contain the header in the firs line
        :param my_delimiter: the type of delimiter that split the data in the file. As default is ','
        :return: The corresponding data frame
        """
        if header is not None and not 'infer':
            raise Exception("The header value must be 'None' or 'infer'")
        with open(file_name) as csv_file:
            df = pd.read_csv(csv_file, sep=my_delimiter, header=header)
            df.dropna(how='all', inplace=True)
            if header is None:
                my_header = list()
                for i in range(0, len(df.columns)):
                    my_header.append('Var-'+str(i))
                df.columns = my_header
        return df

    def convert_categorical_to_number(self)->None:
        """
        It converts the columns which the type of data are string to categorical. Also, save the variable and the
        levels in a dictionary (dict_categorical_var) and then transform the categorical data to numeric code
        :return:
        """
        for col in self.my_df.columns:
            if type(self.my_df[col].values.tolist()[0]) is str:
                self.my_df[col] = pd.Categorical(self.my_df[col])
                values_of_cat = dict(enumerate(self.my_df[col].cat.categories))
                self.dict_categorical_var[col] = values_of_cat
                self.my_df[col] = self.my_df[col].cat.codes

    def normalize_data_frame(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Normalize a data frame. It requires that the data in the input data frame must be numeric
        :param df: The data frame that we want to normalize
        :return: Corresponding normalize data frame
        """
        df_norm = df.copy()
        for col in df_norm:
            total = sum(df_norm[col])
            df_norm[col] = df_norm[col]/total
        return df_norm

    def get_multi_line_plot(self, df: pd.DataFrame, width, height, title):
        """
        This function design a plot with the structure of Parallel Coordinates graph.
        For that, it uses the function multi_line from bokeh module. And then, it calls the
        function add_annotation_for_categorical_data in order to add a label where there are the code-category
        from the categorical data
        :param df: Data frame which we want to plot
        :param width: The width measure for the figure
        :param height: The height measure for the figure
        :param title: The tittle  for the figure
        :return: The corresponding plot completed
        """
        plot = bk.figure(plot_width=width, plot_height=height, title=title, x_range=list(self.my_df))
        ys_list = list()
        xs_list = list()
        for i in range(0, len(df)):
            aux_ys_list = df.iloc[i].tolist()
            ys_list.append(aux_ys_list.copy())
            xs_list.append(list(range(0, len(df.columns))))
        try:
            my_palette = viridis(len(df.index))
            plot.multi_line(xs=xs_list, ys = ys_list, line_color=my_palette)
        except ValueError:
            plot.multi_line(xs=xs_list, ys = ys_list)
        plot.xaxis.major_tick_line_color = None
        plot.xgrid.visible = False
        plot.ygrid.visible = False
        TextAlign = enumeration("left", "right", "center")
        plot.xaxis.major_label_text_align = TextAlign.left
        plot.xaxis.major_label_orientation = pi/6
        plot = self.add_annotation_for_categorical_data(plot, width)
        return plot

    def add_annotation_for_categorical_data(self, plot, width):
        """
        This function permit us to understand the code for categorical data. For that, it adds a label which
        show the code number and the string category
        For each categorical variable that is stored at the dictionary (dict_categorical_var) there is going to be
        one label.
        :param plot: The plot where we want to add the label
        :param width: The width of the label
        :return: The plot with the added label
        """
        height = -100
        for key in self.dict_categorical_var:
            text = key + ': ' + str(self.dict_categorical_var[key])
            my_text = Label(x=width/5, y=height, x_units='screen', y_units='screen',
                            text=text, render_mode='css',
                            border_line_color='black', border_line_alpha=1.0,
                            background_fill_color='white', background_fill_alpha=1.0)
            plot.add_layout(my_text)
            height = height - 50
        return plot

    def plot(self, normalize=False, width=500, height=500, title='Parallel-Coordinates', show=True, notebook=False)->None:
        """
        The function plot the data frame as Parallel Coordinates graph. For that, it requires the function
        get_multi_line_plot. In the case, that we want the normalize data, it compute both and show both thanks
        to a tab. Also, it verifies if we are working or notebook or not.
        :param normalize: Boolean that indicates if the data must be normalize or not. In the case of yes, the function
        show both
        :param width: The width measure for the figure. As default is 500
        :param height: The height measure for the figure. As default is 500
        :param title: The tittle  for the figure. As default is 'Parallel-Coordinates'
        :param show: Boolean that indicate if we want to show the plot in a browser
        :param notebook: Boolean that indicate if we are using a notebook, in order to show the plot
        :return:
        """
        if notebook:
            output_notebook()
        else:
            output_file(title + ".html")
        if normalize:
            self.my_df_normalize = self.normalize_data_frame(self.my_df)
            p1 = self.get_multi_line_plot(self.my_df_normalize, width, height, title)
            tab1 = Panel(child=p1, title="Normalize")
            p2 = self.get_multi_line_plot(self.my_df, width, height, title)
            tab2 = Panel(child=p2, title="No normalize")
            self.parallel_plot = Tabs(tabs=[tab1, tab2])
        else:
            self.parallel_plot = self.get_multi_line_plot(self.my_df, width, height, title)
        if show:
            bk.show(self.parallel_plot)

    def file_name_with_ext_and_path(self, file_name: str, format: str, path: str)->str:
        """
        The objective of this function is to add the corresponding path and extension to the name which we want
        to store the plot. In case that the extension is added, it checks if both correspond.
        :param file_name: the file name which we want to store the plot.
        :param format: The corresponding format {.html, .png, .svg}
        :param path: The path where we want to store the data
        :return:
        """
        list_fn = file_name.split('.')
        if len(list_fn) == 1:
            file_name_plus_extension = list_fn[0] + '.' + format
        elif list_fn[1]!=format:
            file_name_plus_extension = list_fn[0] + '.' + format
        else:
            file_name_plus_extension = file_name
        return path + '/' + file_name_plus_extension

    def my_path(self)->str:
        """
        Obtain the path where, as default, we want to store the data
        :return: The path correspond to the source root plus another directory; 'results'
        """
        path = os.getcwd() + '/results'
        if not os.path.exists(path):
            os.makedirs(path)
        return path

    def save(self, format='html', file_name='Parallel-Coordinates', path=None)->None:
        """
        This function allows to save the plot in a specific format.
        :param format: The format that we want for our file
        :param file_name: The corresponding name of the file
        :param path: The path where we want to store the plot, as default we assign the actual directory and
        create new one in there; 'results'
        :return:
        """
        if path is None:
            path = self.my_path()
        valid_format = ['html', 'png', 'svg', 'all']
        if format not in valid_format:
            raise Exception('The format is incorrect')
        if format == 'html' or format == 'all':
            file_name = self.file_name_with_ext_and_path(file_name, 'html', path)
            save(self.parallel_plot, filename=file_name)
        if format == 'png' or format == 'all':
            file_name = self.file_name_with_ext_and_path(file_name, 'png', path)
            be.export_png(self.parallel_plot, filename=file_name)
        if format == 'svg' or format == 'all':
            file_name = self.file_name_with_ext_and_path(file_name, 'svg', path)
            self.parallel_plot.output_backend = "svg"
            be.export_svgs(self.parallel_plot, filename=file_name)


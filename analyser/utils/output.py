from typing import List
import matplotlib.pyplot as plt
import pandas as pd
import plotly.graph_objects as go
from matplotlib import rcParams

rcParams.update({'figure.autolayout': True, 'figure.dpi': 600, 'savefig.dpi': 600})
# rcParams["figure.figsize"] = [7.50, 7.50]
rcParams["figure.autolayout"] = True


class Output:
    @staticmethod
    def _prepare_dataframe(dataframe: pd.DataFrame):
        new_dataframe = dataframe.copy()
        try:
            new_dataframe = dataframe.rename(columns={
                '0m': '0m',
                'MEDIUM_PERSON_ARM_MAX': 'ARMS',
                'MEDIUM_PERSON_SHOULDER_MAX': 'SHOULDER',
            }, errors='raise')
            new_dataframe = new_dataframe[['0m', 'SHOULDER', 'ARMS']]
        except:
            try:
                new_dataframe = new_dataframe.sort_index(axis=1)
            except:
                pass
        if 'REFERENCE' in new_dataframe.columns.values:
            columns = new_dataframe.columns.values.tolist()
            columns.remove('REFERENCE')
            columns.insert(0, 'REFERENCE')
            new_dataframe = new_dataframe.reindex(columns, axis=1)
        return new_dataframe

    @staticmethod
    def _get_colors(dataframe: pd.DataFrame) -> List:
        color_dict = {
            'REFERENCE': 'black',
            'ONEPLUS8T': 'crimson',
            'IPHONE6S': 'dimgray',
            'IPHONE6S2': 'lightgray',
            'LENOVOTAB': 'darkviolet',
            'LENOVOTAB2': 'violet',
            'XPERIAZ3COM': 'teal',
            'XPERIAZ3COM2': 'lightseagreen',
            'XPERIAZ3': 'springgreen',
            'MOTOG6': 'deepskyblue'
        }
        colors = None
        if 'Device' in dataframe.columns.names:
            colors = [color_dict.get(x, '#333333') for x in dataframe.columns]
        return colors

    @staticmethod
    def plot_bar(title,
                 dataframe: pd.DataFrame,
                 xlabel,
                 ylabel,
                 file_path=None,
                 file_name=None):
        plt.clf()
        prepared_dataframe = Output._prepare_dataframe(dataframe)
        colors = Output._get_colors(prepared_dataframe)
        kwargs = {}
        if colors:
            kwargs["color"] = colors
        prepared_dataframe.plot(
            kind='bar',
            xlabel=xlabel,
            ylabel=ylabel,
            title=title,
            grid=True,
            stacked=False,
            width=.75,
            **kwargs
        )
        plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))
        if file_path and file_name:
            plt.savefig(
                f'{file_path}/{file_name}.png'
            )
        else:
            plt.show()

    @staticmethod
    def plot_scatter_and_maxima(title,
                                dataframe: pd.DataFrame,
                                maxima: pd.DataFrame,
                                xlabel,
                                ylabel,
                                file_path=None,
                                file_name=None):
        plt.clf()
        prepared_dataframe = Output._prepare_dataframe(dataframe)
        colors = Output._get_colors(prepared_dataframe)
        kwargs = {}
        if colors:
            kwargs["color"] = colors
        ax = prepared_dataframe.plot(
            kind='line',
            xlabel=xlabel,
            ylabel=ylabel,
            title=title,
            style='.-',
            linewidth=0.5,
            ms=3,
            **kwargs
        )
        ax.scatter(maxima.index, maxima, color='r', s=10)
        ax.set_axisbelow(True)
        plt.legend(bbox_to_anchor=(1.0, 1.0))
        plt.grid()
        if file_path and file_name:
            plt.savefig(f'{file_path}/{file_name}.png')
        else:
            plt.show()

    @staticmethod
    def plot_scatter(title,
                     dataframe: pd.DataFrame,
                     xlabel,
                     ylabel,
                     file_path=None,
                     file_name=None):
        plt.clf()
        prepared_dataframe = Output._prepare_dataframe(dataframe)
        colors = Output._get_colors(prepared_dataframe)
        kwargs = {}
        if colors:
            kwargs["color"] = colors
        prepared_dataframe.plot(
            kind='line',
            xlabel=xlabel,
            ylabel=ylabel,
            title=title,
            style='.-',
            grid=True,
            linewidth=0.5,
            ms=3,
            **kwargs
        )
        plt.legend(bbox_to_anchor=(1.0, 1.0))
        if file_path and file_name:
            plt.savefig(f'{file_path}/{file_name}.png')
        else:
            plt.show()

    @staticmethod
    def box_plot(title, dataframe, file_path=None, file_name=None, ignore_clean=False, hide_outliers=False):
        prepared_dataframe = dataframe
        if not ignore_clean:
            prepared_dataframe = Output._prepare_dataframe(dataframe)
        plt.clf()
        prepared_dataframe.plot(
            title=title,
            kind='box',
            grid=True,
            rot=-20,
            showfliers=not hide_outliers
        )
        if file_path and file_name:
            plt.savefig(f'{file_path}/{file_name}.png')
        else:
            plt.show()

    @staticmethod
    def plot_3d(title, x_label, y_label, z_label, dataframe: pd.DataFrame):
        fig = go.Figure(data=[go.Surface(z=dataframe.values)])
        fig.update_layout(title=title, autosize=False,
                          width=1000, height=1000,
                          scene=dict(
                              xaxis=dict(title=x_label,
                                         # tickmode='linear',
                                         # tick0=dataframe.columns.values[0],
                                         # dtick=100,
                                         # tickmode='array',
                                         ticktext=dataframe.columns,
                                         # tickvals=list(range(0, dataframe.shape[1]))
                                         ),
                              yaxis=dict(title=y_label,
                                         ticktext=dataframe.index,
                                         # tickvals=list(range(0, dataframe.shape[0]))
                                         ),
                              zaxis=dict(title=z_label),
                          ),
                          )
        fig.show()

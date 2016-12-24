import json
import pandas as pd
import itertools
import plotly.offline as po
from plotly.graph_objs import *
import plotly.graph_objs as go


def generate_bar_chart(frequency_token, number_of_word, title=None):

    token = ["Value: " + str(token_distri[0]) if isinstance(token_distri[0], int) else token_distri[0] for token_distri in frequency_token]
    frequency = [token_distri[1] for token_distri in frequency_token]
    distribution = [go.Bar(
            x=token[:number_of_word],
            y=frequency[:number_of_word]
    )]
    layout = go.Layout(
        title=title
    )
    fig = go.Figure(data=distribution, layout=layout)
    po.iplot(fig)


def generate_histogram(values, title, label):
    trace = go.Histogram(
                x=values,
                opacity=0.90,
                name=label
    )
    data = [trace]
    layout = go.Layout(
        title=title,
        barmode='group'
    )
    fig = go.Figure(data=data, layout=layout)
    po.iplot(fig)


def generate_histograms(title, *args):
    data = []
    labelizer = False
    values = []
    labels = []
    for arg in args:
        if labelizer:
            labels.append(arg)
            labelizer = False
        else:
            values.append(arg)
            labelizer = True
    for index, label in enumerate(labels):
        trace = go.Histogram(
                    x=values[index],
                    opacity=0.90,
                    name=label,
                    histnorm='probability'
                )
        data.append(trace)
    layout = go.Layout(
        xaxis=dict(
            autotick=True,
            type='category'
        ),
        title=title,
        barmode='group'
    )
    fig = go.Figure(data=data, layout=layout)
    po.iplot(fig)


def generate_pie(dictionary, title):
    pie_values = []
    labels = []
    for key, value in dictionary.iteritems():
        pie_values.append(value)
        labels.append(key)
    fig = {
        'data': [{'labels': labels,
                  'values': pie_values,
                  'type': 'pie'}],
        'layout': {'title': title}
     }

    po.iplot(fig)


def load_data_from_file(file_name):
    data = None
    with open('../data/{0}'.format(file_name)) as data_file:
        if file_name.split('.')[1] == 'json':
            data = json.load(data_file)
        if file_name.split('.')[1] == 'csv':
            data = pd.read_csv(data_file, delimiter=',')
            data = data.to_json()
            data = json.loads(data)
            well_formated = {}
            for key, postId in data['postId'].iteritems():
                well_formated[postId] = {}
                well_formated[postId]['wordLevel'] = data['wordLevel'][key]
                well_formated[postId]['videoSpeed'] = data['videoSpeed'][key]
                well_formated[postId]['subtitleLengthRatio'] = data['subtitleLengthRatio'][key]
                well_formated[postId]['sectionLength'] = data['sectionLength'][key]
                well_formated[postId]['wordList'] = data['wordList'][key]
            data = well_formated
    return data

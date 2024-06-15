import pandas as pd
import dash_leaflet as dl
from dash import Dash, html

# initializing parameters
nihonbashi = [35.6803,139.7716]

data = pd.read_csv('data_lonlat.csv')
markers = []
for _, row in data.iterrows():
    marker_element = html.Div(
        [
            html.A(row['title_detail'], href = row['url'], target = '_blank'),
            html.P('発生日：' + row['incident_date'])
        ]
    )
    marker = dl.Marker(title = row['title_detail'],
                       position = (row['lat'], row['lon']),
                       children = [dl.Popup(marker_element)]
                       )
    markers.append(marker)

app = Dash()
server = app.server

map = dl.Map(
    children = [
    dl.TileLayer(),
    dl.LocateControl(locateOptions={'enableHighAccuracy': True}),
    *markers
    ],
    center = nihonbashi,
    zoom=14, 
    style={'height': '70vh', 'width': '100%', 'margin': '0 auto'},
    
)

header = html.H1(
        '東京不審者マップ', 
        style={'textAlign': 'center', 'color': '#503D36','font-size': 40}
        )

description = html.Ul(children = [
    html.H3('このウェブアプリについて'),
    html.Li('2024年4月から同年6月半ばにかけての東京都の不審者情報を地図上に表示します'),
    html.Li('マーカーをクリックすると不審者情報を表示します'),
    html.Li('矢印ボタンを押すと現在位置を取得し周辺を表示します'),
    html.Br(),
    html.H3('データについて'),
    html.Li(children = ['データは', html.A('日本不審者情報センター', href = 'https://fushinsha-joho.co.jp/', target = '_blank'), 'から取得しました']),
    html.Li('その著作権は日本不審者情報センター合同会社に帰属します')
            ])

app.layout = html.Div(children = [header, map, description])

if __name__ == '__main__':
    app.run_server(debug = False)

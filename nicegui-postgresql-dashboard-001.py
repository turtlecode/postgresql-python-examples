'''
CREATE TABLE sales_data (
    id SERIAL PRIMARY KEY,
    category VARCHAR(50),
    sales_amount INTEGER
);

INSERT INTO sales_data (category, sales_amount) 
VALUES ('Electronics', 4500), 
	   ('Home Decor', 3200), 
	   ('Software', 7800), 
	   ('Books', 1200);

select * from sales_data;

update sales_data
set sales_amount = 5000
where category = 'Books';
'''
from nicegui import ui
import psycopg2
import pandas as pd
import plotly.express as px


DB_CONFIG = {
    'dbname': 'postgres',
    'user': 'postgres',
    'password': 'turtlecode',
    'host': 'localhost',
    'port': '5432',
}


def fetch_data():
    try:
        conn = psycopg2.connect(**DB_CONFIG, connect_timeout=2)
        df = pd.read_sql(
            "SELECT category, sales_amount FROM sales_data",
            conn
        )
        conn.close()
        return df
    except Exception as e:
        print('DB ERROR:', e)
        return pd.DataFrame(columns=['category', 'sales_amount'])


class Dashboard:

    def __init__(self):
        self.df = pd.DataFrame(columns=['category', 'sales_amount'])

        with ui.row().classes('w-full justify-center'):
            ui.label('Colorful Sales Dashboard').classes(
                'text-h4 q-ma-md font-bold text-secondary'
            )


        with ui.row().classes('w-full justify-center gap-4'):

            # TABLE
            with ui.card().classes('w-full max-w-md'):
                ui.label('Raw Data').classes('text-lg font-bold')
                self.table = ui.table(
                    columns=[
                        {'name': 'category', 'label': 'Category', 'field': 'category'},
                        {'name': 'sales_amount', 'label': 'Sales Amount', 'field': 'sales_amount'},
                    ],
                    rows=[]
                ).classes('w-full')

            # CHART
            with ui.card().classes('w-full max-w-2xl'):
                ui.label('Category Performance').classes('text-lg font-bold')
                self.plot = ui.plotly({}).classes('w-full')

        ui.button(
            'Update Data',
            icon='refresh',
            on_click=self.refresh_all
        ).classes('fixed-bottom-right q-ma-lg')

        # 🔥 Load after UI ready
        ui.timer(0.1, self.refresh_all, once=True)

    def update_chart(self):
        if self.df.empty:
            return

        fig = px.bar(
            self.df,
            x='category',
            y='sales_amount',
            color='category',  # 🎨 RENK BURADA
            color_discrete_sequence=px.colors.qualitative.Pastel
        )

        fig.update_layout(
            height=350,
            showlegend=False,
            margin=dict(l=20, r=20, t=20, b=20),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
        )

        self.plot.update_figure(fig)

    def refresh_all(self):
        self.df = fetch_data()
        self.table.rows = self.df.to_dict('records')
        self.update_chart()
        ui.notify('Data refreshed!', color='positive')


@ui.page('/')
def main_page():
    ui.colors(primary='#5898d4', secondary='#2c3e50')
    Dashboard()


ui.run(
    title='Multi-Color Dashboard',
    port=8081,
    reload=False
)

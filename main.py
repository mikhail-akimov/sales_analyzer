import click
import pandas as pd
from datetime import date
from config import path_to_file


class Sales:
    def __init__(self, path):
        self.raw_data = self.get_data_from_csv(path)
        self.data = self.prepare_data()
        self.profit = None
        self.best_profit_sku = None
        self.best_sales_sku = None
        self.best_quantity_sku = None
        self.worst_profit_sku = None
        self.worst_sales_sku = None
        self.worst_quantity_sku = None
        self.avg_delivery_time = None
        self.normal_delivery_delta = None

    @staticmethod
    def get_data_from_csv(path: str) -> pd.DataFrame:
        df = pd.read_csv(path, sep=';', comment='#', decimal=',')
        return df

    def prepare_data(self) -> pd.DataFrame:
        data = self.raw_data
        data.fillna(0, inplace=True)
        data['Order Date'] = pd.to_datetime(data['Order Date'])
        data['Ship Date'] = pd.to_datetime(data['Ship Date'])
        data['Profit'] = data['Profit'].round(decimals=2)
        return data

    def count_profit(self) -> float:
        self.profit = self.data['Profit'].sum()
        return self.profit

    def get_best_profit(self) -> str:
        df = self.data.groupby(['Product ID'])['Profit'].sum().reset_index()
        self.best_profit_sku = df.sort_values(
            by=['Profit'], ascending=False).iloc[0]['Product ID']
        return self.best_profit_sku

    def get_best_sales(self) -> str:
        df = self.data.groupby(['Product ID'])['Sales'].sum().reset_index()
        self.best_sales_sku = df.sort_values(
            by=['Sales'], ascending=False).iloc[0]['Product ID']
        return self.best_sales_sku

    def get_best_quantity(self) -> str:
        df = self.data.groupby(['Product ID'])['Quantity'].sum().reset_index()
        self.best_quantity_sku = df.sort_values(
            by=['Quantity'], ascending=False).iloc[0]['Product ID']
        return self.best_quantity_sku

    def get_worst_profit(self) -> str:
        df = self.data.groupby(['Product ID'])['Profit'].sum().reset_index()
        self.worst_profit_sku = df.sort_values(
            by=['Profit'], ascending=True).iloc[0]['Product ID']
        return self.worst_profit_sku

    def get_worst_sales(self) -> str:
        df = self.data.groupby(['Product ID'])['Sales'].sum().reset_index()
        self.worst_sales_sku = df.sort_values(
            by=['Sales'], ascending=True).iloc[0]['Product ID']
        return self.worst_sales_sku

    def get_worst_quantity(self) -> str:
        df = self.data.groupby(['Product ID'])['Quantity'].sum().reset_index()
        self.worst_quantity_sku = df.sort_values(
            by=['Quantity'], ascending=True).iloc[0]['Product ID']
        return self.worst_quantity_sku

    def get_avg_delivery_time(self) -> str:
        df = self.data.groupby(['Order ID',
                                'Order Date',
                                'Ship Date']
                               ).mean().reset_index()
        df['Delivery'] = df['Ship Date'] - df['Order Date']
        result = df['Delivery'].mean()
        self.avg_delivery_time = str(result).split('.')[0]
        df = df[['Order ID', 'Order Date', 'Ship Date', 'Delivery']]
        avg_delivery_time = df['Delivery'].mean()
        df['Delta'] = df['Delivery'] - avg_delivery_time
        df['count'] = df.groupby('Delta')['Delta'].transform('count')
        delta = df.sort_values(by=['count'], ascending=False).iloc[0]['Delta']
        self.normal_delivery_delta = str(delta).split('.')[0]
        return self.avg_delivery_time

    def get_normal_delivery_delta(self) -> str:
        if not self.normal_delivery_delta:
            self.get_avg_delivery_time()
        return self.normal_delivery_delta

    def get_sales_statistics(self):
        df = self.data.groupby([
            'Product ID',
            'Product Name',
        ])[['Sales', 'Quantity', 'Profit']].sum().reset_index()
        self.save_df_to_csv(df)

    @staticmethod
    def save_df_to_csv(df: pd.DataFrame):
        df.to_csv(f'sales_statistics_{date.today()}.csv', sep=',', index=False)


@click.command()
@click.option('--file', default=path_to_file, help='path to file with sales')
def main(file):
    try:
        sales = Sales(file)
    except FileNotFoundError:
        print('There is no input file. Please use `--file`.')
    else:
        sales.count_profit()
        print('Total profit is - {0}'.format(sales.profit))
        sales.get_best_profit()
        print('Product with best profit is - {0}'.format(sales.best_profit_sku))
        sales.get_best_sales()
        print('Product with best sales is - {0}'.format(sales.best_sales_sku))
        sales.get_best_quantity()
        print('Product with best quantity is - {0}'.format(sales.best_quantity_sku))
        sales.get_worst_profit()
        print('Product with worst profit is - {0}'.format(sales.worst_profit_sku))
        sales.get_worst_sales()
        print('Product with worst sales is - {0}'.format(sales.worst_sales_sku))
        sales.get_worst_quantity()
        print('Product with worst quantity is - {0}'.format(sales.worst_quantity_sku))
        sales.get_avg_delivery_time()
        print('Average delivery time is - {0}'.format(sales.avg_delivery_time))
        sales.get_normal_delivery_delta()
        print('Standart delivery delta - {0}'.format(sales.normal_delivery_delta))
        sales.get_sales_statistics()
        print('File with sales statistics generated.')


if __name__ == '__main__':
    main()

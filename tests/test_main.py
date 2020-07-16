from main import Sales
import pandas.api.types as ptypes
from config import path_to_test_file


class TestStat:

    def setup_class(self):
        self.test_data = Sales(path_to_test_file)

    def teardown_class(self):
        self.test_data = None

    def test_parsing_data_from_csv(self):
        assert isinstance(self.test_data, Sales)

    def test_profit_round(self):
        assert self.test_data.data['Profit'].max() == 85.79

    def test_date_field_types(self):
        assert ptypes.is_datetime64_any_dtype(self.test_data.data['Order Date'])
        assert ptypes.is_datetime64_any_dtype(self.test_data.data['Ship Date'])

    def test_profit(self):
        assert self.test_data.profit is None
        assert self.test_data.count_profit() == 17.37

    def test_best_profit_sku(self):
        assert self.test_data.best_profit_sku is None
        assert self.test_data.get_best_profit() == 'TEC-AC-10003033'

    def test_get_best_sales(self):
        assert self.test_data.best_sales_sku is None
        assert self.test_data.get_best_sales() == 'TEC-PH-10001363'

    def test_get_best_quantity(self):
        assert self.test_data.best_quantity_sku is None
        assert self.test_data.get_best_quantity() == 'OFF-AP-10001947'

    def test_get_worst_profit_sku(self):
        assert self.test_data.worst_profit_sku is None
        assert self.test_data.get_worst_profit() == 'TEC-PH-10001363'

    def test_get_worst_sales(self):
        assert self.test_data.worst_sales_sku is None
        assert self.test_data.get_worst_sales() == 'OFF-BI-10000145'

    def test_get_worst_quantity(self):
        assert self.test_data.worst_quantity_sku is None
        assert self.test_data.get_worst_quantity() == 'OFF-AR-10003602'

    def test_get_avg_delivery_time(self):
        assert self.test_data.get_avg_delivery_time() == '3 days 08:00:00'

    def test_get_delta_delivery_time(self):
        assert self.test_data.get_normal_delivery_delta() == '-2 days +16:00:00'

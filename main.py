import time
from itertools import count

import data
import helpers

from pages import UrbanRoutesPage
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestUrbanRoutes:
    @classmethod
    def setup_class(cls):
        from selenium.webdriver import DesiredCapabilities
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
        cls.driver = Chrome()
        cls.driver.implicitly_wait(5)

        if helpers.is_url_reachable(data.URBAN_ROUTES_URL):
            print("Conectado ao servidor Urban Routes")
        else:
            print("Não foi possível conectar ao Urban Routes. Verifique se o servidor está ligado e ainda em execução.")

    def setup_method(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        self.pages = UrbanRoutesPage(self.driver)
        self.pages.enter_locations(data.ADDRESS_FROM, data.ADDRESS_TO)


    def test_set_route(self):
        assert  self.pages.get_from_location() == data.ADDRESS_FROM
        assert self.pages.get_to_location() == data.ADDRESS_TO


    def test_select_plan(self):
        self.pages.click_taxi_option()
        self.pages.click_icon_comfort_selected()
        assert self.pages.is_comfort_icon_active()

    def test_fill_phone_number(self):
        self.pages.click_taxi_option()
        self.pages.set_phone_number('+11111111111')
        self.pages.set_sms_code()

    def test_fill_card(self):
        self.pages.click_taxi_option()
        self.pages.click_payment_method_()
        self.pages.click_add_card_button()
        self.pages.fill_card_data()
        self.pages.confirm_card()


    def test_comment_for_driver(self):
        self.pages.click_taxi_option()
        self.pages.click_comment_field()
        driver_message = "Traga os lanchinhos"
        comment_input_value = self.driver.find_element(*self.pages.comment_field).get_attribute('value')
        assert comment_input_value == driver_message

    def test_order_blanket_and_handkerchiefs(self):
        self.pages.click_taxi_option()
        self.pages.click_icon_comfort_selected()
        self.pages.toggle_blanket_and_tissues()
        is_selected = self.pages.is_blanket_activated()
        assert is_selected is True, f"Esperado True, mas o status da manta foi {is_selected}"

    def test_order_2_ice_creams(self):
        self.pages.add_ice_cream(2)
        count = self.pages.get_ice_cream()
        assert count == 2, f"Esperado 2 sorvetes, mas o contador marcou {count}"
    def test_order_2_ice_creams(self):
        numbers_of_ice_creams = 2
        for count in range(numbers_of_ice_creams):
         print("função criada para adicionar sorvete")
         pass


    def test_car_search_model_appears(self):
        self.pages.click_taxi_option()
        self.pages.click_icon_comfort_selected()
        self.pages.click_comment_field()
        driver_message = "Traga os lanchinhos"
        self.pages.click_order_taxi_button()
        assert self.pages.click_order_modal_present() is True, "A janela modal de busca de carros não apareceu!"


        @classmethod
        def teardown_class(cls):
            cls.driver.quit()
from dataclasses import field
from html.parser import commentclose

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time
import helpers
from selenium.webdriver.common.action_chains import ActionChains
import time
from selenium.webdriver.common.keys import Keys

class UrbanRoutesPage:
    #Seção De e Para
    from_field =(By.ID, 'from')
    to_field =(By.ID, 'to')

    #Fluxo de chamada de taxi
    taxi_option = (By.XPATH, '//button[contains(text(),"Chamar")]')
    comfort_icon = (By.XPATH, '//img[contains(@src,"kids")]')
    comfort_active = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[1]/div[5]')

    #Adicionar número de telefone
    phone_number = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[1]')
    phone_input = (By.ID,'phone')
    next_button = (By.XPATH, '//*[@id="root"]/div/div[1]/div[2]/div[1]/form/div[2]/button')
    sms_code_input = (By.XPATH, '//*[@id="root"]/div/div[1]/div[2]/div[2]/form/div[1]/div[1]')
    confirm_button = (By.XPATH, '//*[@id="root"]/div/div[1]/div[2]/div[2]/form/div[2]/button[1]')

    #Adicionar um cartão de crédito
    payment_method_button = (By.CLASS_NAME, "pp-text")
    add_card_button_modal =(By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[1]/div[2]/div[3]/div[3]/div')
    card_number_input = (By.ID, "number")
    card_code_input = (By.NAME, 'code')
    confirm_card_button = (By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[2]/form/div[3]/button[1]')

    #Deixar recado para o motorista
    comment_field = (By.ID, 'comment')

    #Pedir Leçóis e cobertores
    comfort_icon = (By.XPATH, '//img[contains(@src,"kids")]')
    blanket_switch_clickable = (By.CLASS_NAME, 'switch')
    blanket_checkbox_status = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[1]/div/div[2]/div/input')


    #Pedir 2 sorvetes
    comfort_icon = (By.XPATH, '//img[contains(@src,"kids")]')
    ice_cream_plus_button = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[3]/div/div[2]/div[1]/div/div[2]/div/div[3]')
    ice_cream_counter_value = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[3]/div/div[2]/div[1]/div/div[2]/div/div[2]')

    #Pedir carro 'confort' e enviar mensagem para o motorista
    taxi_option = (By.XPATH, '//button[contains(text(),"Chamar")]')
    comfort_icon = (By.XPATH, '//img[contains(@src,"kids")]')
    comment_field = (By.ID, 'comment')
    smart_button = (By.XPATH, '//*[@id="root"]/div/div[3]/div[4]/button')
    order_modal_present_button = (By.CSS_SELECTOR, '.order-header-title')


    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    #Métodos COR POM

    def _find(self, locator):
        return self.wait.until(
            EC.visibility_of_element_located(locator)
        )

    def _click(self, locator):
        self.wait.until(
            EC.element_to_be_clickable(locator)
        ) .click()

    def _type(self, locator, text):
        element = self._find(locator)
        element.clear()
        element.send_keys(text)

    #Definir o endereço

    def _get_text(self, locator):
        return self.find(locator).text

    def _get_value(self, locator):
        return self._find(locator).get_attribute('value')

    def enter_locations(self, from_text, to_text):
        self._type(self.from_field, from_text)
        self._type(self.to_field, to_text)

    def get_from_location(self):
        return self._get_value(self.from_field)

    def get_to_location(self):
        return self._get_value(self.to_field)

    #Selecionar o plano Comfort
    def click_taxi_option(self):
        self.driver.find_element(*self.taxi_option).click()

    def click_icon_comfort_selected(self):
        self.driver.find_element(*self.comfort_icon).click()

    def is_comfort_icon_active(self):
        try:
            self.wait.until(EC.visibility_of_element_located(self.comfort_active))
            active_button = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located(self.comfort_active)
            )
            return "active" in active_button.get_attribute("class")
        except:
            return False

    #Preencher o número de telefone
    def set_phone_number(self, phone_number):
        self.wait.until(EC.element_to_be_clickable(self.phone_number))
        active_button = WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located(self.phone_number)).click()
        self.driver.find_element(*self.phone_input).send_keys('+11111111111')
        self.driver.find_element(*self.next_button).click()

    def set_sms_code(self):
        code = helpers.retrieve_phone_code(self.driver)
        time.sleep(1)
        sms_input = self.wait.until(EC.visibility_of_element_located(self.sms_code_input))
        actions = ActionChains(self.driver)
        actions.move_to_element(sms_input).click().send_keys(code).perform()
        self.driver.find_element(*self.confirm_button).click()

    #Adicionar carão de crédito
    def click_payment_method_(self):
        self.wait.until(EC.element_to_be_clickable(self.payment_method_button)).click()

    def click_add_card_button(self):
         self.wait.until(EC.element_to_be_clickable(self.add_card_button_modal)).click()

    def click_add_card_confirm(self):
        self.wait.until(EC.element_to_be_clickable(self.card_number_input)).click()

    def fill_card_data(self):
        num_field = self.wait.until(EC.visibility_of_element_located(self.card_number_input))
        num_field.send_keys('1111111111')
        cvv_field = self.wait.until(EC.visibility_of_element_located(self.card_code_input))
        cvv_field.send_keys('12')
        cvv_field.send_keys(Keys.TAB)

    def confirm_card(self):
        self.wait.until(EC.element_to_be_clickable(self.confirm_card_button)).click()


    #Deixar um recado para o motorista
    def click_comment_field(self):
        comment_input = self.wait.until(EC.visibility_of_element_located(self.comment_field))
        comment_input.send_keys('Traga os lanchinhos')


    #Pedir lençóis e cobertores
    def click_comfort_tarif(self):
        self.wait.until(EC.visibility_of_element_located(self.comfort_tarif_card)).click()
    def toggle_blanket_and_tissues(self):
        self.wait.until(EC.element_to_be_clickable(self.blanket_switch_clickable)).click()
    def is_blanket_activated(self):
        checkbox = self.driver.find_element(*self.blanket_checkbox_status)
        return checkbox.get_property('checked')


    #Pedir 2 sorvetes
    def add_ice_cream(self, quantity):
        plus_button = self.wait.until(EC.element_to_be_clickable(self.ice_cream_plus_button))
        for _ in range(quantity):
            plus_button.click()
    def get_ice_cream(self):
        return int(self.driver.find_element(*sel.ice_cream_counter_value).text)




    #Pedir um táxi "confort" e mandar uma mensagem para o morotista
    def click_taxi_option(self):
        self.driver.find_element(*self.taxi_option).click()
    def click_icon_comfort_selected(self):
        self.driver.find_element(*self.comfort_icon).click()
    def click_comment_field(self):
            comment_input = self.wait.until(EC.visibility_of_element_located(self.comment_field))
            comment_input.send_keys('Traga os lanchinhos')
    def click_order_taxi_button(self):
        self.wait.until(EC.element_to_be_clickable(self.smart_button)).click()
    def click_order_modal_present(self):
        try:
            WebDriverWait(self.driver, 15).until(
                EC.visibility_of_element_located(self.order_modal_present_button)
            )
            return True
        except:
            return False

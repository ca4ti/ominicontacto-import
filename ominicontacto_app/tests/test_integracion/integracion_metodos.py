from __future__ import unicode_literals
from time import sleep

import os
import socket
from selenium.webdriver.common.by import By

ADMIN_USERNAME = os.getenv('ADMIN_USERNAME')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')
ADMIN_PASSWORD_RESET = '098098ZZZ'
USER = os.getenv('USER')

CAMPANA_MANUAL = os.getenv('CAMPANA_MANUAL')

AGENTE_PASSWORD = '098098ZZZ'

TESTS_INTEGRACION = os.getenv('TESTS_INTEGRACION')

TESTS_INTEGRACION_HOSTNAME = os.getenv('TESTS_INTEGRACION_HOSTNAME')
if not TESTS_INTEGRACION_HOSTNAME:
    TESTS_INTEGRACION_HOSTNAME = socket.gethostname()


def login(browser, username, password):
    browser.get('https://{0}'.format(TESTS_INTEGRACION_HOSTNAME))
    browser.find_element_by_name('username').send_keys(username)
    if username == ADMIN_USERNAME:
        # Para logearse por primera vez en un entorno desde cero
        try:
            browser.find_element_by_name('password').send_keys(password)
            browser.find_element_by_tag_name('button').click()
            sleep(1)
        except Exception:
            pass

        # Cuando ya tiene la nueva password seteada
        try:
            browser.find_element_by_name('password').send_keys(ADMIN_PASSWORD_RESET)
            browser.find_element_by_tag_name('button').click()
            sleep(1)
        except Exception:
            pass

    else:
        browser.find_element_by_name('password').send_keys(password)
        browser.find_element_by_tag_name('button').click()
        sleep(1)

    # Setea password nuevo para nuevos usuarios
    try:
        browser.find_element_by_name('password1').send_keys(ADMIN_PASSWORD_RESET)
        browser.find_element_by_name('password2').send_keys(ADMIN_PASSWORD_RESET)
        browser.find_element_by_tag_name('button').click()
        sleep(1)
    except Exception:
        pass

    # Prueba si Django toolbar esta abierto y lo cierra
    try:
        if browser.find_elements_by_id('djHideToolBarButton'):
            browser.find_element_by_id('djHideToolBarButton').click()
            sleep(1)
    except Exception:
        pass


def crear_user(browser, username, password, tipo_usuario):
    link_create_user = browser.find_element_by_xpath('//a[contains(@href,"/user/nuevo/")]')
    href_create_user = link_create_user.get_attribute('href')
    browser = browser
    browser.get(href_create_user)
    browser.find_element_by_id('id_0-username').send_keys(username)
    browser.find_element_by_id('id_0-first_name').send_keys(username)
    browser.find_element_by_id('id_0-password1').send_keys(password)
    browser.find_element_by_id('id_0-password2').send_keys(password)
    browser.find_element_by_xpath("//select[@id='id_0-rol']//option[contains\
                                       (text(), \'{0}\')]".format(tipo_usuario)).click()
    if tipo_usuario == 'Agente':
        browser.find_element_by_xpath("//form[@id=\'wizardForm\']/button").click()
        sleep(1)
        browser.find_elements_by_xpath("//select[@id='id_1-grupo']/option")[1].click()
        browser.find_elements_by_xpath("//form[@id=\'wizardForm\']/button")[2].click()
        sleep(1)
    else:
        browser.find_element_by_xpath('//form[@id=\'wizardForm\']/button').click()
        sleep(1)


def crear_grupo(browser, group_name):
    link_create_group = browser.find_element_by_xpath(
        '//a[contains(@href,"/grupo/nuevo")]')
    href_create_group = link_create_group.get_attribute('href')
    browser.get(href_create_group)
    browser.find_element_by_id('id_nombre').send_keys(group_name)
    browser.find_element_by_id('id_auto_attend_inbound').click()
    browser.find_element_by_id('id_auto_attend_dialer').click()
    browser.find_element_by_xpath((
        "//button[@type='submit' and @id='id_registrar']")).click()
    sleep(1)


def asignar_agente_campana_manual(browser, agente):
    list_manual_href = browser.find_element_by_xpath(
        '//a[contains(@href,"/campana_manual/lista/")]')
    href_manual = list_manual_href.get_attribute('href')
    browser.get(href_manual)
    link_add_agent = browser.find_element_by_xpath(
        '//tr[@id=\'{0}\']/td/div//a[contains(@href, "/queue_member/")]'.format(CAMPANA_MANUAL))
    href_add_agent = link_add_agent.get_attribute('href')
    browser.get(href_add_agent)
    browser.find_element_by_xpath('//select/option[contains(text(), \'{0}\')]'
                                  .format(agente)).click()
    browser.find_element_by_xpath((
        "//button[@id='id_guardar']")).click()
    sleep(1)


def get_href(browser, path):
    link = browser.find_element(By.XPATH, path)
    href = link.get_attribute('href')
    browser.get(href)


def crear_BD(browser, path, base_datos, multinum):
    login(browser, ADMIN_USERNAME, ADMIN_PASSWORD)
    href_nueva_BD = '//a[contains(@href,"/base_datos_contacto/nueva/")]'
    get_href(browser, href_nueva_BD)
    browser.find_element_by_id('id_nombre').send_keys(base_datos)
    browser.find_element_by_id('id_archivo_importacion').send_keys(path)
    browser.find_element_by_xpath("//button[@type='submit']").click()
    sleep(1)

    if multinum:
        browser.find_element_by_xpath('//label/input[@value = "phone"]').click()
        browser.find_element_by_xpath('//label/input[@value = "cell"]').click()
    else:
        browser.find_element_by_xpath('//label/input[@value = "telefono"]').click()

    browser.find_element_by_xpath("//button[@type='submit']").click()
    sleep(1)


def crear_blacklist(browser, path, base_datos):
    link_create_blacklist = '//a[contains(@href,"/blacklist/nueva")]'
    get_href(browser, link_create_blacklist)
    browser.find_element(By.NAME, 'nombre').send_keys(base_datos)
    browser.find_element(By.NAME, 'archivo_importacion').send_keys(path)
    browser.find_element(By.CSS_SELECTOR, ".btn-primary").click()
    browser.implicitly_wait(3)


def crear_lista_rapida(browser, path, nombre_lista):
    link_create = '//a[contains(@href,"/lista_rapida/nueva/")]'
    get_href(browser, link_create)
    browser.find_element(By.NAME, 'nombre').send_keys(nombre_lista)
    browser.find_element(By.NAME, 'archivo_importacion').send_keys(path)
    browser.find_element(By.CSS_SELECTOR, ".btn-primary").click()
    sleep(1)


def crear_campos_formulario(browser, campos):
    for items in campos:
        browser.find_element(By.NAME, 'nombre_campo').send_keys(items)
        if items == 'Nombre':
            browser.find_element(By.XPATH, "//option[. = 'Text']").click()
        elif items == 'Fecha_nacimiento':
            browser.find_element(By.XPATH, "//option[. = 'Date']").click()
        elif items == 'Opciones':
            browser.find_element(By.XPATH, "//option[. = 'List']").click()
            for i in range(10):
                browser.find_element(By.NAME, "value_item").send_keys(i)
                browser.find_element(By.ID, "agregar_lista").click()
                sleep(1)
        elif items == 'Comentarios':
            browser.find_element(By.XPATH, "//option[. = 'Text area box']").click()
        browser.find_element_by_xpath("//button[@type='submit']").click()
        sleep(1)


def crear_calificacion(browser, items):
    calificacion = browser.find_element_by_xpath(
        "//a[contains(@href, '/calificacion/nuevo/')]")
    href_calificacion = calificacion.get_attribute('href')
    browser.get(href_calificacion)
    browser.find_element_by_id('id_nombre').send_keys(items)
    browser.find_element_by_xpath("//button[@type='submit']").click()
    sleep(1)


def sitio_externo(browser, sitio, url):
    nuevo_sitio = '//a[contains(@href, "/sitio_externo/nuevo/")]'
    get_href(browser, nuevo_sitio)
    browser.find_element_by_id('id_nombre').send_keys(sitio)
    browser.find_element_by_id('id_url').send_keys(url)


def formato_sitio(browser, items):
    if items == 'multipart':
        browser.find_elements_by_xpath(
            '//select[@id=\'id_formato\']/option')[1].click()
    elif items == 'urlencoded':
        browser.find_elements_by_xpath(
            '//select[@id=\'id_formato\']/option')[2].click()
    elif items == 'text':
        browser.find_elements_by_xpath(
            '//select[@id=\'id_formato\']/option')[3].click()
    elif items == 'json':
        browser.find_elements_by_xpath(
            '//select[@id=\'id_formato\']/option')[4].click()
    browser.find_element_by_xpath("//button[@type='submit']").click()
    sleep(1)

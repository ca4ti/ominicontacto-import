# -*- coding: utf-8 -*-
# Copyright (C) 2018 Freetech Solutions

# This file is part of OMniLeads

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see http://www.gnu.org/licenses/.
#

from __future__ import unicode_literals

from django.urls import reverse

from ominicontacto_app.models import SitioExterno, ParametrosCrm
from ominicontacto_app.tests.utiles import OMLBaseTest
from ominicontacto_app.tests.factories import (
    SitioExternoFactory, CampanaFactory, ParametrosCrmFactory, ContactoFactory, COLUMNAS_DB_DEFAULT)


class TestsABMSitioExterno(OMLBaseTest):
    PWD = u'admin123'

    def setUp(self, *args, **kwargs):
        super(TestsABMSitioExterno, self).setUp(*args, **kwargs)

        self.admin = self.crear_administrador()
        self.agente = self.crear_user_agente()
        self.agente.set_password(self.PWD)
        self.admin.set_password(self.PWD)

        self.sitio_externo = SitioExternoFactory()

    def _obtener_post_sitio_externo(self):
        return {
            'nombre': 'test_ruta_entrante',
            'url': 'http://www.infobae.com/',
            'disparador': SitioExterno.BOTON,
            'metodo': SitioExterno.GET,
            # 'formato': None,
            'objetivo': SitioExterno.EMBEBIDO,
        }

    def test_crear_sitio_externo(self):
        url = reverse('sitio_externo_create')
        self.client.login(username=self.admin.username, password=self.PWD)
        post_data = self._obtener_post_sitio_externo()
        n_sitio_externo = SitioExterno.objects.count()
        response = self.client.post(url, post_data, follow=True)
        self.assertEqual(SitioExterno.objects.count(), n_sitio_externo + 1)
        list_url = reverse('sitio_externo_list')
        self.assertRedirects(response, list_url)

    def test_update_sitio_externo(self):
        url = reverse('modificar_sitio_externo', args=[self.sitio_externo.pk])
        self.client.login(username=self.admin.username, password=self.PWD)
        nombre_modificado = 'sitio_crm_ventas'
        post_data = self._obtener_post_sitio_externo()
        post_data['nombre'] = nombre_modificado
        response = self.client.post(url, post_data, follow=True)
        self.sitio_externo.refresh_from_db()
        self.assertEqual(self.sitio_externo.nombre, nombre_modificado)
        list_url = reverse('sitio_externo_list')
        self.assertRedirects(response, list_url)

    def test_admin_elimina_sitio_externo(self):
        url = reverse('sitio_externo_delete', args=[self.sitio_externo.pk])
        self.client.login(username=self.admin.username, password=self.PWD)
        n_sitio_externo = SitioExterno.objects.count()
        response = self.client.post(url, follow=True)
        self.assertEqual(SitioExterno.objects.count(), n_sitio_externo - 1)
        list_url = reverse('sitio_externo_list')
        self.assertRedirects(response, list_url)

    def test_no_se_permite_eliminar_sitio_externo_asociado_campana(self):
        url = reverse('sitio_externo_delete', args=[self.sitio_externo.pk])
        self.client.login(username=self.admin.username, password=self.PWD)
        CampanaFactory.create(sitio_externo=self.sitio_externo, tipo_interaccion=2)
        n_sitio_externo = SitioExterno.objects.count()
        self.client.post(url, follow=True)
        self.assertEqual(SitioExterno.objects.count(), n_sitio_externo)

    def test_usuario_no_admin_no_puede_eliminar_sitio_externo(self):
        self.client.login(username=self.agente.username, password=self.PWD)
        url = reverse('sitio_externo_delete', args=[self.sitio_externo.pk])
        response = self.client.post(url, follow=True)
        self.assertTemplateUsed(response, '403.html')


class TestsSitioExterno(OMLBaseTest):
    PWD = u'admin123'

    def setUp(self, *args, **kwargs):
        self.agente = self.crear_agente_profile()
        self.sitio_externo = SitioExternoFactory()
        self.campana = CampanaFactory(sitio_externo=self.sitio_externo,
                                      tipo_interaccion=2)
        self.contacto = ContactoFactory()
        self.call_data = {
            'call_id': '1234',
            'agent_id': str(self.agente.id),
            'telefono': '351351351',
            'id_contacto': str(self.contacto.id),
            'rec_filename': 'rec_filename',
            'call_wait_duration': '44',
            'Omlcrmnombre_1': 'valor_crm_1',
            'Omlcrmnombre_2': 'valor_crm_2',
        }
        super(TestsSitioExterno, self).setUp(*args, **kwargs)

    def test_obtener_parametros_campana(self):
        nombres = ['id', 'nombre', 'tipo']
        for nombre in nombres:
            ParametrosCrmFactory(campana=self.campana, tipo=ParametrosCrm.DATO_CAMPANA,
                                 nombre=nombre, valor=nombre)
        parametros = self.sitio_externo.get_parametros(self.agente, self.campana, self.contacto,
                                                       self.call_data)
        self.assertEqual(len(parametros), len(nombres))
        for nombre in nombres:
            self.assertIn(nombre, parametros)
        self.assertEqual(parametros['id'], str(self.campana.id))
        self.assertEqual(parametros['nombre'], self.campana.nombre)
        self.assertEqual(parametros['tipo'], self.campana.get_type_display())

    def test_obtener_parametros_llamada(self):
        nombres = ['call_id', 'agent_id', 'telefono', 'id_contacto', 'rec_filename',
                   'call_wait_duration']
        for nombre in nombres:
            ParametrosCrmFactory(campana=self.campana, tipo=ParametrosCrm.DATO_LLAMADA,
                                 nombre=nombre, valor=nombre)
        parametros = self.sitio_externo.get_parametros(self.agente, self.campana, self.contacto,
                                                       self.call_data)
        self.assertEqual(len(parametros), len(nombres))
        for nombre in nombres:
            self.assertIn(nombre, parametros)
        self.assertEqual(parametros['call_id'], self.call_data['call_id'])
        self.assertEqual(parametros['agent_id'], self.call_data['agent_id'])
        self.assertEqual(parametros['telefono'], self.call_data['telefono'])
        self.assertEqual(parametros['id_contacto'], self.call_data['id_contacto'])
        self.assertEqual(parametros['rec_filename'], self.call_data['rec_filename'])
        self.assertEqual(parametros['call_wait_duration'], self.call_data['call_wait_duration'])

    def test_obtener_parametros_contacto(self):
        for nombre in COLUMNAS_DB_DEFAULT:
            ParametrosCrmFactory(campana=self.campana, tipo=ParametrosCrm.DATO_CONTACTO,
                                 nombre=nombre, valor=nombre)
        parametros = self.sitio_externo.get_parametros(self.agente, self.campana, self.contacto,
                                                       self.call_data)
        self.assertEqual(len(parametros), len(COLUMNAS_DB_DEFAULT))
        for nombre in COLUMNAS_DB_DEFAULT:
            self.assertIn(nombre, parametros)

    def test_obtener_parametros_custom(self):
        ParametrosCrmFactory(campana=self.campana, tipo=ParametrosCrm.CUSTOM,
                             nombre='nombre_1', valor='valor_1')
        ParametrosCrmFactory(campana=self.campana, tipo=ParametrosCrm.CUSTOM,
                             nombre='nombre_2', valor='valor_2')
        parametros = self.sitio_externo.get_parametros(self.agente, self.campana, self.contacto,
                                                       self.call_data)
        self.assertEqual(len(parametros), 2)
        self.assertIn('nombre_1', parametros)
        self.assertIn('nombre_2', parametros)
        self.assertEqual(parametros['nombre_1'], 'valor_1')
        self.assertEqual(parametros['nombre_2'], 'valor_2')

    def test_obtener_parametros_cmr(self):
        ParametrosCrmFactory(campana=self.campana, tipo=ParametrosCrm.DIALPLAN,
                             nombre='nombre_1', valor='Omlcrmnombre_1')
        ParametrosCrmFactory(campana=self.campana, tipo=ParametrosCrm.DATO_LLAMADA,
                             nombre='nombre_2', valor='Omlcrmnombre_2')
        parametros = self.sitio_externo.get_parametros(self.agente, self.campana, self.contacto,
                                                       self.call_data)
        self.assertEqual(len(parametros), 2)
        self.assertIn('nombre_1', parametros)
        self.assertIn('nombre_2', parametros)
        self.assertEqual(parametros['nombre_1'], 'valor_crm_1')
        self.assertEqual(parametros['nombre_2'], 'valor_crm_2')

    def test_obtener_beautiful_url_con_parametros(self):
        self.sitio_externo.url = 'https://oml.com/{1}/{2}/{3}/{4}'
        ParametrosCrmFactory(campana=self.campana, tipo=ParametrosCrm.DATO_CONTACTO,
                             nombre='{1}', valor='telefono')
        ParametrosCrmFactory(campana=self.campana, tipo=ParametrosCrm.DATO_CAMPANA,
                             nombre='{2}', valor='id')
        ParametrosCrmFactory(campana=self.campana, tipo=ParametrosCrm.DATO_LLAMADA,
                             nombre='{3}', valor='call_id')
        ParametrosCrmFactory(campana=self.campana, tipo=ParametrosCrm.CUSTOM,
                             nombre='{4}', valor='valor_1')
        url = self.sitio_externo.get_url_interaccion(self.agente, self.campana, self.contacto,
                                                     self.call_data)
        expected_url = 'https://oml.com/' + self.contacto.telefono + '/' + str(self.campana.id)
        expected_url += '/' + self.call_data['call_id'] + '/valor_1'

        self.assertEqual(url, expected_url)
        self.assertEqual(self.sitio_externo.get_parametros(self.agente, self.campana, self.contacto,
                                                           self.call_data), {})

    def test_obtener_get_url_con_parametros_crm(self):
        self.sitio_externo.url = 'https://oml.com/'
        ParametrosCrmFactory(campana=self.campana, tipo=ParametrosCrm.DIALPLAN,
                             nombre='nombre_1', valor='Omlcrmnombre_1')
        ParametrosCrmFactory(campana=self.campana, tipo=ParametrosCrm.DIALPLAN,
                             nombre='nombre_2', valor='Omlcrmnombre_2')
        url = self.sitio_externo.get_url_interaccion(self.agente, self.campana, self.contacto,
                                                     self.call_data, True)
        self.assertIn("nombre_1=valor_crm_1", url)
        self.assertIn("nombre_2=valor_crm_2", url)

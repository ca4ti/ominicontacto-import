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
from django.utils.translation import ugettext_lazy as _
from django.apps import AppConfig


class SupervisionAppConfig(AppConfig):
    name = 'supervision_app'

    def supervision_menu_items(self, request):
        if request.user.get_supervisor_profile():
            return [
                {
                    'label': _('Supervisión'),
                    'icon': 'icon-headset',
                    'id': 'menuSupervise',
                    'children': [
                        {
                            'label': _('Agentes'),
                            'url': reverse('supervision_agentes'),
                        },
                        {
                            'label': _('Campañas Entrantes'),
                            'url': reverse('supervision_campanas_entrantes'),
                        },
                        {
                            'label': _('Campañas Salientes'),
                            'url': reverse('supervision_campanas_salientes'),
                        },
                    ],
                },
            ]
        return None

    def configuraciones_de_permisos(self):
        return [
            {'nombre': 'supervision_agentes',
             'roles': ['Administrador', 'Gerente', 'Supervisor', 'Referente', ]},
            {'nombre': 'supervision_campanas_entrantes',
             'roles': ['Administrador', 'Gerente', 'Supervisor', 'Referente', ]},
            {'nombre': 'supervision_campanas_salientes',
             'roles': ['Administrador', 'Gerente', 'Supervisor', 'Referente', ]},
        ]

    informacion_de_permisos = {
        'supervision_agentes':
            {'descripcion': _('Estado de agentes en supervisión'), 'version': '1.5.1'},
        'supervision_campanas_entrantes':
            {'descripcion': _('Estado de campañas entrantes en supervisión'), 'version': '1.5.1'},
        'supervision_campanas_salientes':
            {'descripcion': _('Estado de campañas salientes en supervision'), 'version': '1.5.1'},
    }

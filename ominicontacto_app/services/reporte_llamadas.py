# -*- coding: utf-8 -*-

"""Servicio para generar reporte de supervision de los agentes """

import pygal
import datetime
import os

from pygal.style import Style, RedBlueStyle

from django.conf import settings
from django.db.models import Count
from ominicontacto_app.models import AgenteProfile, Queuelog, Campana
from ominicontacto_app.services.queue_log_service import AgenteTiemposReporte

import logging as _logging

logger = _logging.getLogger(__name__)


ESTILO_AZUL_ROJO_AMARILLO = Style(
    background='transparent',
    plot_background='transparent',
    foreground='#555',
    foreground_light='#555',
    foreground_dark='#555',
    opacity='1',
    opacity_hover='.6',
    transition='400ms ease-in',
    colors=('#428bca', '#5cb85c', '#5bc0de', '#f0ad4e', '#d9534f',
            '#a95cb8', '#5cb8b5', '#caca43', '#96ac43', '#ca43ca')
)


class EstadisticasService():

    def _obtener_agentes(self):
        return AgenteProfile.objects.all()

    def calcular_tiempo_sesion(self, agentes, fecha_inferior, fecha_superior):
        """
        Calcula el tiempo de session de los agentes en el periodo evaluado
        :return: un listado de agentes con el tiempo de session
        """
        eventos_sesion = ['ADDMEMBER', 'REMOVEMEMBER']

        if fecha_inferior and fecha_superior:
            fecha_desde = datetime.datetime.combine(fecha_inferior,
                                                    datetime.time.min)
            fecha_hasta = datetime.datetime.combine(fecha_superior,
                                                    datetime.time.max)

        logs_queue = Queuelog.objects.filter(
            queuename='ALL',
            event__in=eventos_sesion,
            time__range=(fecha_desde, fecha_hasta)).order_by('-time')

        agentes_tiempo = []

        # iterar por agente evaluando los eventos de session
        for agente in agentes:
            tiempo_agente = []
            logs_time = logs_queue.filter(agent=agente)
            is_remove = False
            time_actual = None
            # iterar los log teniendo en cuenta que si encuentra un evento REMOVEMEMBER
            # y luego un ADDMEMBER calcula el tiempo de session
            for logs in logs_time:
                if is_remove and logs.event == 'ADDMEMBER':
                    resta = time_actual - logs.time
                    tiempo_agente.append(agente)
                    tiempo_agente.append(logs.time.strftime('%Y-%m-%d'))
                    tiempo_string = str(resta) + "hs"
                    tiempo_agente.append(str(tiempo_string))
                    agentes_tiempo.append(tiempo_agente)
                    tiempo_agente = []
                    is_remove = False
                    time_actual = None
                if logs.event == 'REMOVEMEMBER':
                    time_actual = logs.time
                    is_remove = True
        return agentes_tiempo

    def calcular_tiempo_pausa(self, agentes, fecha_inferior, fecha_superior):
        """
        Calcula el tiempo de pausa de los agentes en el periodo evaluado
        :return: un listado de agentes con el tiempo de pausa
        """
        eventos_pausa = ['PAUSEALL', 'UNPAUSEALL']

        agentes_tiempo = []

        # iterar por agente evaluando los eventos de pausa
        for agente in agentes:

            logs_time = Queuelog.objects.obtener_log_agente_pk_event_periodo_all(
                eventos_pausa, fecha_inferior, fecha_superior, agente.id)
            is_unpause = False
            time_actual = None
            tiempos_pausa = {}
            # iterar los log teniendo en cuenta que si encuentra un evento UNPAUSEALL
            # y luego un PAUSEALL calcula el tiempo de session
            for logs in logs_time:
                if is_unpause and logs.event == 'PAUSEALL':
                    resta = time_actual - logs.time
                    if logs.data1 in tiempos_pausa.keys():
                        tiempos_pausa[logs.data1] += resta
                    else:
                        tiempos_pausa.update({logs.data1: resta})
                    is_unpause = False
                    time_actual = None
                if logs.event == 'UNPAUSEALL':
                    time_actual = logs.time
                    is_unpause = True
            for tiempo_pausa in tiempos_pausa:
                tiempo_agente = []

                tiempo_agente.append(agente.user.get_full_name())
                tiempo_agente.append(tiempo_pausa)
                tiempos_pausa[tiempo_pausa] = str(datetime.timedelta(
                    seconds=tiempos_pausa[tiempo_pausa].seconds))
                tiempo_agente.append(tiempos_pausa[tiempo_pausa])
                agentes_tiempo.append(tiempo_agente)

        return agentes_tiempo

    def calcular_tiempo_llamada(self, agentes, fecha_inferior, fecha_superior):
        """
        Calcula el tiempo de llamadas de los agentes en el periodo evaluado
        :return: un listado de agentes con el tiempo de llamadas
        """
        eventos_llamadas = ['COMPLETECALLER', 'COMPLETEAGENT']

        agentes_tiempo = []

        # iterar por agente evaluando los eventos de llamadas
        for agente in agentes:
            logs_time = Queuelog.objects.obtener_log_agente_event_periodo(
                eventos_llamadas, fecha_inferior, fecha_superior, agente)
            llamadas_cola = {}
            for logs in logs_time:
                tiempo_llamada = int(logs.data2)
                if logs.queuename in llamadas_cola.keys():
                    llamadas_cola[logs.queuename] += tiempo_llamada
                else:
                    llamadas_cola.update({logs.queuename: tiempo_llamada})
            for tiempo_cola in llamadas_cola:
                tiempo_agente = []
                tiempo_agente.append(agente)
                tiempo_agente.append(tiempo_cola)
                llamadas_cola[tiempo_cola] = str(datetime.timedelta(
                    0, llamadas_cola[tiempo_cola]))
                tiempo_agente.append(llamadas_cola[tiempo_cola])
                agentes_tiempo.append(tiempo_agente)

        return agentes_tiempo

    def calcular_tiempos_agentes(self, agentes, fecha_inferior, fecha_superior):
        eventos_pausa = ['PAUSEALL', 'UNPAUSEALL']
        agentes_tiempo = []

        for agente in agentes:
            agente_nuevo = None
            logs_time = Queuelog.objects.obtener_log_agente_pk_event_periodo_all(
                eventos_pausa, fecha_inferior, fecha_superior, agente.id)
            is_unpause = False
            time_actual = None
            for logs in logs_time:
                if is_unpause and logs.event == 'PAUSEALL':
                    resta = time_actual - logs.time
                    agente_en_lista = filter(lambda x: x.agente == agente,
                                             agentes_tiempo)
                    if agente_en_lista:
                        agente_nuevo = agente_en_lista[0]
                        if agente_nuevo.tiempo_pausa:
                            agente_nuevo._tiempo_pausa += resta
                        else:
                            agente_nuevo._tiempo_pausa = resta
                    else:
                        agente_nuevo = AgenteTiemposReporte(
                            agente, None, resta, None, 0, 0, None, None)
                        agentes_tiempo.append(agente_nuevo)
                    agente_nuevo = None
                    is_unpause = False
                    time_actual = None
                if logs.event == 'UNPAUSEALL':
                    time_actual = logs.time
                    is_unpause = True

        eventos_sesion = ['ADDMEMBER', 'REMOVEMEMBER']

        for agente in agentes:
            agente_nuevo = None
            logs_time = Queuelog.objects.obtener_log_agente_pk_event_periodo_all(
                eventos_sesion, fecha_inferior, fecha_superior, agente.id)
            is_remove = False
            time_actual = None
            for logs in logs_time:
                if is_remove and logs.event == 'ADDMEMBER':
                    resta = time_actual - logs.time
                    agente_en_lista = filter(lambda x: x.agente == agente,
                                             agentes_tiempo)
                    if agente_en_lista:
                        agente_nuevo = agente_en_lista[0]
                        if agente_nuevo.tiempo_sesion:
                            agente_nuevo._tiempo_sesion += resta
                        else:
                            agente_nuevo._tiempo_sesion = resta
                    else:
                        agente_nuevo = AgenteTiemposReporte(
                            agente, resta, None, None, 0, 0, None, None)
                        agentes_tiempo.append(agente_nuevo)
                    agente_nuevo = None
                    is_remove = False
                    time_actual = None
                if logs.event == 'REMOVEMEMBER':
                    time_actual = logs.time
                    is_remove = True

        eventos_llamadas = ['COMPLETECALLER', 'COMPLETEAGENT']

        for agente in agentes:
            agente_nuevo = None
            logs_time = Queuelog.objects.obtener_log_agente_pk_event_periodo(
                eventos_llamadas, fecha_inferior, fecha_superior, agente.id)
            lista_tiempo_llamada = [int(log.data2) for log in logs_time]
            agente_en_lista = filter(lambda x: x.agente == agente,
                                     agentes_tiempo)
            if agente_en_lista:
                agente_nuevo = agente_en_lista[0]
                agente_nuevo._tiempo_llamada = sum(lista_tiempo_llamada)
            else:
                agente_nuevo = AgenteTiemposReporte(
                    agente, None, None, sum(lista_tiempo_llamada), 0, 0, None, None)
                agentes_tiempo.append(agente_nuevo)

        eventos_llamadas_perdidas = ['RINGNOANSWER']

        for agente in agentes:
            agente_nuevo = None
            logs_time = Queuelog.objects.obtener_log_agente_pk_event_periodo(
                eventos_llamadas, fecha_inferior, fecha_superior, agente.id)
            logs_time_perdidas = Queuelog.objects.obtener_log_agente_pk_event_periodo(
                eventos_llamadas_perdidas, fecha_inferior, fecha_superior, agente.id)

            agente_en_lista = filter(lambda x: x.agente == agente,
                                     agentes_tiempo)
            if agente_en_lista:
                agente_nuevo = agente_en_lista[0]
                agente_nuevo._cantidad_llamadas_procesadas = logs_time.count()
                agente_nuevo._cantidad_llamadas_perdidas = logs_time_perdidas.count()
            else:
                agente_nuevo = AgenteTiemposReporte(
                    agente, None, None, None, logs_time.count(),
                    logs_time_perdidas.count(), None, None)
                agentes_tiempo.append(agente_nuevo)

        eventos_llamadas = ['COMPLETECALLER', 'COMPLETEAGENT']

        for agente in agentes:
            agente_nuevo = None
            logs_time = Queuelog.objects.obtener_log_agente_pk_event_periodo(
                eventos_llamadas, fecha_inferior, fecha_superior, agente.id)
            lista_tiempo_llamada = [int(log.data2) for log in logs_time]
            logs_saliente = logs_time.filter(data4='saliente')
            lista_tiempo_saliente = [int(log.data2) for log in logs_saliente]
            cantidad_llamadas = logs_time.count()
            cantidad_saliente = logs_saliente.count()
            cantidad_asignadas = cantidad_llamadas - cantidad_saliente
            tiempo_llamadas = sum(lista_tiempo_llamada)
            tiempo_saliente = sum(lista_tiempo_saliente)
            tiempo_asignadas = tiempo_llamadas - tiempo_saliente
            media_asignadas = 0
            if tiempo_asignadas > 0:
                media_asignadas = tiempo_asignadas / cantidad_asignadas
            media_salientes = 0
            if tiempo_saliente > 0:
                media_salientes = tiempo_saliente / cantidad_saliente
            agente_en_lista = filter(lambda x: x.agente == agente,
                                     agentes_tiempo)
            if agente_en_lista:
                agente_nuevo = agente_en_lista[0]

                agente_nuevo._media_asignada = media_asignadas
                agente_nuevo._media_saliente = media_salientes
            else:
                agente_nuevo = AgenteTiemposReporte(
                    agente, None, None, sum(lista_tiempo_llamada), 0, 0, media_asignadas,
                    media_salientes)
                agentes_tiempo.append(agente_nuevo)

        return agentes_tiempo

    def obtener_count_llamadas_campana(self, agentes, fecha_inferior, fecha_superior,
                                       user):
        eventos_llamadas = ['COMPLETECALLER', 'COMPLETEAGENT']

        campanas = Campana.objects.obtener_all_dialplan_asterisk()
        if not user.get_is_administrador():
            campanas = Campana.objects.obtener_campanas_vista_by_user(campanas, user)

        agentes_tiempo = []
        agentes = [agente.id for agente in agentes]
        logs_time = Queuelog.objects.obtener_agentes_campanas_total(
            eventos_llamadas, fecha_inferior, fecha_superior, agentes, campanas)

        for log in logs_time:
            campana = log[1].split('_')
            try:
                campana_nombre = campana[1]
            except ValueError:
                campana_nombre = log[1]
            agente = log[0].split('_')
            try:
                agente_nombre = agente[1]
            except ValueError:
                agente_nombre = log[0]
            tiempo_agente = []
            tiempo_agente.append(agente_nombre)
            tiempo_agente.append(campana_nombre)
            tiempo_agente.append(str(datetime.timedelta(0, log[2])))
            tiempo_agente.append(log[3])
            agentes_tiempo.append(tiempo_agente)

        return agentes_tiempo

    def _calcular_estadisticas(self, fecha_inferior, fecha_superior, agentes, user):
        if not agentes:
            agentes = self._obtener_agentes()
        #agentes_tiempo = self.calcular_tiempo_sesion(agentes, fecha_inferior,
         #                                            fecha_superior)
        agentes_pausa = self.calcular_tiempo_pausa(agentes, fecha_inferior,
                                                   fecha_superior)
        #agentes_llamadas = self.calcular_tiempo_llamada(agentes,
         #                                               fecha_inferior, fecha_superior)
        agentes_tiempos = self.calcular_tiempos_agentes(agentes, fecha_inferior,
                                                        fecha_superior)
        count_llamada_campana = self.obtener_count_llamadas_campana(
            agentes, fecha_inferior, fecha_superior, user)

        dic_estadisticas = {
            'agentes_tiempos': agentes_tiempos,
            'fecha_desde': fecha_inferior,
            'fecha_hasta': fecha_superior,
            'agentes_pausa': agentes_pausa,
            #'agentes_llamadas': agentes_llamadas,
            'count_llamada_campana': count_llamada_campana

        }
        return dic_estadisticas

    def general_campana(self, fecha_inferior, fecha_superior, agentes, user):
        estadisticas = self._calcular_estadisticas(fecha_inferior,
                                                   fecha_superior, agentes, user)

        if estadisticas:
            logger.info("Generando grafico calificaciones de campana por cliente ")

        return estadisticas

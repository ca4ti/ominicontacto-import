# -*- coding: utf-8 -*-

"""
Servicio para generar reporte de las grabaciones de las llamadas
"""

import pygal
import datetime

from collections import OrderedDict
from pygal.style import Style

from django.db.models import Q, Count

from ominicontacto_app.models import Grabacion, Queuelog, Campana
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


class GraficoService():

    def _obtener_total_llamdas_tipo(self, listado_grabaciones):
        """
        Obtiene el total de llamadas por tipo de origen de llamadas
        :param listado_grabaciones: listados de las grabaciones de las llamadas
        :return: dicionario con los totales por tipo de llamadas
        """
        counter_por_tipo = {
            Grabacion.TYPE_DIALER: 0,
            Grabacion.TYPE_ICS: 0,
            Grabacion.TYPE_INBOUND: 0,
            Grabacion.TYPE_MANUAL: 0,
        }

        tipos_llamadass = (Grabacion.TYPE_DIALER, Grabacion.TYPE_INBOUND,
                           Grabacion.TYPE_ICS, Grabacion.TYPE_MANUAL)

        for grabacion in listado_grabaciones:
            if grabacion.tipo_llamada in tipos_llamadass:
                counter_por_tipo[grabacion.tipo_llamada] += 1

        return counter_por_tipo

    def _obtener_campana_llamada(self, fecha_inferior, fecha_superior, campanas):
        """
        Obtiene el totales de llamadas por campanas
        :param fecha_inferior: fecha desde cual se obtendran las grabaciones
        :param fecha_superior: fecha hasta el cual se obtendran las grabaciones
        :return: queryset con las cantidades totales por campana
        """
        # lista de dict con la cantidad por  cada campana
        fecha_inferior = datetime.datetime.combine(fecha_inferior,
                                                   datetime.time.min)
        fecha_superior = datetime.datetime.combine(fecha_superior,
                                                   datetime.time.max)

        campanas_ids_nombres = OrderedDict()
        campanas_tipos = []

        for pk_nombre_tipo in campanas.values('pk', 'nombre', 'type').order_by('pk'):
            campanas_ids_nombres[pk_nombre_tipo['pk']] = pk_nombre_tipo['nombre']
            campana_tipo = Campana.TYPES_CAMPANA[pk_nombre_tipo['type'] - 1][1]
            campanas_tipos.append(campana_tipo)

        campanas_ids = campanas_ids_nombres.keys()

        dict_campana = Queuelog.objects.filter(
            event='ENTERQUEUE',
            time__range=(fecha_inferior, fecha_superior),
            campana_id__in=campanas_ids).values(
                'campana_id').annotate(cantidad=Count('campana_id')).order_by('campana_id')

        result = (dict_campana, campanas_ids, campanas_ids_nombres.values(), campanas_tipos)

        return result

    def _obtener_total_campana_llamadas(self, dict_campana, campanas):
        """
        Obtiene los totales de llamadas por campana a partir de una lista de campañas
        """

        total_campana = []
        for campana_id in campanas:
            count = 0
            try:
                count = dict_campana.get(campana_id=campana_id)['cantidad']
            except Queuelog.DoesNotExist:
                pass
            total_campana.append(count)
        return total_campana

    # def _obtener_total_llamadas_dialer(self, dict_campana, campanas_ids_tipos):
    #     """
    #     Obtiene el total de llamadas asociadas a campañas de DIALER por campaña en una lista
    #     :return: lista con el total de llamadas DIALER por campana
    #     """
    #     total_dialer = []

    #     for campana_id, campana_tipo in campanas_ids_tipos.items():
    #         if campana.

    #         total_dialer.append(cantidad)

    #     return total_dialer

    def _obtener_total_inbound_grabacion(self, dict_campana, campana):
        """
        Obtiene el total grabaciones INBOUND por campana en una lista
        :return: lista con el total de llamadas INBOUND por campana
        """
        total_inbound = []
        for campana_id in campana:
            cantidad = 0
            result = dict_campana.filter(tipo_llamada=Grabacion.TYPE_INBOUND).\
                filter(campana=campana_id)
            if result:
                cantidad = result[0]['cantidad']

            total_inbound.append(cantidad)
        return total_inbound

    def _obtener_total_manual_grabacion(self, dict_campana, campana):
        """
        Obtiene el total grabaciones MANUAL por campana en una lista
        :return: lista con el total de llamadas MANUAL por campana
        """
        total_manual = []

        for campana_id in campana:
            cantidad = 0
            result = dict_campana.filter(tipo_llamada=Grabacion.TYPE_MANUAL).\
                filter(campana=campana_id)
            if result:
                cantidad = result[0]['cantidad']

            total_manual.append(cantidad)

        return total_manual

    def _obtener_total_llamadas_campana_inbound(self, fecha_inferior,
                                                fecha_superior):
        # lista de dict con la cantidad de cada campana
        dict_campana = Grabacion.objects.obtener_count_campana().filter(
            fecha__range=(fecha_inferior, fecha_superior)).filter(
            tipo_llamada=3)
        list_campana = []
        list_cantidad = []
        for campana_counter in dict_campana:
            list_campana.append(campana_counter['campana__nombre'])
            list_cantidad.append(campana_counter['cantidad'])
        return list_campana, list_cantidad

    def _obtener_total_llamadas_agente_inbound(self, fecha_inferior, fecha_superior):
        # lista de dict con la cantidad de cada agente
        dict_agentes = Grabacion.objects.obtener_count_agente().filter(
            fecha__range=(fecha_inferior, fecha_superior)).filter(
            tipo_llamada=3)
        list_agente = []
        list_cantidad = []
        for agente_counter in dict_agentes:
            list_agente.append(agente_counter['sip_agente'])
            list_cantidad.append(agente_counter['cantidad'])
        return list_agente, list_cantidad

    def calcular_cantidad_llamadas(self, campanas, fecha_inferior, fecha_superior):
        """
        Calcula la cantidad de llamadas ingresadas, atendidas, abandondas, expiradas
        por campana
        :return: en un dicionaros los totales por campana y los totales para hacer el
        grafico
        """
        eventos_llamadas_ingresadas = ['ENTERQUEUE']
        eventos_llamadas_atendidas = ['CONNECT']
        eventos_llamadas_abandonadas = ['ABANDON']
        eventos_llamadas_expiradas = ['EXITWITHTIMEOUT']

        nombres_queues = []
        total_atendidas = []
        total_abandonadas = []
        total_expiradas = []

        queues_tiempo = []

        for campana in campanas:
            ingresadas = Queuelog.objects.obtener_log_campana_id_event_periodo(
                eventos_llamadas_ingresadas, fecha_inferior, fecha_superior,
                campana.id)
            atendidas = Queuelog.objects.obtener_log_campana_id_event_periodo(
                eventos_llamadas_atendidas, fecha_inferior, fecha_superior,
                campana.id)
            abandonadas = Queuelog.objects.obtener_log_campana_id_event_periodo(
                eventos_llamadas_abandonadas, fecha_inferior, fecha_superior,
                campana.id)
            expiradas = Queuelog.objects.obtener_log_campana_id_event_periodo(
                eventos_llamadas_expiradas, fecha_inferior, fecha_superior,
                campana.id)
            count_llamadas_ingresadas = ingresadas.count()
            count_llamadas_atendidas = atendidas.count()
            count_llamadas_abandonadas = abandonadas.count()
            count_llamadas_expiradas = expiradas.count()
            count_llamadas_manuales = ingresadas.filter(data4='saliente').count()
            count_manuales_atendidas = atendidas.filter(data4='saliente').count()
            count_manuales_abandonadas = abandonadas.filter(data4='saliente').count()
            cantidad_campana = []
            cantidad_campana.append(campana.nombre)
            cantidad_campana.append(count_llamadas_ingresadas)
            cantidad_campana.append(count_llamadas_atendidas)
            cantidad_campana.append(count_llamadas_expiradas)
            cantidad_campana.append(count_llamadas_abandonadas)
            cantidad_campana.append(count_llamadas_manuales)
            cantidad_campana.append(count_manuales_atendidas)
            cantidad_campana.append(count_manuales_abandonadas)

            queues_tiempo.append(cantidad_campana)

            # para reportes
            nombres_queues.append(campana.nombre)
            total_atendidas.append(count_llamadas_atendidas)
            total_abandonadas.append(count_llamadas_expiradas)
            total_expiradas.append(count_llamadas_abandonadas)

        totales_grafico = {
            'nombres_queues': nombres_queues,
            'total_atendidas': total_atendidas,
            'total_abandonadas': total_abandonadas,
            'total_expiradas': total_expiradas
        }

        return queues_tiempo, totales_grafico

    def obtener_total_llamadas(self, fecha_inferior, fecha_superior, campanas):
        """
        Calcula la cantidad de llamadas ingresadas, atendidas, abandondas, expiradas
        :return: los totales de llamadas por ingresadas, atendidas, abandonad y expiradas
        """

        eventos_llamadas_ingresadas = ['ENTERQUEUE']
        eventos_llamadas_atendidas = ['CONNECT']
        eventos_llamadas_abandonadas = ['ABANDON']
        eventos_llamadas_expiradas = ['EXITWITHTIMEOUT']
        campanas_entrantes = campanas.filter(
            type=Campana.TYPE_ENTRANTE).values_list('id', flat=True)
        campanas_dialer = campanas.filter(
            type=Campana.TYPE_DIALER).values_list('id', flat=True)

        ingresadas_dialer = Queuelog.objects.obtener_log_event_periodo(
            eventos_llamadas_ingresadas, fecha_inferior, fecha_superior).filter(
                Q(campana_id__in=campanas_dialer), ~Q(data4='saliente'))
        atendidas_dialer = Queuelog.objects.obtener_log_event_periodo(
            eventos_llamadas_atendidas, fecha_inferior, fecha_superior).filter(
                Q(campana_id__in=campanas_dialer), ~Q(data4='saliente'))
        abandonadas_dialer = Queuelog.objects.obtener_log_event_periodo(
            eventos_llamadas_abandonadas, fecha_inferior, fecha_superior).filter(
                Q(campana_id__in=campanas_dialer), ~Q(data4='saliente'))
        expiradas_dialer = Queuelog.objects.obtener_log_event_periodo(
            eventos_llamadas_expiradas, fecha_inferior, fecha_superior).filter(
                campana_id__in=campanas_dialer)

        ingresadas_entrantes = Queuelog.objects.obtener_log_event_periodo(
            eventos_llamadas_ingresadas, fecha_inferior, fecha_superior).filter(
                Q(campana_id__in=campanas_entrantes), ~Q(data4='saliente'))
        atendidas_entrantes = Queuelog.objects.obtener_log_event_periodo(
            eventos_llamadas_atendidas, fecha_inferior, fecha_superior).filter(
                Q(campana_id__in=campanas_entrantes), ~Q(data4='saliente'))
        abandonadas_entrantes = Queuelog.objects.obtener_log_event_periodo(
            eventos_llamadas_abandonadas, fecha_inferior, fecha_superior).filter(
                Q(campana_id__in=campanas_entrantes), ~Q(data4='saliente'))
        expiradas_entrantes = Queuelog.objects.obtener_log_event_periodo(
            eventos_llamadas_expiradas, fecha_inferior, fecha_superior).filter(
                Q(campana_id__in=campanas_entrantes), ~Q(data4='saliente'))

        llamadas_ingresadas_manuales = Queuelog.objects.obtener_log_event_periodo(
            eventos_llamadas_ingresadas, fecha_inferior, fecha_superior).filter(
            campana_id__in=campanas, data4='saliente')
        llamadas_atendidas_manuales = Queuelog.objects.obtener_log_event_periodo(
            eventos_llamadas_atendidas, fecha_inferior, fecha_superior).filter(
            campana_id__in=campanas, data4='saliente')
        llamadas_abandonadas_manuales = Queuelog.objects.obtener_log_event_periodo(
            eventos_llamadas_abandonadas, fecha_inferior, fecha_superior).filter(
            campana_id__in=campanas, data4='saliente')

        count_llamadas_ingresadas_dialer = ingresadas_dialer.count()
        count_llamadas_gestionadas_dialer = atendidas_dialer.count()
        count_llamadas_abandonadas_dialer = abandonadas_dialer.count()
        count_llamadas_expiradas_dialer = expiradas_dialer.count()
        count_llamadas_perdidas_dialer = count_llamadas_abandonadas_dialer + \
            count_llamadas_expiradas_dialer

        count_llamadas_ingresadas_entrantes = ingresadas_entrantes.count()
        count_llamadas_atendidas_entrantes = atendidas_entrantes.count()
        count_llamadas_abandonadas_entrantes = abandonadas_entrantes.count()
        count_llamadas_expiradas_entrantes = expiradas_entrantes.count()

        count_llamadas_ingresadas_manuales = llamadas_ingresadas_manuales.count()
        count_llamadas_atendidas_manuales = llamadas_atendidas_manuales.count()
        count_llamadas_abandonadas_manuales = llamadas_abandonadas_manuales.count()

        total_llamadas_ingresadas = count_llamadas_ingresadas_entrantes + \
            count_llamadas_ingresadas_dialer + \
            count_llamadas_ingresadas_manuales

        cantidad_campana = OrderedDict()
        cantidad_campana['total_llamadas_ingresadas'] = total_llamadas_ingresadas

        cantidad_campana['llamadas_ingresadas_dialer'] = count_llamadas_ingresadas_dialer
        cantidad_campana['llamadas_gestionadas_dialer'] = count_llamadas_gestionadas_dialer
        cantidad_campana['llamadas_perdidas_dialer'] = count_llamadas_perdidas_dialer

        cantidad_campana['llamadas_ingresadas_entrantes'] = count_llamadas_ingresadas_entrantes
        cantidad_campana['llamadas_atendidas_entrantes'] = count_llamadas_atendidas_entrantes
        cantidad_campana['llamadas_expiradas_entrantes'] = count_llamadas_expiradas_entrantes
        cantidad_campana['llamadas_abandonadas_entrantes'] = count_llamadas_abandonadas_entrantes

        cantidad_campana['llamadas_ingresadas_manuales'] = count_llamadas_ingresadas_manuales
        cantidad_campana['llamadas_atendidas_manuales'] = count_llamadas_atendidas_manuales
        cantidad_campana['llamadas_abandonadas_manuales'] = count_llamadas_abandonadas_manuales

        return cantidad_campana

    def _calcular_estadisticas(self, fecha_inferior, fecha_superior, user, finalizadas):

        if finalizadas:
            campanas = Campana.objects.obtener_all_activas_finalizadas()
        else:
            campanas = Campana.objects.obtener_all_dialplan_asterisk()

        if not user.get_is_administrador():
            campanas = Campana.objects.obtener_campanas_vista_by_user(campanas, user)

        # obtiene el total de llamadas por tipo de llamadas
        total_llamadas_dict = self.obtener_total_llamadas(fecha_inferior, fecha_superior,
                                                          campanas)
        total_llamadas_ingresadas = total_llamadas_dict['total_llamadas_ingresadas']

        # calculo el porcentaje de las llamadas por tipo de llamadas
        porcentaje_dialer = 0.0
        porcentaje_entrantes = 0.0
        porcentaje_manual = 0.0
        total_dialer = total_llamadas_dict['llamadas_ingresadas_dialer']
        total_entrantes = total_llamadas_dict['llamadas_ingresadas_entrantes']
        total_manual = total_llamadas_dict['llamadas_ingresadas_manuales']
        if total_llamadas_ingresadas > 0:
            porcentaje_dialer = (100.0 * float(total_dialer) /
                                 float(total_llamadas_ingresadas))
            porcentaje_entrantes = (100.0 * float(total_entrantes) /
                                    float(total_llamadas_ingresadas))
            porcentaje_manual = (100.0 * float(total_manual) /
                                 float(total_llamadas_ingresadas))

        queues_llamadas, totales_grafico = self.calcular_cantidad_llamadas(
            campanas, fecha_inferior, fecha_superior)

        total_llamadas = total_llamadas_dict.values()

        # ----
        dict_campana, campanas, campanas_nombre, tipos_campana = self._obtener_campana_llamada(
            fecha_inferior, fecha_superior, campanas)
        total_campana = self._obtener_total_campana_llamadas(dict_campana, campanas)

        # total_grabacion_dialer = self._obtener_total_llamadas_dialer(
        #     dict_campana, campanas)
        # total_grabacion_entrantes = self._obtener_total_llamadas_entrantes(
        #     dict_campana, campanas)
        # total_grabacion_manual = self._obtener_total_llamdas_manuales(
        #     dict_campana, campanas)
        # -----

        dic_estadisticas = {
            'porcentaje_dialer': porcentaje_dialer,
            'porcentaje_entrantes': porcentaje_entrantes,
            'porcentaje_manual': porcentaje_manual,
            'total_grabaciones': total_llamadas_ingresadas,
            'total_dialer': total_dialer,
            'total_inbound': total_entrantes,
            'total_manual': total_manual,
            'campana_nombre': campanas_nombre,
            'campana': campanas,
            'total_campana': total_campana,
            'tipos_campana': tipos_campana,
            # 'total_grabacion_dialer': total_grabacion_dialer,
            # 'total_grabacion_entrantes': total_grabacion_entrantes,
            # 'total_grabacion_manual': total_grabacion_manual,
            'queues_llamadas': queues_llamadas,
            'fecha_desde': fecha_inferior,
            'fecha_hasta': fecha_superior,
            'total_llamadas': total_llamadas,
            'total_llamadas_dict': total_llamadas_dict,
            'totales_grafico': totales_grafico,
        }
        return dic_estadisticas

    def general_llamadas_hoy(self, fecha_inferior, fecha_superior, user, finalizadas):
        estadisticas = self._calcular_estadisticas(
            fecha_inferior, fecha_superior, user, finalizadas)

        if estadisticas:
            logger.info("Generando grafico para grabaciones de llamadas ")

        no_data_text = "No hay llamadas para ese periodo"
        torta_grabaciones = pygal.Pie(  # @UndefinedVariable
            style=ESTILO_AZUL_ROJO_AMARILLO,
            no_data_text=no_data_text,
            no_data_font_size=32,
            legend_font_size=25,
            truncate_legend=10,
            tooltip_font_size=50,
        )

        # Barras: muestran la desagregación de todas las llamadas por campañas
        barras_llamadas_campanas = pygal.Bar(  # @UndefinedVariable
            show_legend=True,
            style=ESTILO_AZUL_ROJO_AMARILLO)

        barras_llamadas_campanas.x_labels = ["Dialer", "Entrantes", "Manuales"]
        barras_llamadas_campanas.add(
            'Ingresadas', [estadisticas['total_llamadas_dict']['llamadas_ingresadas_dialer'],
                           estadisticas['total_llamadas_dict']['llamadas_ingresadas_entrantes'],
                           estadisticas['total_llamadas_dict']['llamadas_ingresadas_manuales']])
        barras_llamadas_campanas.add(
            'Atendidas', [estadisticas['total_llamadas_dict']['llamadas_gestionadas_dialer'],
                          estadisticas['total_llamadas_dict']['llamadas_atendidas_entrantes'],
                          estadisticas['total_llamadas_dict']['llamadas_atendidas_manuales']])
        perdidas_entrantes = estadisticas['total_llamadas_dict']['llamadas_expiradas_entrantes'] + \
            estadisticas['total_llamadas_dict']['llamadas_abandonadas_entrantes']
        barras_llamadas_campanas.add(
            'Perdidas',
            [estadisticas['total_llamadas_dict']['llamadas_perdidas_dialer'],
             perdidas_entrantes,
             estadisticas['total_llamadas_dict']['llamadas_abandonadas_manuales']])

        # torta_grabaciones.title = "Resultado de las llamadas"
        torta_grabaciones.add('Dialer', estadisticas['porcentaje_dialer'])
        torta_grabaciones.add('Entrantes', estadisticas['porcentaje_entrantes'])
        torta_grabaciones.add('Manual', estadisticas['porcentaje_manual'])

        # # Barra: Cantidad de llamadas de las campana por tipo de llamadas
        # barra_campana_total = pygal.Bar(  # @UndefinedVariable
        #     show_legend=False,
        #     style=ESTILO_AZUL_ROJO_AMARILLO)
        # barra_campana_total.title = 'Cantidad de llamadas de las campana por tipo de llamadas'

        # barra_campana_total.x_labels = estadisticas['campana_nombre']
        # barra_campana_total.add('ICS',
        #                         estadisticas['total_grabacion_ics'])
        # barra_campana_total.add('DIALER',
        #                         estadisticas['total_grabacion_dialer'])
        # barra_campana_total.add('INBOUND',
        #                         estadisticas['total_grabacion_inbound'])
        # barra_campana_total.add('MANUAL',
        #                         estadisticas['total_grabacion_manual'])

        # # Barra: Cantidad de llamadas por campana
        # barra_campana_llamadas = pygal.Bar(  # @UndefinedVariable
        #     show_legend=False,
        #     style=ESTILO_AZUL_ROJO_AMARILLO)
        # # barra_campana_llamadas.title = 'Distribucion por campana'

        # barra_campana_llamadas.x_labels = \
        #     estadisticas['totales_grafico']['nombres_queues']
        # barra_campana_llamadas.add('atendidas',
        #                            estadisticas['totales_grafico']['total_atendidas'])
        # barra_campana_llamadas.add('abandonadas ',
        #                            estadisticas['totales_grafico']['total_abandonadas'])
        # barra_campana_llamadas.add('expiradas',
        #                            estadisticas['totales_grafico']['total_expiradas'])

        return {
            'estadisticas': estadisticas,
            'barras_llamadas_campanas': barras_llamadas_campanas,
            'torta_grabaciones': torta_grabaciones,
            'dict_campana_counter': zip(estadisticas['campana_nombre'],
                                        estadisticas['total_campana'],
                                        estadisticas['tipos_campana']),
            # 'barra_campana_total': barra_campana_total,
            # 'barra_campana_llamadas': barra_campana_llamadas,
        }

# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import psycopg2


class KamailioService():

    def _conectar_base_datos(self):
        connection = psycopg2.connect(database='kamailio', user='kamailio',
                                      password='kamailiorw', host='127.0.0.1',
                                      port='5432')
        cursor = connection.cursor()
        return connection, cursor

    def crear_agente_kamailio(self, agente):
        """
        crear usuario
        """
        connection, cursor = self._conectar_base_datos()

        try:
            sql = """INSERT INTO sip (id, name, secret, directmedia, context,
                  callerid, kamailiopass, deny, permit,accountcode) values
                  (%(id)s, %(name)s, '', 'no', 'from-internal', %(callerid)s,
                  %(kamailiopass)s, '0.0.0.0/0.0.0.0', '172.16.20.219/255.255.255.255',
                  %(accountcode)s)"""
            params = {
                'id': agente.id,
                'name': agente.sip_extension,
                'callerid': agente.user.get_full_name(),
                'kamailiopass': agente.sip_password,
                'accountcode': agente.grupo.nombre
            }
            cursor.execute(sql, params)
            connection.commit()
            connection.close()
        except psycopg2.DatabaseError, e:
            print "error base de datos"
            print e
            connection.close()

    def update_agente_kamailio(self, agente):
        """
        crear usuario
        """
        connection, cursor = self._conectar_base_datos()

        try:
            sql = """UPDATE sip SET name=%(name)s, callerid=%(callerid)s,
                  kamailiopass=%(kamailiopass)s, accountcode=%(accountcode)s
                  WHERE id=%(id)s"""
            params = {
                'id': agente.id,
                'name': agente.sip_extension,
                'callerid': agente.user.get_full_name(),
                'kamailiopass': agente.sip_password,
                'accountcode': agente.grupo.nombre
            }
            cursor.execute(sql, params)
            connection.commit()
            connection.close()
        except psycopg2.DatabaseError, e:
            print "error base de datos"
            print e
            connection.close()

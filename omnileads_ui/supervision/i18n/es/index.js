export default {
    option: 'Opción | Opciones',
    name: 'Nombre',
    agent: 'Agente | Agentes',
    campaign: 'Campaña | Campañas',
    group: 'Grupo | Grupos',
    campaign_info: 'Campaña: {name}',
    penalty: 'Multa',
    agents_campaign: 'Agentes de campaña',
    clean_object: 'Limpiar {object}',
    find_by: 'Busca por {field}...',
    select_a: 'Selecciona un {field} | Selecciona una {field}',
    agent_campaign: {
        name: 'Nombre',
        username: 'Nombre de usuario',
        sip: 'ID SIP',
        penalty: 'Multa'
    },
    sweet_alert: {
        title: {
            success: '¡Operación exitosa!',
            error: '¡Operación erronea!',
            warning: '¡Advertencia!',
        },
        icons: {
            success: 'success',
            error: 'error',
            warning: 'warning',
            info: 'info',
        }
    },
    actions: {
        new: 'Nuevo',
        add: 'Agregar',
        delete: 'Borrar',
        create: 'Crear',
        clean: 'Limpiar',
        edit: 'Editar',
        update: 'Actualizar',
        show: 'Ver | Mostrar',
        save: 'Guardar',
        find: 'Busca | Buscar'
    },
    pages: {
        dashboard_home_page: {
            active_campaign_by_type: 'Campañas {type} Activas',
            campaigns: {
                inbound: 'Entrantes',
                dialer: 'Dialer',
                manual: 'Manuales',
                preview: 'Preview'
            },
            agent_status: 'Estado de agentes',
            call_sumary: 'Resumen de llamadas'
        },
        add_agents_to_campaign: {
            delete_agent: 'Elimina al agente',
            empty_agents: 'No se encontraron agentes',
            load_info: 'Cargando la información',
            already_agent_in_campaign: 'El agente ya está en la campaña',
            already_agents_in_campaign: 'Los siguientes agentes ya estaban en la campaña: ( {agents} ), por lo tanto no se agregaron',
            not_select_type: 'No seleccionaste un {type}',
            select_type: 'Selecciona {type}',
            how_to_edit_penalty: 'Para modificar el penalty selecciona la columna',
            group_added_success: 'El grupo se agrego exitosamente',
            agent_added_success: 'El agente se agrego exitosamente',
            agents_added_success: 'Los agentes se actualizaron exitosamente',
            agents_added_error: 'Error al actualizar los agentes',
            agent_deleted_success: 'Agente eliminado exitosamente',
        }
    }
}

export default {
    agent: 'Agent | Agents',
    campaign: 'Campaign | Campaigns',
    group: 'Group | Groups',
    campaign_info: 'Campaign: {name}',
    penalty: 'Penalty',
    agents_campaign: 'Campaign agents',
    clean_object: 'Clean {object}',
    find_by: 'Find by {field}...',
    select_a: 'Select a {field} | Select one {field}',
    agent_campaign: {
        name: 'Name',
        username: 'Username',
        sip: 'ID SIP',
        penalty: 'Penalty'
    },
    sweet_alert: {
        title: {
            success: 'Successful!',
            error: 'Error!',
            warning: 'Warning!',
        }
    },
    actions: {
        new: 'New',
        add: 'Add',
        delete: 'Delete',
        create: 'Create',
        clean: 'Clean',
        edit: 'Edit',
        update: 'Update',
        show: 'Show',
        save: 'Save',
        find: 'Find'
    },
    pages: {
        dashboard_home_page: {
            active_campaign_by_type: 'Active {type} Campaigns',
            campaigns: {
                inbound: 'Inbound',
                dialer: 'Dialer',
                manual: 'Manual',
                preview: 'Preview'
            },
            agent_status: 'Agent Status',
            call_sumary: 'Call Sumary'
        },
        add_agents_to_campaign: {
            delete_agent: 'Remove the agent',
            empty_agents: 'No agents found',
            load_info: 'Loading the information',
            already_agent_in_campaign: 'The agent is already in the campaign',
            already_agents_in_campaign: 'The following agents were already in the campaign: ( {agents} ), therefore not added',
            not_select_type: 'You did not select a {type}',
            select_type: 'Choose {type}',
            how_to_edit_penalty: 'To modify the penalty select the column',
        }
    }
}

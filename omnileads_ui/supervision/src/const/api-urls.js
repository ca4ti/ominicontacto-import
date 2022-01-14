const apiUrls = {
    'DashboardSupervision': '/api/v1/dashboard_supervision',
    'CampaignAgents': (id_campaign) => `/api/v1/campaign/${id_campaign}/agents`,
    'ActiveAgents': '/api/v1/active_agents',
    'ActiveAgentsByGroup': '/api/v1/active_agents_by_group',
    'UpdateAgentsCampaign': '/api/v1/campaign/agents_update',
}
export default apiUrls;

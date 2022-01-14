import { createStore } from 'vuex'
import AgentsCampaignService from '../services/agentsCampaignService.js'
const agentsCampaignService = new AgentsCampaignService();

export default createStore({
  state: {
    agents_by_campaign: [],
    active_agents: [],
    groups: []
  },
  mutations: {
    addAgentToCampaign (state, new_agent) {
      state.agents_by_campaign.push(new_agent)
    },
    initAgentsCampaign(state, agents){
      state.agents_by_campaign = agents
    },
    initActiveAgents(state, active_agents){
      state.active_agents = active_agents
    },
    initGroups(state, groups){
      state.groups = groups
    },
    removeAgentOfCampaign(state, agent_id){
      state.agents_by_campaign = state.agents_by_campaign.filter(e => e['agent_id'] != agent_id)
    },
    updateAgentsCampaign(state){
      console.log(state.agents_by_campaign)
    },
    updateAgentPenalty(state, payload){
      state.agents_by_campaign.filter((agent) => {
        if(agent['agent_id'] == payload['agent_id']){
          agent['agent_penalty'] = payload['penalty']
        }
      })
    },
  },
  actions: {
    addAgentToCampaign ({ commit }, new_agent) {
      commit('addAgentToCampaign', new_agent)
    },
    removeAgentOfCampaign ({ commit }, agent_id) {
      commit('removeAgentOfCampaign', agent_id)
    },
    async initAgentsCampaign ({ commit }, campaign_id) {
      const {agents_campaign} = await agentsCampaignService.getAgentsByCampaign(campaign_id)
      commit('initAgentsCampaign', agents_campaign)
    },
    async initActiveAgents ({ commit }) {
      const {active_agents} = await agentsCampaignService.getActiveAgents()
      commit('initActiveAgents', active_agents)
    },
    async initGroups ({ commit }) {
      const {groups} = await agentsCampaignService.getActiveAgentsByGroup()
      commit('initGroups', groups)
    },
    async updateAgentsCampaign({ commit }, campaign_id){
      let agents = this.state.agents_by_campaign.map((agent)=>{
        return {
          agent_id: agent['agent_id'],
          agent_penalty: agent['agent_penalty']
        }
      })
      let update_resp = await agentsCampaignService.updateAgentsByCampaign({
        campaign_id,
        agents
      })
      console.log(update_resp)
      const {agents_campaign} = await agentsCampaignService.getAgentsByCampaign(campaign_id)
      commit('initAgentsCampaign', agents_campaign)
    },
    updateAgentPenalty ({ commit }, payload) {
      commit('updateAgentPenalty', payload)
    },
  },
  modules: {
  }
});

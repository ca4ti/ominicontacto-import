import apiUrls from './../const/api-urls'
import { HTTP, BaseService } from './apiBaseService'

export default class AgentsCampaignService extends BaseService {
    constructor() {
        super()
    }

    async getAgentsByCampaign(id_campaign) {
        try {
            let resp = await fetch(apiUrls.CampaignAgents(id_campaign), this.payload)
            let agents_by_campaign = await resp.json()
            return agents_by_campaign
        } catch (error) {
            console.error("No se pudieron obtener los agentes por campaña")
            return []
        }
    }

    async getActiveAgents() {
        try {
            let resp = await fetch(apiUrls.ActiveAgents, this.payload)
            let agents = await resp.json()
            return agents
        } catch (error) {
            console.error("No se pudieron obtener los agentes activos")
            return []
        }
    }

    async getActiveAgentsByGroup() {
        try {
            let resp = await fetch(apiUrls.ActiveAgentsByGroup, this.payload)
            let agents_by_group = await resp.json()
            return agents_by_group
        } catch (error) {
            console.error("No se pudieron obtener los agentes activos por grupo")
            return []
        }
    }

    async updateAgentsByCampaign(data) {
        try {
            this.setPayload(HTTP.POST, JSON.stringify(data))
            const resp = await fetch(
                apiUrls.UpdateAgentsCampaign,
                this.payload
            )
            this.initPayload()
            return resp
        } catch (error) {
            console.error("No se pudieron actualizar los agentes de la campaña")
            console.error(error)
            return {}
        }
    }
}
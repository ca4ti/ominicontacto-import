import Cookies from 'universal-cookie'
import apiUrls from './../const/api-urls'

const HTTP = {
    'POST': 'POST',
    'GET': 'GET',
    'PUT': 'PUT',
    'DELETE': "DELETE"
}

export default class AgentsCampaignService {
    constructor(){
        this.cookies = new Cookies()
        this.headers = {
            'X-CSRFToken': this.cookies.get('csrftoken'),
            'Content-Type': 'application/json'
        }
        this.initPayload()
    }

    setPayload(method=HTTP.POST, body=null){
        if(body){
            this.payload.body = body
        }
        this.payload.method = method
    }

    initPayload(){
        this.payload = {
            method: HTTP.GET,
            credentials: 'same-origin',
            headers: this.headers
        }
    }

    async getAgentsByCampaign(id_campaign){
        try {
            let resp = await fetch(apiUrls.CampaignAgents(id_campaign), this.payload)
            let agents = await resp.json()
            return agents
        } catch (error) {
            console.error("No se pudo hacer la peticion al API")
            return []
        }
    }

    async getActiveAgents(){
        try {
            let resp = await fetch(apiUrls.ActiveAgents, this.payload)
            let agents = await resp.json()
            return agents
        } catch (error) {
            console.error("No se pudo hacer la peticion al API")
            return []
        }
    }

    async getActiveAgentsByGroup(){
        try {
            let resp = await fetch(apiUrls.ActiveAgentsByGroup, this.payload)
            let agents = await resp.json()
            return agents
        } catch (error) {
            console.error("No se pudo hacer la peticion al API")
            return []
        }
    }

    async updateAgentsByCampaign(data){
        try {
            // const formData = new FormData();
            // formData.append('campaign_id', data['campaign_id'])
            // formData.append('agents', data['agents'])
            // this.setPayload(HTTP.POST, formData)
            this.setPayload(HTTP.POST, JSON.stringify(data))
            console.log(this.payload)
            const resp = await fetch(
                apiUrls.UpdateAgentsCampaign,
                this.payload
            )
            console.log(resp)
            this.initPayload()
            // return await resp.json()
            return {}
        } catch (error) {
            console.error("No se pudo hacer la peticion al API")
            console.error(error)
            return []
        }
    }
}
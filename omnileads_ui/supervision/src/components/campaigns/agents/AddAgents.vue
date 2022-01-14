<template>
  <div>
    <div class="p-field p-col-12 p-md-8">
        <Dropdown 
        v-model="selectedAgent"
        :options="agents"
        optionLabel="agent"
        placeholder="Selecciona un agente"
        :filter="true"
        filterPlaceholder="Busca"/>
    </div>
    <div class="p-field p-col-12 p-md-3">
      <Button type="button" label="Agregar" class="p-button-outlined" @click="addAgent"/>
    </div>
  </div>
</template>

<script>
import { mapActions, mapState } from 'vuex'
import AgentsCampaignService from '@/services/agentsCampaignService.js'

export default {
  data() {
    return {
      selectedAgent: null,
      active_agents: [],
      agents: []
    }
  },
  created() {
    this.agentsCampaignService = new AgentsCampaignService()
  },
  methods: {
    addAgent() {
      if(this.selectedAgent){
        var agent_id = this.selectedAgent['value']
        if(this.agents_by_campaign.find((agent) => agent_id == agent['agent_id'])){
          this.$swal({
            title: '¡Operacion erronea!',
            text: 'El agente ya está en la campaña',
            icon: 'warning',
            timer: 2000,
            showConfirmButton: false
          })
        }else{
          var agent = this.active_agents.find((agent) => agent_id == agent['agent_id'])
          this.addAgentToCampaign(agent)
          this.selectedAgent = null
          this.$swal({
            title: '¡Operacion exitosa!',
            text: 'Se agrego el agente exitosamente',
            icon: 'success',
            timer: 2000,
            showConfirmButton: false
          })
        }
      }else{
        this.$swal({
          title: '¡Operacion erronea!',
          text: 'No seleccionaste un agente',
          icon: 'warning',
          timer: 2000,
          showConfirmButton: false
        })
      }
    },
    ...mapActions(['addAgentToCampaign'])
  },
  async mounted() {
    const {active_agents} = await this.agentsCampaignService.getActiveAgents()
    this.active_agents = await active_agents
    this.agents = await this.active_agents.map((agent) => {
      return {
        'agent': agent['agent_full_name'],
        'value': agent['agent_id']
      }
    })
  },
  computed: {
    ...mapState(['agents_by_campaign'])
  }
};
</script>

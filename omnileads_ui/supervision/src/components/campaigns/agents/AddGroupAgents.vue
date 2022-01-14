<template>
  <div>
    <div class="p-field p-col-12 p-md-8">
        <Dropdown
        v-model="selectedGroup"
        :options="groupsSelectize"
        optionLabel="group"
        placeholder="Selecciona un grupo"
        :filter="true"
        filterPlaceholder="Busca"/>
    </div>
    <div class="p-field p-col-12 p-md-3">
      <Button type="button" label="Agregar" class="p-button-outlined" @click="addGroup"/>
    </div>
  </div>
</template>

<script>
import { mapActions, mapState } from 'vuex'
import AgentsCampaignService from '@/services/agentsCampaignService.js'

export default {
  data() {
    return {
      groupsSelectize: [],
      selectedGroup: null,
      groups: []
    }
  },
  created() {
    this.agentsCampaignService = new AgentsCampaignService()
  },
  methods: {
    addGroup() {
      if(this.selectedGroup){
        var group_id = this.selectedGroup['value']
        var group = this.groups.find((group) => group_id == group['group']['id'])
        var existing_agents = []
        group['agents'].forEach(agent => {
          if(this.agents_by_campaign.find((a) => a['agent_id'] == agent['agent_id'] )){
            existing_agents.push(agent['agent_username'])
          }else{
            this.addAgentToCampaign(agent)
          }
        })
        this.selectedGroup = null
        if(existing_agents.length > 0){
          this.$swal({
            title: '¡Advertencia!',
            text: `Los siguientes agentes ya estaban en la campaña:
                  ( ${existing_agents.join(' - ')} ), por lo tanto
                  no se agregaron`,
            icon: 'warning',
            timer: 5000,
            showConfirmButton: false
          })
        }else{
          this.$swal({
            title: '¡Operacion exitosa!',
            text: 'Se agrego el grupo exitosamente',
            icon: 'success',
            timer: 4000,
            showConfirmButton: false
          })
        }
      }else{
        this.$swal({
          title: '¡Operacion erronea!',
          text: 'No seleccionaste el grupo',
          icon: 'warning',
          timer: 2000,
          showConfirmButton: false
        })
      }
    },
    ...mapActions(['addAgentToCampaign'])
  },
  async mounted() {
    const {groups} = await this.agentsCampaignService.getActiveAgentsByGroup()
    this.groups = await groups
    this.groupsSelectize = await this.groups.map((group) => {
      return {
        'group': group['group']['name'],
        'value': group['group']['id']
      }
    })
  },
  computed: {
    ...mapState(['agents_by_campaign'])
  }
};
</script>


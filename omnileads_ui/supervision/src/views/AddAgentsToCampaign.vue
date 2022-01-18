<template>
  <div class="card">
    <h1>{{ $t('campaign_info', {name: campaign["nombre"]}) }}</h1>
    <div class="p-fluid p-formgrid p-grid">
      <div class="p-field p-sm-12 p-md-6 p-lg-6 p-xl-6">
        <h2>{{$tc('agent',2)}}</h2>
        <AddAgents />
      </div>
      <div class="p-sm-12 p-md-6 p-lg-6 p-xl-6">
        <h2>{{$tc('group',2)}}</h2>
        <AddGroupAgents />
      </div>
    </div>
    <hr />
    <div class="p-grid">
      <div class="p-sm-12 p-md-12 p-lg-12 p-xl-12">
        <div class="p-d-flex p-jc-between p-ai-center">
          <div><h2>{{$t('agents_campaign')}}</h2></div>
          <div>
            <Button
              class="p-mr-2 p-button-raised p-button-rounded p-button-info"
              label="Penalty"
              icon="pi pi-info-circle"
              v-tooltip.left="'Para modificar el penalty selecciona la columna'"
            />
            <Button
              type="button"
              v-bind:label="$t('actions.save')"
              icon="pi pi-save"
              v-tooltip.left="'Se actualizarán los agentes de la campaña'"
              class="p-button"
              @click="updateAgentsCampaign(this.$route.params.campaign_id)"
            />
          </div>
        </div>
        <AgentsCampaignTable />
      </div>
    </div>
  </div>
</template>

<script>
import { mapActions, mapState } from "vuex";
import AddAgents from "@/components/campaigns/agents/AddAgents.vue";
import AddGroupAgents from "@/components/campaigns/agents/AddGroupAgents.vue";
import AgentsCampaignTable from "@/components/campaigns/agents/AgentsCampaignTable.vue";

export default {
  components: {
    AgentsCampaignTable,
    AddGroupAgents,
    AddAgents,
  },
  created() {
    this.initAgentsCampaign(this.$route.params.campaign_id);
    this.initActiveAgents();
    this.initGroups();
  },
  methods: {
    ...mapActions([
      "initAgentsCampaign",
      "initActiveAgents",
      "initGroups",
      "updateAgentsCampaign",
    ]),
  },
  computed: {
    ...mapState(["campaign"]),
  },
};
</script>

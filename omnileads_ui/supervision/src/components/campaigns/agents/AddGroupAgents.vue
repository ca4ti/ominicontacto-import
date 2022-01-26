<template>
  <div>
    <div class="p-field p-col-12 p-md-8">
      <Dropdown
        v-model="selectedGroup"
        :options="groupsSelectize"
        optionLabel="group"
        :placeholder="$tc('select_a',1,{field: 'grupo'})"
        :filter="true"
        v-bind:filterPlaceholder="$t('find_by', {field: 'nombre'})"
      />
    </div>
    <div class="p-field p-col-12 p-md-3">
      <Button
        type="button"
        v-bind:label="$t('actions.add')"
        class="p-button-outlined"
        @click="addGroup"
      />
    </div>
  </div>
</template>

<script>
import { mapActions, mapState } from "vuex";
import AgentsCampaignService from "@/services/agentsCampaignService.js";

export default {
  data() {
    return {
      groupsSelectize: [],
      selectedGroup: null,
      groups: [],
    };
  },
  created() {
    this.agentsCampaignService = new AgentsCampaignService();
  },
  methods: {
    addGroup() {
      if (this.selectedGroup) {
        var group_id = this.selectedGroup["value"];
        var group = this.groups.find(
          (group) => group_id == group["group"]["id"]
        );
        var existing_agents = [];
        group["agents"].forEach((agent) => {
          if (
            this.agents_by_campaign.find(
              (a) => a["agent_id"] == agent["agent_id"]
            )
          ) {
            existing_agents.push(agent["agent_username"]);
          } else {
            this.addAgentToCampaign(agent);
          }
        });
        this.selectedGroup = null;
        if (existing_agents.length > 0) {
          this.$swal({
            title: this.$t('sweet_alert.title.warning'),
            text: this.$t('pages.add_agents_to_campaign.already_agents_in_campaign', {agents: existing_agents.join(" - ")}),
            icon: "warning",
            timer: 5000,
            showConfirmButton: false,
          });
        }
      } else {
        this.$swal({
          title: this.$t('sweet_alert.title.warning'),
          text: this.$t('pages.add_agents_to_campaign.not_select_type', {type: this.$t('group')}),
          icon: "warning",
          timer: 2000,
          showConfirmButton: false,
        });
      }
    },
    ...mapActions(["addAgentToCampaign"]),
  },
  async mounted() {
    const { groups } =
      await this.agentsCampaignService.getActiveAgentsByGroup();
    this.groups = await groups;
    this.groupsSelectize = await this.groups.map((group) => {
      return {
        group: group["group"]["name"],
        value: group["group"]["id"],
      };
    });
  },
  computed: {
    ...mapState(["agents_by_campaign"]),
  },
};
</script>


<template>
  <div class="card">
    <DataTable
      :value="agents_by_campaign"
      class="p-datatable-sm editable-cells-table"
      showGridlines
      :scrollable="true"
      scrollHeight="600px"
      responsiveLayout="scroll"
      dataKey="id"
      :rows="10"
      :rowsPerPageOptions="[10, 20, 50]"
      :paginator="true"
      paginatorTemplate="CurrentPageReport FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink RowsPerPageDropdown"
      currentPageReportTemplate="Mostrando del {first} al {last} de {totalRecords}"
      v-model:filters="filters"
      filterDisplay="menu"
      :globalFilterFields="[
        'agent_full_name',
        'agent_penalty',
        'representative.name',
      ]"
      editMode="cell"
      @cell-edit-complete="onCellEditComplete"
    >
      <template #header>
        <div class="p-d-flex p-jc-between">
          <Button
            type="button"
            icon="pi pi-filter-slash"
            :label="$t('clean_object',{object: 'filtros'})"
            class="p-button-outlined"
            @click="clearFilter()"
          />
          <span class="p-input-icon-left">
            <i class="pi pi-search" />
            <InputText
              v-model="filters['global'].value"
              icon="pi pi-check"
              :placeholder="$t('find_by', {field: 'nombre'})"
            />
          </span>
        </div>
      </template>
      <template #empty> No se encontraron agentes. </template>
      <template #loading> Cargando la información. Espere por favor. </template>
      <Column field="agent_full_name" :header="$t('agent_campaign.name')"></Column>
      <Column field="agent_username" :header="$t('agent_campaign.username')"></Column>
      <Column field="agent_sip_id" :header="$t('agent_campaign.sip')" :sortable="true"></Column>
      <Column field="agent_penalty" :header="$t('agent_campaign.penalty')" :sortable="true">
        <template #editor="{ data, field }">
          <Dropdown
            v-model="data[field]"
            :options="penalties"
            optionLabel="label"
            optionValue="value"
            placeholder="Selecciona penalty"
          >
            <template #option="slotProps">
              <span>{{ slotProps.option.label }}</span>
            </template>
          </Dropdown>
        </template>
      </Column>
      <Column :exportable="false" style="min-width: 8rem">
        <template #body="slotProps">
          <div class="p-d-flex p-jc-center">
            <Button
              icon="pi pi-trash"
              class="p-button-danger"
              @click="removeAgent(slotProps.data.agent_id)"
            />
          </div>
        </template>
      </Column>
    </DataTable>
  </div>
</template>

<script>
import { mapState, mapActions } from "vuex";
import { FilterMatchMode } from "primevue/api";

export default {
  data() {
    return {
      filters: null,
      penalties: [
        { label: 0, value: 0 },
        { label: 1, value: 1 },
        { label: 2, value: 2 },
        { label: 3, value: 3 },
        { label: 4, value: 4 },
        { label: 5, value: 5 },
        { label: 6, value: 6 },
        { label: 7, value: 7 },
        { label: 8, value: 8 },
        { label: 9, value: 9 },
      ],
    };
  },
  created() {
    this.initFilters();
  },
  mounted() {},
  methods: {
    clearFilter() {
      this.initFilters();
    },
    initFilters() {
      this.filters = {
        global: { value: null, matchMode: FilterMatchMode.CONTAINS },
      };
    },
    removeAgent(agent_id) {
      this.removeAgentOfCampaign(agent_id);
    },
    onCellEditComplete(event) {
      let { data, newValue } = event;
      this.updateAgentPenalty({
        agent_id: data["agent_id"],
        penalty: newValue,
      });
    },
    ...mapActions(["removeAgentOfCampaign", "updateAgentPenalty"]),
  },
  computed: {
    ...mapState(["agents_by_campaign"]),
  },
};
</script>

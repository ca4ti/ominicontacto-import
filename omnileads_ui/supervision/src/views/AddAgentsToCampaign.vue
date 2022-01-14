<template>
    <div class="card">
        <h1>Campaña: TEST</h1>
        <div class="p-fluid p-formgrid p-grid">
            <div class="p-field p-sm-12 p-md-6 p-lg-6 p-xl-6">
                <h2>Agentes</h2>
                <AddAgents />
            </div>
            <div class="p-sm-12 p-md-6 p-lg-6 p-xl-6">
                <h2>Grupos</h2>
                <AddGroupAgents />
            </div>
        </div>
        <hr>
        <div class="p-grid">
            <div class="p-sm-12 p-md-12 p-lg-12 p-xl-12">
                <div class="p-d-flex p-jc-between p-ai-center">
                    <div><h2>Agentes de campaña</h2></div>
                    <div>
                        <Button class="p-mr-2 p-button-raised p-button-rounded p-button-info" label="Penalty" icon="pi pi-info-circle" v-tooltip.left="'Para modificar el penalty selecciona la columna'"/>
                        <Button type="button" label="Guardar" icon="pi pi-save" v-tooltip.left="'Se actualizarán los agentes de la campaña'" class="p-button" @click="updateAgentsCampaign(2)"/>
                    </div>
                </div>
                <Accordion>
                    <AccordionTab>
                        <template #header>
                            <i class="pi pi-calendar"></i>
                            <span>Header I</span>
                        </template>
                        Content
                    </AccordionTab>
                </Accordion>
                <AgentsTable />
            </div>
        </div>
    </div>
</template>

<script>
import { mapActions } from 'vuex'
import AddAgents from '@/components/campaigns/agents/AddAgents.vue'
import AddGroupAgents from '@/components/campaigns/agents/AddGroupAgents.vue'
import AgentsTable from '@/components/campaigns/agents/AgentsTable.vue'

export default {
    components: {
        AgentsTable,
        AddGroupAgents,
        AddAgents,
    },
    created() {
        this.initAgentsCampaign(2)
        this.initActiveAgents()
        this.initGroups()
    },
    methods: {
        ...mapActions(['initAgentsCampaign',
            'initActiveAgents', 'initGroups', 'updateAgentsCampaign']),
    }
}
</script>

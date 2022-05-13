<template>
  <div class="card">
    <Toolbar class="p-mb-4">
      <template #start>
        <h1>{{ $t("views.pause_sets.title") }}</h1>
      </template>
      <template #end>
        <Button
          :label="$tc('globals.new')"
          icon="pi pi-plus"
          class="p-button-success"
          @click="newPauseGroup"
        />
      </template>
    </Toolbar>
    <ExternalSitiesTable
      :externalSities="externalSities"
    ></ExternalSitiesTable>
    <!-- <EditGroup
      :showModal="showModalEdit"
      :group="group"
      @handleModal="handleEditModal"
      @initDataEvent="initData"
    ></EditGroup> -->
  </div>
</template>

<script>
import { mapActions, mapState } from 'vuex';
import ExternalSitiesTable from '@/components/external_sities/ExternalSitiesTable';
// import EditGroup from '@/components/pause_sets/forms/EditGroup';

export default {
    data () {
        return {
            showModalEdit: false,
            group: {}
        };
    },
    components: {
        ExternalSitiesTable
    },
    async created () {
        await this.initData();
    },
    methods: {
        // editGroup (group) {
        //     this.group = group;
        //     this.showModalEdit = true;
        // },
        // newPauseGroup () {
        //     this.$router.push({ name: 'pause_sets_new' });
        // },
        // handleEditModal (show) {
        //     this.showModalEdit = show;
        // },
        async initData () {
            await this.initExternalSities();
        },
        ...mapActions(['initExternalSities'])
    },
    computed: {
        ...mapState(['externalSities'])
    }
};
</script>

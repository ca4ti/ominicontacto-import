<template>
  <div class="card">
    <Toolbar class="p-mb-4">
      <template #start>
        <h1>{{ $t("views.external_sities.list_title") }}</h1>
      </template>
      <template #end>
        <Button
          :label="$tc('globals.new')"
          icon="pi pi-plus"
          class="p-button-success"
          @click="newExternalSite"
        />
      </template>
    </Toolbar>
    <ExternalSitiesTable
      :externalSities="externalSities"
      @showDetail="showDetail"
    ></ExternalSitiesTable>
    <ModalDetail
      :showModal="showModalDetail"
      :externalSite="externalSite"
      @handleModal="handleModal"
    />
  </div>
</template>

<script>
import { mapActions, mapState } from 'vuex';
import ExternalSitiesTable from '@/components/external_sities/ExternalSitiesTable';
import ModalDetail from '@/components/external_sities/ModalDetail';

export default {
    data () {
        return {
            showModalDetail: false,
            externalSite: null
        };
    },
    components: {
        ExternalSitiesTable,
        ModalDetail
    },
    async created () {
        await this.initData();
    },
    methods: {
        showDetail (data) {
            this.externalSite = data;
            this.showModalDetail = true;
        },
        handleModal (show) {
            this.showModalDetail = show;
        },
        newExternalSite () {
            this.$router.push({ name: 'external_sities_new' });
        },
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

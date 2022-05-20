<template>
  <div class="card">
    <Toolbar class="p-mb-4">
      <template #start>
        <h1>{{ $t("globals.edit") }} {{ $tc("globals.pause_set") }}</h1>
      </template>
      <template #end>
        <Button
          :label="$tc('globals.back_to', { type: $t('globals.pause_set') })"
          icon="pi pi-arrow-left"
          class="p-button-info p-mr-2"
          @click="backToExternalSitiesList"
        />
      </template>
    </Toolbar>
    <Form :externalSite="externalSiteDetail" :formToCreate="false" />
  </div>
</template>

<script>
import { mapActions, mapState } from 'vuex';
import Form from '@/components/external_sities/Form';

export default {
    inject: ['$helpers'],
    data () {
        return {
            externalSite: {
                nombre: '',
                url: '',
                metodo: '',
                disparador: '',
                formato: '',
                objetivo: ''
            }
        };
    },
    components: {
        Form
    },
    async created () {
        const id = this.$route.params.id;
        await this.initExternalSiteDetail(id);
    },
    methods: {
        ...mapActions(['initExternalSiteDetail']),
        backToExternalSitiesList () {
            this.$router.push({ name: 'external_sities' });
        }
    },
    computed: {
        ...mapState(['externalSiteDetail'])
    }
};
</script>

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
          @click="newScore"
        />
      </template>
    </Toolbar>
    <ListTable
      :scores="scores"
      @handleModalEvent='handleModal'
    />
    <Modal />
  </div>
</template>

<script>
import { mapActions, mapState } from 'vuex';
import ListTable from '@/components/scores/ListTable';
import Modal from '@/components/scores/Modal';

export default {
    data () {
        return {
            showModal: false,
            score: null
        };
    },
    components: {
        ListTable,
        Modal
    },
    async created () {
        await this.initData();
    },
    methods: {
        handleModal ({ showModal, toCreate, score }) {
            console.log('INDEX - handleModal');
            console.log(showModal, toCreate, score);
            this.showModal = showModal;
        },
        newScore () {
            this.showModal = true;
        },
        async initData () {
            await this.initScores();
        },
        ...mapActions(['initScores'])
    },
    computed: {
        ...mapState(['scores'])
    }
};
</script>

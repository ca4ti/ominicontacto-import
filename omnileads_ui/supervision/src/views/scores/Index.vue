<template>
  <div class="card">
    <Toolbar class="p-mb-4">
      <template #start>
        <h1>{{ $t("views.scores.list_title") }}</h1>
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
    <FormModal
      :showModal='showModal'
      :formToCreate='formToCreate'
      :score="score"
      @handleModalEvent='handleModal'
    />
  </div>
</template>

<script>
import { mapActions, mapState } from 'vuex';
import ListTable from '@/components/scores/ListTable';
import FormModal from '@/components/scores/FormModal';

export default {
    data () {
        return {
            formToCreate: true,
            showModal: false,
            score: { nombre: '' }
        };
    },
    components: {
        ListTable,
        FormModal
    },
    async created () {
        await this.initData();
    },
    methods: {
        handleModal ({ showModal, toCreate, score }) {
            this.formToCreate = toCreate;
            this.showModal = showModal;
            this.score = score;
        },
        newScore () {
            this.showModal = true;
            this.formToCreate = true;
            this.score = { nombre: '' };
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

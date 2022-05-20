<template>
  <Dialog
    :visible="showModal"
    :style="{ width: '50vw' }"
    :closable="false"
    :modal="true"
  >
    <template #header>
      <h3>Informacion del sitio externo</h3>
    </template>
    <template #footer>
      <Button label="ok" @click="closeModal" />
    </template>
  </Dialog>
</template>

<script>
export default {
    props: {
        showModal: {
            type: Boolean,
            default: false
        },
        score: {
            type: Object,
            default: function () {
                return {
                    name: ''
                };
            }
        }
    },
    methods: {
        closeModal () {
            this.$emit('handleModal', false);
        }
    }
};
</script>

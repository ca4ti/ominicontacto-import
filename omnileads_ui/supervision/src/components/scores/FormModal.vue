<template>
  <Dialog
    :visible="showModal"
    :style="{ width: '30vw' }"
    :closable="false"
    :modal="true"
  >
    <template #header>
      <h3 v-if="formToCreate">{{ $t("views.scores.new_title") }}</h3>
      <h3 v-else>{{ $t("views.scores.edit_title") }}</h3>
    </template>
    <div class="card">
      <div class="p-fluid p-grid p-formgrid">
        <div class="field p-col-12">
          <label
            id="score_name"
            :class="{
              'p-error': v$.scoreForm.nombre.$invalid && submitted,
            }"
            >{{ $t("models.score.name") }}*</label
          >
          <div class="p-inputgroup p-mt-2">
            <span class="p-inputgroup-addon">
              <i class="pi pi-list"></i>
            </span>
            <InputText
              id="score_name"
              :class="{
                'p-invalid': v$.scoreForm.nombre.$invalid && submitted,
              }"
              :placeholder='$t("forms.score.enter_name")'
              v-model="v$.scoreForm.nombre.$model"
            />
          </div>
          <small
            v-if="
              (v$.scoreForm.nombre.$invalid && submitted) ||
              v$.scoreForm.nombre.$pending.$response
            "
            class="p-error"
            >{{
              v$.scoreForm.nombre.required.$message.replace(
                "Value",
                $t("models.score.name")
              )
            }}</small
          >
        </div>
      </div>
      <div class="p-flex p-justify-content-end p-flex-wrap">
        <Button
          class="p-button-danger p-button-outlined p-mr-2"
          :label="$t('globals.cancel')"
          @click="closeModal"
        />
        <Button
          :label="$t('globals.save')"
          icon="pi pi-save"
          class="p-mt-4"
          @click="save(!v$.$invalid)"
        />
      </div>
    </div>
  </Dialog>
</template>

<script>
import { required } from '@vuelidate/validators';
import { useVuelidate } from '@vuelidate/core';
import { mapActions } from 'vuex';

export default {
    setup: () => ({ v$: useVuelidate() }),
    validations () {
        return {
            scoreForm: {
                nombre: { required }
            }
        };
    },
    inject: ['$helpers'],
    props: {
        formToCreate: {
            type: Boolean,
            default: true
        },
        showModal: {
            type: Boolean,
            default: false
        },
        score: {
            type: Object,
            default () {
                return {
                    nombre: ''
                };
            }
        }
    },
    data () {
        return {
            scoreForm: {
                nombre: ''
            },
            submitted: false,
            filters: null
        };
    },
    created () {
        this.initializeData();
    },
    methods: {
        ...mapActions(['createScore', 'updateScore']),
        initializeData () {
            this.initFormData();
            this.submitted = false;
        },
        initFormData () {
            this.scoreForm.nombre = this.score.nombre;
        },
        closeModal () {
            this.submitted = false;
            this.$emit('handleModalEvent', {
                showModal: false,
                toCreate: false,
                score: { nombre: '' }
            });
        },
        async save (isFormValid) {
            this.submitted = true;
            if (!isFormValid) {
                return null;
            }
            var response = null;
            var successMsg = null;
            var errorMsg = null;
            if (this.formToCreate) {
                response = await this.createScore(this.scoreForm);
                successMsg = this.$tc('globals.success_added_type', {
                    type: this.$tc('globals.score')
                });
                errorMsg = this.$tc('globals.error_to_created_type', {
                    type: this.$tc('globals.score')
                });
            } else {
                response = await this.updateScore({
                    id: this.score.id,
                    data: this.scoreForm
                });
                successMsg = this.$tc('globals.success_updated_type', {
                    type: this.$tc('globals.score')
                });
                errorMsg = this.$tc('globals.error_to_updated_type', {
                    type: this.$tc('globals.score')
                });
            }
            this.closeModal();
            if (response) {
                this.$router.push({ name: 'scores' });
                this.$swal(
                    this.$helpers.getToasConfig(
                        this.$t('globals.success_notification'),
                        successMsg,
                        this.$t('globals.icon_success')
                    )
                );
            } else {
                this.$swal(
                    this.$helpers.getToasConfig(
                        this.$t('globals.error_notification'),
                        errorMsg,
                        this.$t('globals.icon_error')
                    )
                );
            }
        }
    },
    watch: {
        score: {
            handler () {
                this.initFormData();
            },
            deep: true,
            immediate: true
        }
    }
};
</script>

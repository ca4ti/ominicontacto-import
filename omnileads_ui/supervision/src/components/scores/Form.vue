<template>
  <div class="card">
    <div class="p-fluid p-grid p-formgrid p-mt-4">
      <div class="field p-col-6">
        <label
          id="score_name"
          :class="{
            'p-error': v$.scoreForm.nombre.$invalid && submitted,
          }"
          >{{ $t("models.external_site.name") }}*</label
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
              $t("models.external_site.name")
            )
          }}</small
        >
      </div>
    </div>
    <div class="p-flex p-flex-row-reverse p-flex-wrap">
      <div class="p-flex p-align-items-center">
        <Button
          :label="$t('globals.save')"
          icon="pi pi-save"
          class="p-mt-4"
          @click="save(!v$.$invalid)"
        />
      </div>
    </div>
  </div>
</template>

<script>
import { FilterMatchMode } from 'primevue/api';
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
        score: {
            type: Object,
            default () {
                return {
                    nombre: '',
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
            this.scoreForm.nombre =  this.score.nombre;
        },
        clearFilter () {
            this.initFilters();
        },
        initFilters () {
            this.filters = {
                global: { value: null, matchMode: FilterMatchMode.CONTAINS }
            };
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
                    type: this.$tc('globals.external_site')
                });
                errorMsg = this.$tc('globals.error_to_created_type', {
                    type: this.$tc('globals.external_site')
                });
            } else {
                response = await this.updateScore({
                    id: this.score.id,
                    data: this.scoreForm
                });
                successMsg = this.$tc('globals.success_updated_type', {
                    type: this.$tc('globals.external_site')
                });
                errorMsg = this.$tc('globals.error_to_updated_type', {
                    type: this.$tc('globals.external_site')
                });
            }
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

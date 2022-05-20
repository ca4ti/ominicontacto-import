<template>
  <div class="card">
    <DataTable
      :value="externalSitiesFilter"
      class="p-datatable-sm"
      showGridlines
      :scrollable="true"
      scrollHeight="600px"
      responsiveLayout="scroll"
      dataKey="id"
      :rows="10"
      :rowsPerPageOptions="[10, 20, 50]"
      :paginator="true"
      paginatorTemplate="CurrentPageReport FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink RowsPerPageDropdown"
      :currentPageReportTemplate="
        $t('globals.showing_datatable_info', {
          first: '{first}',
          last: '{last}',
          totalRecords: '{totalRecords}',
        })
      "
      :filters="filters"
      :globalFilterFields="['nombre']"
    >
      <template #header>
        <div class="p-d-flex p-jc-between">
          <Button
            type="button"
            icon="pi pi-filter-slash"
            :label="$t('globals.clean_filter')"
            class="p-button-outlined"
            @click="clearFilter()"
          />
          <div>
            <span class="p-input-icon-left">
              <i class="pi pi-search" />
              <InputText
                v-model="filters['global'].value"
                icon="pi pi-check"
                :placeholder="
                  $t('globals.find_by', { field: $tc('globals.name', 1) })
                "
              />
            </span>
          </div>
        </div>
      </template>
      <template #empty> {{ $t("globals.without_data") }} </template>
      <template #loading> {{ $t("globals.load_info") }} </template>
      <Column
        field="nombre"
        :sortable="true"
        :header="$t('models.external_site.name')"
      ></Column>
      <Column :header="$tc('globals.option', 2)" :exportable="false">
        <template #body="slotProps">
          <Button
            icon="pi pi-eye"
            v-if="slotProps.data.oculto == true"
            class="p-button-success p-ml-2"
            @click="show(slotProps.data.id)"
            v-tooltip.top="$t('views.external_sities.show')"
          />
          <Button
            icon="pi pi-eye-slash"
            v-if="slotProps.data.oculto == false"
            class="p-button-secondary p-ml-2"
            @click="hide(slotProps.data.id)"
            v-tooltip.top="$t('views.external_sities.hide')"
          />
          <Button
            icon="pi pi-pencil"
            class="p-button-warning p-ml-2"
            @click="toEditExternalSite(slotProps.data)"
            v-tooltip.top="$t('globals.edit')"
          />
          <Button
            icon="pi pi-trash"
            class="p-button-danger p-ml-2"
            @click="remove(slotProps.data.id)"
            v-tooltip.top="$t('globals.delete')"
          />
          <Button
            icon="pi pi-info-circle"
            class="p-button-info p-ml-2"
            @click="showExternalSiteDetail(slotProps.data)"
            v-tooltip.top="$t('globals.help')"
          />
        </template>
      </Column>
    </DataTable>
  </div>
</template>

<script>
import { mapActions } from 'vuex';
import { FilterMatchMode } from 'primevue/api';

export default {
    inject: ['$helpers'],
    props: {
        scores: {
            type: Array,
            default: () => []
        }
    },
    data () {
        return {
            filters: null
        };
    },
    created () {
        this.initFilters();
    },
    methods: {
        clearFilter () {
            this.initFilters();
        },
        initFilters () {
            this.filters = {
                global: { value: null, matchMode: FilterMatchMode.CONTAINS }
            };
        },
        toEditScore (externalSite) {
            this.$router.push({
                name: 'external_sities_update',
                params: { id: externalSite.id },
                props: { externalSite }
            });
        },
        async remove (id) {
            this.$swal({
                title: this.$t('globals.sure_notification'),
                text: this.$t('views.pause_sets.pause_settings_will_be_deleted'),
                icon: this.$t('globals.icon_warning'),
                showCancelButton: true,
                confirmButtonText: this.$t('globals.yes'),
                cancelButtonText: this.$t('globals.no'),
                backdrop: false,
                reverseButtons: true
            }).then(async (result) => {
                if (result.isConfirmed) {
                    this.$swal.fire({
                        title: this.$t('globals.processing_request'),
                        timerProgressBar: true,
                        allowOutsideClick: false,
                        didOpen: () => {
                            this.$swal.showLoading();
                        }
                    });
                    const resp = await this.deleteExternalSite(id);
                    this.$swal.close();
                    if (resp) {
                        this.initExternalSities();
                        this.$swal(
                            this.$helpers.getToasConfig(
                                this.$t('globals.success_notification'),
                                this.$tc('globals.success_deleted_type', {
                                    type: this.$tc('globals.external_site')
                                }),
                                this.$t('globals.icon_success')
                            )
                        );
                    } else {
                        this.$swal(
                            this.$helpers.getToasConfig(
                                this.$t('globals.error_notification'),
                                this.$tc('globals.error_to_deleted_type', {
                                    type: this.$tc('globals.external_site')
                                }),
                                this.$t('globals.icon_error')
                            )
                        );
                    }
                } else if (result.dismiss === this.$swal.DismissReason.cancel) {
                    this.$swal(
                        this.$helpers.getToasConfig(
                            this.$t('globals.cancelled'),
                            this.$tc('globals.error_to_deleted_type', {
                                type: this.$tc('globals.external_site')
                            }),
                            this.$t('globals.icon_error')
                        )
                    );
                }
            });
        },
        ...mapActions([
            'deleteExternalSite',
            'initExternalSities'
        ])
    },
    watch: {
        externalSities: {
            handler () {
                this.initDataTable();
            },
            deep: true,
            immediate: true
        }
    }
};
</script>

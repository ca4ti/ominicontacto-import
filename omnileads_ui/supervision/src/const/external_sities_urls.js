export default {
    ExternalSitiesList: '/api/v1/external_sities',
    ExternalSiteCreate: '/api/v1/external_sities/create/',
    ExternalSiteDetail: (id) => `/api/v1/external_sities/${id}`,
    ExternalSiteUpdate: (id) => `/api/v1/external_sities/${id}/update/`,
    ExternalSiteDelete: (id) => `/api/v1/external_sities/${id}/delete`,
    ExternalSiteHide: (id) => `/api/v1/external_sities/${id}/hide`,
    ExternalSiteShow: (id) => `/api/v1/external_sities/${id}/show`
};

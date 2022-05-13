export default {
    ExternalSitiesList: '/api/v1/external_sities',
    ExternalSiteCreate: '/api/v1/external_site/create/',
    ExternalSiteDetail: (id) => `/api/v1/external_site/${id}`,
    ExternalSiteUpdate: (id) => `/api/v1/external_site/${id}/update/`,
    ExternalSiteDelete: (id) => `/api/v1/external_site/${id}/delete`,
    ExternalSiteHide: (id) => `/api/v1/external_site/${id}/hide`,
    ExternalSiteShow: (id) => `/api/v1/external_site/${id}/show`
};

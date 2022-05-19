/* eslint-disable no-unused-vars */
import ExternalSiteService from '@/services/externalSiteService';
const externalSiteService = new ExternalSiteService();

export default {
    async initExternalSities ({ commit }) {
        const { externalSities } = await externalSiteService.externalSitiesList();
        commit('initExternalSities', externalSities);
    },
    async initExternalSiteDetail ({ commit }, id) {
        const { externalSiteDetail } = await externalSiteService.externalSiteDetail(id);
        commit('initExternalSiteDetail', externalSiteDetail);
    },
    async deleteExternalSite ({ commit }, id) {
        const { status } = await externalSiteService.deleteExternalSite(id);
        if (status === 'SUCCESS') {
            return true;
        }
        return false;
    },
    async hideExternalSite ({ commit }, id) {
        const { status } = await externalSiteService.hideExternalSite(id);
        if (status === 'SUCCESS') {
            return true;
        }
        return false;
    },
    async showExternalSite ({ commit }, id) {
        const { status } = await externalSiteService.showExternalSite(id);
        if (status === 'SUCCESS') {
            return true;
        }
        return false;
    },
    async createExternalSite ({ commit }, data) {
        const { status } = await externalSiteService.createExternalSite(data);
        if (status === 'SUCCESS') {
            const { externalSities } = await externalSiteService.externalSitiesList();
            commit('initExternalSities', externalSities);
            return true;
        }
        return false;
    },
    async updateExternalSite ({ commit }, { id, data }) {
        const { status } = await externalSiteService.updateExternalSite(id, data);
        if (status === 'SUCCESS') {
            return true;
        }
        return false;
    }
};

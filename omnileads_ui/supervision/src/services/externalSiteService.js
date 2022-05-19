import apiUrls from '../const/api-urls';
import { HTTP, BaseService } from './apiBaseService';

export default class ExternalSiteService extends BaseService {
    async externalSitiesList () {
        try {
            const resp = await fetch(apiUrls.ExternalSitiesList, this.payload);
            return await resp.json();
        } catch (error) {
            console.error('No se pudieron obtener los sitios externos');
            return [];
        }
    }

    async externalSiteDetail (id) {
        try {
            const resp = await fetch(
                apiUrls.ExternalSiteDetail(id), this.payload);
            return await resp.json();
        } catch (error) {
            console.error('No se pudo obtener el detalle del sitio externo');
            return [];
        }
    }

    async hideExternalSite (id) {
        try {
            const resp = await fetch(
                apiUrls.ExternalSiteHide(id), this.payload);
            return await resp.json();
        } catch (error) {
            console.error('No se pudo ocultar el sitio externo');
            return [];
        }
    }

    async showExternalSite (id) {
        try {
            const resp = await fetch(
                apiUrls.ExternalSiteShow(id), this.payload);
            return await resp.json();
        } catch (error) {
            console.error('No se pudo desocultar el sitio externo');
            return [];
        }
    }

    async deleteExternalSite (id) {
        try {
            this.setPayload(HTTP.DELETE);
            const resp = await fetch(
                apiUrls.ExternalSiteDelete(id),
                this.payload
            );
            this.initPayload();
            return await resp.json();
        } catch (error) {
            console.error('No se pudo eliminar el sitio externo');
            return [];
        }
    }

    async createExternalSite (data) {
        try {
            this.setPayload(HTTP.POST, JSON.stringify(data));
            const resp = await fetch(
                apiUrls.ExternalSiteCreate,
                this.payload
            );
            this.initPayload();
            return await resp.json();
        } catch (error) {
            console.error('No se pudo crear el sitio externo');
            console.error(error);
            return {};
        }
    }

    async updateExternalSite (id, data) {
        try {
            this.setPayload(HTTP.PUT, JSON.stringify(data));
            const resp = await fetch(
                apiUrls.ExternalSiteUpdate(id),
                this.payload
            );
            this.initPayload();
            return await resp.json();
        } catch (error) {
            console.error('No se pudo actualizar el sitio externo');
            console.error(error);
            return {};
        }
    }
}

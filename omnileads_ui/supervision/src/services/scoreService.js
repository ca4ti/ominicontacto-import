import apiUrls from '../const';
import { HTTP, BaseService } from './apiBaseService';

export default class ScoreService extends BaseService {
    async list () {
        try {
            const resp = await fetch(apiUrls.ScoresList, this.payload);
            return await resp.json();
        } catch (error) {
            console.error('No se pudieron obtener los sitios externos');
            return [];
        }
    }

    async delete (id) {
        try {
            this.setPayload(HTTP.DELETE);
            const resp = await fetch(
                apiUrls.ScoresDelete(id),
                this.payload
            );
            this.initPayload();
            return await resp.json();
        } catch (error) {
            console.error('No se pudo eliminar el sitio externo');
            return [];
        }
    }

    async create (data) {
        try {
            this.setPayload(HTTP.POST, JSON.stringify(data));
            const resp = await fetch(
                apiUrls.ScoresCreate,
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

    async update (id, data) {
        try {
            this.setPayload(HTTP.PUT, JSON.stringify(data));
            const resp = await fetch(
                apiUrls.ScoresUpdate(id),
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

/* eslint-disable no-unused-vars */
import ScoreService from '@/services/ScoreService';
const scoreService = new ScoreService();

export default {
    async initScores ({ commit }) {
        const { scores } = await scoreService.list();
        commit('initScores', scores);
    },
    async deleteScore ({ commit }, id) {
        const { status } = await scoreService.delete(id);
        if (status === 'SUCCESS') {
            return true;
        }
        return false;
    },
    async createScore ({ commit }, data) {
        const { status } = await scoreService.create(data);
        if (status === 'SUCCESS') {
            const { scores } = await scoreService.list();
            commit('initScores', scores);
            return true;
        }
        return false;
    },
    async updateScore ({ commit }, { id, data }) {
        const { status } = await scoreService.update(id, data);
        if (status === 'SUCCESS') {
            const { scores } = await scoreService.list();
            commit('initScores', scores);
            return true;
        }
        return false;
    }
};

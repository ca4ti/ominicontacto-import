export default {
    ScoresList: '/api/v1/scores',
    ScoresCreate: '/api/v1/scores/create/',
    ScoresUpdate: (id) => `/api/v1/scores/${id}/update/`,
    ScoresDelete: (id) => `/api/v1/scores/${id}/delete`
};

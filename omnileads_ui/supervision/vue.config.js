import { getCsfrToken, getPageConfig } from './src/helpers/vue_config_helper';

module.exports = {
    publicPath: '/static/omnileads-ui-supervision/',
    pages: {
        ...getPageConfig('supervision_dashboard'),
        ...getPageConfig('audit_page'),
        ...getPageConfig('add_agents_to_campaign'),
        ...getPageConfig('pause_sets'),
        ...getPageConfig('external_sities')
    },
    devServer: {
        proxy: {
            '/api': {
                target: 'https://nginx',
                ws: false,
                changeOrigin: true,
                logLevel: 'debug',
                secure: false,
                bypass: (req) => {
                    if (req.headers && req.headers.referer) {
                        req.headers['X-CSRFToken'] = getCsfrToken(req.headers.cookie);
                    }
                }
            },
            '/media': {
                target: 'https://nginx',
                changeOrigin: true
            }
        }
    }
};

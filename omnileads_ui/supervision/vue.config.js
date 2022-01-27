const path = require("path");
module.exports = {
    publicPath: '/static/omnileads-ui-supervision/',
    pages: {
        add_agents_to_campaign: {
            entry: 'src/pages/add_agents_to_campaign/main.js',
            template: 'public/add_agents_to_campaign.html',
            filename: 'add_agents_to_campaign.html',
            title: 'add_agents_to_campaign',
            chunks: ['chunk-vendors', 'chunk-common', 'add_agents_to_campaign']
        },
    },
    devServer: {
        proxy: {
            '/api': {
                target: 'https://nginx',
                ws: false,
                changeOrigin: true,
                logLevel: 'debug',
                secure: false,
                bypass: (req, res) => {
                    if (req.headers && req.headers.referer) {
                        req.headers['X-CSRFToken'] = getCsfrToken(req.headers.cookie)
                    }
                    console.log(req.headers)
                },
            },
            '/media': {
                target: 'https://nginx',
                changeOrigin: true

            },
        }
    }
}

function getCsfrToken(cookie) {
    let arr = cookie.split(';');
    for (const a in arr) {
        if (arr[a].search('csrftoken=') != -1) {
            return arr[a].replace('csrftoken=', '')
        }
    }
}

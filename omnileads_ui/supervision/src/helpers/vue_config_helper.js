export function getCsfrToken (cookie) {
    const arr = cookie.split(';');
    for (const a in arr) {
        if (arr[a].search('csrftoken=') !== -1) {
            return arr[a].replace('csrftoken=', '');
        }
    }
}

export function getPageConfig(pageName) {
    return {
        pageName: {
            entry: 'src/main.js',
            template: `public/${pageName}.html`,
            filename: pageName,
            title: pageName,
            chunks: ['chunk-vendors', 'chunk-common', pageName]
        }
    }
}
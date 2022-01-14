import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

// Primevue
import PrimeVue from 'primevue/config'
import 'primeflex/primeflex.css'
import 'primevue/resources/themes/saga-blue/theme.css'       //theme
import 'primevue/resources/primevue.min.css'                 //core css
import 'primeicons/primeicons.css'                           //icons

// Components primevue
import Card from 'primevue/card';
import Button from 'primevue/button';

// Idiomas
import { createI18n } from 'vue-i18n'
import es from './../i18n/es'
import en from './../i18n/en'
import fa from './../i18n/fa'
import pt_br from '../i18n/pt-br'

import Cookies from "universal-cookie";
const cookies = new Cookies();
const lenguage = cookies.get("django_language")

// Configuramos los idiomas
const i18n = createI18n({
    locale: lenguage,
    fallbackLocale: lenguage,
    messages: {
        es,
        en,
        fa,
        'pt-br': pt_br
    }
})

const app = createApp(App)

app.component('Card', Card)
app.component('Button', Button)

app.use(i18n)
    .use(router)
    .use(PrimeVue)
    .mount('#app')
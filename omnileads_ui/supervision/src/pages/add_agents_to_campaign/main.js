import { createApp } from 'vue'
import VueSweetalert2 from 'vue-sweetalert2'
import store from '../../store'
import router from '../../router'
import App from './App.vue'

// Primevue
import PrimeVue from 'primevue/config'
import 'primeflex/primeflex.css'
import 'primevue/resources/themes/saga-green/theme.css'       //theme
import 'primevue/resources/primevue.min.css'                 //core css
import 'primeicons/primeicons.css'                           //icons

// Sweetalert Vue
import 'sweetalert2/dist/sweetalert2.min.css'

// Components primevue
import Card from 'primevue/card'
import Button from 'primevue/button'
import InputText from 'primevue/inputtext'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import ColumnGroup from 'primevue/columngroup'
import MultiSelect from 'primevue/multiselect'
import Message from 'primevue/message'
import Tooltip from 'primevue/tooltip'
import Dropdown from 'primevue/dropdown'

// Idiomas
import { createI18n } from 'vue-i18n'
import es from '../../../i18n/es'
import en from '../../../i18n/en'
import fa from '../../../i18n/fa'
import pt_br from '../../../i18n/pt-br'

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

app.directive('tooltip', Tooltip)
app.component('Card', Card)
app.component('Button', Button)
app.component('InputText', InputText)
app.component('DataTable', DataTable)
app.component('Column', Column)
app.component('ColumnGroup', ColumnGroup)
app.component('MultiSelect', MultiSelect)
app.component('Message', Message)
app.component('Dropdown', Dropdown)

app.use(i18n)
    .use(store)
    .use(router)
    .use(VueSweetalert2)
    .use(PrimeVue)
    .mount('#app')
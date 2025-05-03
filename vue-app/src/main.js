import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import Vant from 'vant'
import 'vant/lib/index.css'
import axios from 'axios'

const app = createApp(App)

app.use(router)
app.use(Vant)
app.config.globalProperties.$axios = axios

app.mount('#app')

import { createApp } from 'vue'
import App from './App.vue'
import router from '@/router/index'
import {Quasar, Dialog, Notify} from 'quasar'
import axios from 'axios'

// Import icon libraries
import '@quasar/extras/material-icons/material-icons.css'

// Import Quasar css
import 'quasar/dist/quasar.css'

// 请求拦截器
axios.interceptors.request.use((config)=>{
    config.baseURL = 'http://127.0.0.1:8080'
    return config
})

// 响应拦截器
axios.interceptors.response.use(
    // 响应成功的回调函数
    res => {
        console.log('响应成功');
        // 把响应数据return给axios的请求函数 await axios
        return res.data
    },
    // 响应失败的回调
    err => {
        console.log('响应失败',err)
        // return Promise.reject(err)
        // 不需要try catch
        return new Promise(()=>{})
    }
)

const app = createApp(App)
app.use(router)
app.use(axios)
app.use(Quasar,{
    plugins: {
        Dialog,
        Notify
    }
})
app.mount('#app')

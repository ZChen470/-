import {createRouter, createWebHistory} from 'vue-router'

import GalaxySinglePicture from '@/pages/GalaxySinglePicture.vue'
import GalaxyMultiPicture from '@/pages/GalaxyMultiPicture.vue'
import GalaxySingleCoord from '@/pages/GalaxySingleCoord.vue'
import GalaxyMultiCoord from '@/pages/GalaxyMultiCoord.vue'

const router = createRouter({
    history: createWebHistory(),
    routes:[
        {
            path:'/GalSPic',
            component:GalaxySinglePicture
        },
        {
            path:'/GalMPic',
            component:GalaxyMultiPicture
        },
        {
            path:'/GalSCoo',
            component:GalaxySingleCoord
        },
        {
            path:'/GalMCoo',
            component:GalaxyMultiCoord
        },
    ]
})

export default router
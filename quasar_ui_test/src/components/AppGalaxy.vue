<template>
    <div class="container">
<!-- q-drawer -->
    <GalaxyNav class="fixed-nav">
    </GalaxyNav>
        <!-- :headers="()=>[{name:'Accept',value:'application/json'}]" -->
            <!-- :field-name="() => 'file'" -->
        <!-- 您还可以通过 headers 和 method 属性设置 HTTP 请求头和 HTTP 请求方式，请查看 API 部分。 -->
    <div class="row items-start shadow-4 q-pa-sm q-gutter-md content-box">
        <q-card class="my-card" flat bordered>

            <q-card-section>
            <div class="text-h4 text-orange-9">{{ category }}</div>
            <div class="text-h6 q-mt-sm q-mb-sm">置信度&nbsp;{{ conf }}</div>

            <q-separator color="orange" inset />

            <div class="q-mt-sm text-body1">
                {{ desc }}
            </div>
            </q-card-section>

            <q-card-actions>
                <q-btn flat color="dark" label="Share" />
                <q-btn flat color="primary" label="Copy" @click="copy"/>

                <q-space />
            </q-card-actions>
        </q-card>

        <q-card class="my-card">
            <img :src="imageBase64" v-if="imageBase64">

            <q-card-section>
                <div class="text-h6">{{ name }}</div>
                <div class="text-subtitle2">{{ source }}</div>
            </q-card-section>

            <q-card-section class="q-pt-none text-body1">
                {{ profile }}
            </q-card-section>
            <q-table
                v-if="info_table.length>0 && !profile"
                grid
                title="搜索结果"
                :rows="rows"
                :columns="columns"
                row-key="name"
                :filter="filter"
                :rows-per-page-options="[2]"
                card-container-class="q-ml-sm"
                :card-container-style="{ 'width': '40vw' }"
                card-class="bg-cyan-8 text-white text-weight-bold"
                :card-style="{ width: '10vw' }"
                hide-header
            >
            </q-table>
        </q-card>
    </div>

    </div>
    
</template>
  
<script setup name="AppGalaxy">
    import { ref, provide, watch } from 'vue'
    import { useQuasar } from 'quasar'
    import GalaxyNav from './GalaxyNav.vue';

    const $q = useQuasar()

    let category = ref("category")
    let conf = ref("0.00%")
    let desc = ref("xxx")
    let profile = ref("")
    let source = ref("")
    let name = ref("")
    let imageBase64 = ref("")
    let info_table = ref([])
    const uploadImageUrl = 'http://59.110.67.30:8080/predict'
    const uploadCoordUrl = 'http://59.110.67.30:8080/coord_csv'
    const coordUrl = 'http://59.110.67.30:8080/coord'
    const copy = () => {
        let text = `${category.value}\n${conf.value}\n${desc.value}`
        navigator.clipboard.writeText(text)
        navigator.clipboard.writeText(text).then(() => {
            $q.dialog({
                title: '提示',
                message: '已成功复制到粘贴板'
            }).onOk(() => {
                // console.log('OK')
            }).onCancel(() => {
                // console.log('Cancel')
            }).onDismiss(() => {
                // console.log('I am triggered on both OK and Cancel')
            })
        })
    }

    const columns = [
    {
        name: 'ra',
        required: true,
        label: 'RA',
        align: 'left',
        field: row => row.ra,
        sortable: true
    },
    { name: 'dec',  label: 'DEC', field: 'dec'},
    { name: 'main_id', label: 'Main_ID', field: 'main_id' },
    { name: 'rvz_redshift', label: 'Redshift', field: 'rvz_redshift' },
    { name: 'otype', label: 'otype', field: 'otype' },
    { name: 'morph', label: 'morph', field: 'morph' },
    { name: 'galdim_majaxis', label: 'galdim_majaxis', field: 'galdim_majaxis' },
    ]

    let rows = []
    watch(info_table,()=>{
        profile.value = ""
        source.value =  ""
        name.value = ""
        imageBase64.value = ""
        rows = []
        for (const item of info_table.value) {
        let jsonItem = {
           ra: item.ra,
           dec: item.dec,
           main_id: item.main_id,
           rvz_redshift: item.rvz_redshift,
           otype: item.otype,
           morph: item.morph,
           galdim_majaxis: item.galdim_majaxis
        }
        rows.push(jsonItem)
    }

    })
    for (const item of info_table.value) {
        let jsonItem = {
           ra: item.ra,
           dec: item.dec,
           main_id: item.main_id,
           rvz_redshift: item.rvz_redshift,
           otype: item.otype,
           morph: item.morph,
           galdim_majaxis: item.galdim_majaxis
        }
        row.push(jsonItem)
    }

    // 祖孙通信
    provide('category', category)
    provide('conf', conf)
    provide('desc', desc)
    provide('profile', profile)
    provide('source', source)
    provide('name', name)
    provide('imageBase64', imageBase64)
    provide('uploadImageUrl', uploadImageUrl)
    provide('uploadCoordUrl', uploadCoordUrl)
    provide('coordUrl', coordUrl)
    provide('info_table', info_table)
    // 
</script>

<style scoped>
    .fixed-nav {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        z-index: 9999;
    }
    .container {
        position: relative;
    }
    .content-box {
        position: absolute;
        left: 40vw;
        top: 0px;
        width: fit-content;
        backdrop-filter: blur(10px) brightness(90%);
        background-color: rgba(255, 255, 255, 0.37);
        border-radius: 10px
    }
    .my-card{
        width: 22vw;
        min-height: 32vw;
    }
    q-uploader {
        width: 1vw;
    }
</style>
  
<template>
    <div class="q-mt-xl column items-start shadow-4 multi-coord">
        <q-uploader
            label="上传星系坐标csv"
            :factory="factoryFn"
            @uploaded="uploaded"
            @uploading="uploading"
            multiple
            max-file-size="1048576"
            max-files="1"
            accept=".csv"
            batch
            @rejected="onRejected"
            no-thumbnails
            bordered
            color="cyan-8"
        />
    </div>
</template>

<script setup lang="ts" name="GalaxyMultiCoord">
    import { ref, inject } from 'vue'
    import { useQuasar } from 'quasar'
    import {saveAs} from 'file-saver'

    const $q = useQuasar()
    
    let uploadUrl = inject('uploadCoordUrl')

    const uploading = (info) => {
        info.xhr.responseType = 'blob'
    }

    const factoryFn = (files) => {
        return {
            url: uploadUrl,
            headers: [{name:'Accept',value:'application/json'}],
            fieldName:'file',
            method: 'POST'
        }
    }

    const uploaded  = (info) => {
        let res = info.xhr.response
        saveAs(res, 'images.zip')
    }

    function onRejected (rejectedEntries) {
        // Notify plugin needs to be installed
        // https://quasar.dev/quasar-plugins/notify#Installation
        $q.notify({
            type: 'negative',
            message: `${rejectedEntries.length} file(s) did not pass validation constraints`
        })
    }
</script>

<style scoped>
    .multi-coord{
        width: 380px;
        height: 380px;
        display: flex;
        justify-content: center;
        align-items: center;
        backdrop-filter: blur(10px) brightness(90%);
        background-color: rgba(255, 255, 255, 0.37);
        border-radius: 10px
    }
</style>

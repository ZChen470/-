<template>
    <div class="q-mt-xl column items-start shadow-4 multi-picture">
        <q-uploader
            class="qup"
            label="多幅图像类别标注(≤20×1M)"
            :factory="factoryFn"
            @uploaded="uploaded"
            @uploading="uploading"
            multiple
            max-file-size="1048576"
            max-files="20"
            accept=".jpg, jpeg, .png"
            batch
            @rejected="onRejected"
            no-thumbnails
            bordered
            color="cyan-8"
        />
    </div>
</template>

<script setup lang="ts" name="GalaxySinglePicture">
    import { ref, inject } from 'vue'
    import { useQuasar } from 'quasar'
    import {saveAs} from 'file-saver'
    import streamSaver from "streamsaver"

    const $q = useQuasar()
    
    let uploadUrl = inject('uploadImageUrl')

    const uploading = (info) => {
        info.xhr.responseType = 'blob'
    }

    const factoryFn = (files) => {
        return {
            url: uploadUrl,
            headers: [{name:'Accept',value:'application/json'}],
            fieldName:'files',
            method: 'POST'
        }
    }

    // const uploaded  = (info) => {
    //     let res = info.xhr.response
    //     saveAs(res, 'images.zip')
    // }

    // stream download 处理大文件下载
    const uploaded = (info) => {
        let res = info.xhr.response;
        
        // 将 response 转换为 Blob
        if (!(res instanceof Blob)) {
            console.error('Response is not a Blob');
            return;
        }
        
        const fileStream = streamSaver.createWriteStream('images.zip');
        const writer = fileStream.getWriter();
        const reader = res.stream().getReader();

        const pump = () => reader.read()
            .then(({ done, value }) => done
                ? writer.close()
                : writer.write(value).then(pump));

        pump().catch(error => {
            console.error('Stream pump error:', error);
            writer.abort(error);
        });
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
    .multi-picture{
        width: 25vw;
        height: 22vw;
        display: flex;
        justify-content: center;
        align-items: center;
        backdrop-filter: blur(10px) brightness(90%);
        background-color: rgba(255, 255, 255, 0.37);
        border-radius: 10px
    }
</style>
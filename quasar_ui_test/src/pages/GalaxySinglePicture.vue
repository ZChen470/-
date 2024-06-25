<template>
    <div class="q-mt-xl column items-start shadow-4 single-picture">
        <q-uploader
        class="qup"
        label="上传单张星系图像(≤10M)"
        :factory="factoryFn"
        @uploaded="uploaded"
        multiple
        max-file-size="10485760"
        max-files="1"
        accept=".jpg, .jpeg, .png"
        @rejected="onRejected"
        bordered
        color="cyan-8"
        />
    </div>
</template>

<script setup lang="ts" name="GalaxySinglePicture">
    import { ref, inject } from 'vue'
    import { useQuasar } from 'quasar'

    const $q = useQuasar()

    let img_prefix = ref("data:image/jpeg;base64,")

    // 注入数据
    let category = inject("category")
    let uploadUrl = inject("uploadImageUrl")
    let conf = inject("conf")
    let desc = inject("desc")
    let profile = inject("profile")
    let source = inject("source")
    let name = inject("name")
    let imageBase64 = inject("imageBase64")


    const factoryFn = (files) => {
        return {
            url: uploadUrl,
            headers: [{name:'Accept',value:'application/json'}],
            fieldName:'files',
            method: 'POST'
        }
    }

    const uploaded  = (info) => {
        const res = JSON.parse(info.xhr.response)
        category.value = res.category
        conf.value = res.confidence
        desc.value = res.description
        
        name.value = res.represent.name
        profile.value = res.represent.profile
        source.value = res.represent.source
        imageBase64.value = `${img_prefix.value}${res.image}`
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
    .single-picture{
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
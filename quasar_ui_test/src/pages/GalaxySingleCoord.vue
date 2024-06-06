<template>
    <div class="q-pa-md column single-coord">
  
      <div id="aladin-lite-div" style="width:450px;height:450px;margin-bottom: 10px;"></div>
      <div>
          <q-btn 
        color="cyan-8"
        label="获取类别"
        :loading="submitting"
        @click="onSubmit"
        style="width:120px">
        <template v-slot:loading>
            <q-spinner-facebook />
        </template>
      </q-btn>
      </div>
    </div>
</template>
  
<script setup  name="GalaxySingelCoord">
    import { useQuasar } from 'quasar'
    import {ref, inject} from 'vue'
    import axios from 'axios'

    const $q = useQuasar()

    const submitting = ref(false)

    let category = inject("category")

    let conf = inject("conf")
    let desc = inject("desc")
    let info_table = inject("info_table")

    let aladin;
    A.init.then(() => {
        aladin = A.aladin('#aladin-lite-div', {
            target: 'NGC 1365',
            cooFrame: 'ICRS',
            survey: 'P/DESI-Legacy-Surveys/DR10/color',
            fov: 0.5 // deg
        });
    });

    const onSubmit = async () => {
        submitting.value = true
        // get information about Aladin View: RA DEC FOV size survey
        const view = aladin.getRaDec()
        const ra = view[0]
        const dec = view[1]
        const fov = aladin.getFov()[0]
        const size = parseInt(aladin.getSize()[0])
        let imagelayer = aladin.getBaseImageLayer()
        const surveyid = imagelayer.creatorDid

        $q.notify({
            color: 'green-4',
            textColor: 'white',
            icon: 'cloud_done',
            message: '提交成功',
            position:'top'
        })

        const result = await axios({
          url: `/coord`,
          headers: {
            'Content-Type': 'application/json'
          },
          method:'POST',
          data: {
            ra:ra,
            dec:dec,
            fov:fov,
            size:size,
            surveyid:surveyid
          }
        })
        submitting.value = false
        
        // return response data
        category.value = result.category
        conf.value = result.confidence
        desc.value = result.description
        info_table.value = result.info_table
    }
</script>

<style scoped>
    .single-coord {
        width: 520px;
        height: 530px;
        display: flex;
        justify-content: center;
        align-items: center;
        backdrop-filter: blur(10px) brightness(90%);
        background-color: rgba(255, 255, 255, 0.37);
        border-radius: 10px
    }
</style>
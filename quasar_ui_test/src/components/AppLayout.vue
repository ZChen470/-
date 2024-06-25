<template>
    <q-layout view="hHh LpR fFf">
  
      <q-header elevated class="bg-cyan-8 text-white" height-hint="98">
        
        <q-toolbar>
          <q-btn dense flat round icon="menu" @click="toggleLeftDrawer" />
  
          <q-toolbar-title class="text-h4">
            <q-avatar>
              <img src="https://cdn.quasar.dev/logo-v2/svg/logo-mono-white.svg">
            </q-avatar>
            Hoshino Ai
          </q-toolbar-title>
          <q-btn flat round dense :icon="theme" @click="toggleTheme" />
          
        </q-toolbar>
        <q-tabs class="text-h5" align="left" v-model="tab">
            <!-- <q-route-tab to="/page1" label="Page One" /> -->
            <!-- <q-tab name="Form" label="Form" /> -->
            <!-- <q-tab name="Table" label="Table" /> -->
            <q-tab  name="Form" icon="fa-galaxy" label="主页" />
            <q-tab  name="File" icon="fa-galaxy" label="星系分类" />
        </q-tabs>
        
      </q-header>
  
      <!-- <q-drawer show-if-above v-model="leftDrawerOpen" side="left" behavior="desktop" bordered>
      </q-drawer> -->
  
      <q-page-container>
        <KeepAlive>
          <component :is="tabs[tab]"></component>
        </KeepAlive>
      </q-page-container>
  
    </q-layout>
  </template>
  
<script setup name="AppLayout">
    import { ref } from 'vue'
    import AppHome from './AppHome.vue'
    import AppTable from './AppTable.vue'
    import AppFile from './AppGalaxy.vue'

    import { useQuasar } from 'quasar'

    const $q = useQuasar()

    const leftDrawerOpen = ref(false)
    const toggleLeftDrawer = () => {
      leftDrawerOpen.value = !leftDrawerOpen.value
    }

    const tab = ref("Home")
    const tabs = {
      Home: AppHome,
      Table: AppTable,
      File: AppFile,
    }

    const theme = ref("light_mode")
    const toggleTheme = () => {
      theme.value = theme.value === "light_mode" ? "dark_mode" : "light_mode"

      $q.dark.toggle()
    }
</script>

<style scoped>
</style>
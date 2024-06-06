<template>
    <q-drawer
        show-if-above
        :width="180"
        :breakpoint="500"
        bordered
        elevated
        class="drawer-container"
      >
        <q-scroll-area class="fit">
          <q-list>

            <template v-for="(menuItem, index) in menuList" :key="index">
              <q-item clickable 
              :active="menuItem.label === actLabel" 
              @click="actLabel=menuItem.label" 
              :to="{path: menuItem.router}"
              v-ripple>
                <q-item-section avatar>
                  <q-icon :name="menuItem.icon" />
                </q-item-section>
                <q-item-section>
                  {{ menuItem.label }}
                </q-item-section>
              </q-item>
              <q-separator :key="'sep' + index"  v-if="menuItem.separator" />
            </template>

          </q-list>
        </q-scroll-area>
      </q-drawer>

       <!-- 这是页面被注入的地方 -->
      <div class="container">
        <router-view></router-view>
      </div>
</template>

<script setup lang="ts" name="GalaxyNav">
  import { ref, onMounted } from 'vue'
    const menuList = [
            {
                icon: 'image',
                label: '单图像',
                router: 'GalSPic',
                separator: false
            },
            {
                icon: 'add_photo_alternate',
                label: '多图像',
                router: 'GalMPic',
                separator: true
            },
            {
                icon: 'location_pin',
                label: '单坐标',
                router: 'GalSCoo',
                separator: false
            },
            {
                icon: 'add_location_alt',
                label: '多坐标',
                router: 'GalMCoo',
                separator: true
            }
        ]
    let actLabel = ref('')

    // 确保在组件挂载后设置激活状态
    onMounted(() => {
        actLabel.value = '单图像'
    })

</script>

<style scoped>
  .container {
    margin-top: 90px;
    margin-left: 100px;
  }
</style>
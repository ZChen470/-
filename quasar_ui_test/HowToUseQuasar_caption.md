# 一、快速上手
使用Quasar有多种选择，这里选择使用Vue的vite插件
先创建Vue应用  
然后安装quasar  
npm install quasar @quasar/extras (extras 为了使用图标)  
https://quasar.dev/start/vite-plugin  
删掉自带的样式文件  
在main.js里导入（关闭sass） 
``` typescript
const app = createApp(App)  
import {Quasar} from "quasar"  
app.use(Quasar, {})  
```
粘贴导入css文件  

components下创建AppLayout.vue  
粘贴导出的模板  
### 带有router的标签在没有安装vue-router时无法使用，同时to属性也是多余的


q-tabs的event需要v-model绑定，否则无法切换  
此外模板没有使用setup  
`const tab = ref("Form")` 初始为表单  
`q-tabs v-model="tab"`  
tab的value是q-tabs中间的q-tab的name属性,name="Form" 同时 label="Form"  

完成后，在q-page-container中添加内容  
使用的是`<router-view>`  
换成动态组件：  
```html
<KeepAlive>
    <component :is="tab">
    </component>
</KeepAlive>
```
接下来：  
例如要添加一个AppForm：  
components下创建Form.vue  
在相应的组件部分view source 复制，粘贴导出的代码，并在`<script>`中绑定变量  
`const text = ref("")`
再添加一个Table：  
components下创建Table.vue  
粘贴导出(Markup Table)的代码，并`<script>`中绑定变量  
`const text = ref("")`  

接下来：  
在Layout.vue创建常量  
```
const tabs = {
    Form: AppForm,
    Table: AppTable,
}
```
修改  
```html
<KeepAlive>
    <component :is="tabs[tab]">
    </component>
</KeepAlive>
```

# 二、风格和特性
在style&identity下有各种quasar已经写好的样式（css类），直接在标签中使用class='xxx'即可
- Typography 排版相关
- Color Palette 颜色 text-xxx bg-xxx(颜色名)
- Theme Builder 主题生成器 选好之后点击 EXPORT Vite模式在app.use中修改
- Spacing 间距 q-mx-xx q-px-xx q-mt-sm mt表示顶部外边距为小
- Breakpoints 断点，配合设备的尺寸设置样式，打开：quasar.config.js> framework> cssAddon: true 例子：q-mx-sm-sm
- Positioning 定位

# 三、Flex布局
```css
display: flex;
<!-- 方向 默认 row -->
flex-direction: row\column\row-reverse\column-reverse;
<!-- 横向 对齐 -->
justify-content: flex-start\flex-end\center\space-between\space-around\space-evenly;
<!-- 垂直反向 对齐 -->
align-items: flex-start\flex-end\center\baseline\stretch;
```
### Quasar内部css类
- flex 普通
- row  横
- column 纵
对齐
- justify-center
- justify-around
- justify-evenly
- items-center
- ...

### 栅格(Grid)系统
col-x offset-x 占x列，并且向右偏移x列（设置空隙）
断点模式：offset-md-4 中等屏幕偏移4列 offset-sm-1 小屏幕偏移1列
在父元素上class添加：
q-gutter-sm 子元素上左方外边距
q-col-gutter-md 子元素上左方内边距

### Flex Playground
flex布局效果快速预览

# 四、布局生成器Layout Builder
九宫格布局: 用字母l、h、f、p表示当前的格子属于header drawer footer page  
大写表示flex布局  
`<q-layout>`属性view="hHh LpR fFf"
* Header Reveal 滚动到顶部是否消失
* Overlay mode 抽屉是否覆盖在页面上
* Behavior 桌面还是移动端显示方式
* Separate type 分割线
### 布局的组成
```html
1.
<q-header></q-header>
Model: model-view:Boolean 控制显示隐藏
Style：border elevated 边框和阴影
2.
<q-footer></q-footer> 类似

3.
<q-drawer></q-drawer>
Behavior:
Model:显示
Style:一些样式

4.
<q-page></q-page> 
padding 加上内边距
q-page-container 包裹 router-view
```
# 五、quasar.config.js
(略)

# 六、Router
router>index.ts
router>routes.ts

# 七、Icon
<q-icon name="..."></q-icon>
content: 
* tag: 指定图标渲染在哪个标签 默认`<i>`
* left: 右边是否有padding以及margin :left="true" 或者直接 left
style: size="..." color="..."

# 八、组件 Components
### 1. QBtn
- props
  - Style
    * push \ :push="true"
    * flat \ :flat="true"
    * outline \ :outline="true"
    * rounded \ :rounded="true" 圆角
    * round \ :round="true" 圆形
    * size
    * color
    * text-color
    * dense 紧凑
    * ripple 点击效果 涟漪特效
  - State&Behavior
    * loading 等待状态 需要绑定一个动态数据 :loading="isloading"
    * percentage 进度条 比如上传时 :perentage="percent"
  - Navigation
    * to 路由跳转 to="/path"
    * replace 和Vue Router `<router-link>`相同
    * href 浏览器页面跳转
    * target _blank 新建标签页
- Slots Vue的插槽
  * default 默认插槽 `<q-btn>按钮的文本</q-btn>`
  * loading v-slot:loading（简写 #loading） `<q-spinner></q-spinner>` 组件 自定义loading 默认是转圈
- Events  监听事件 点击 @click
- Methods 通过DOM调用，而不是直接点击 属性`ref='myBtn'`
  ```typescript
    hClick() {
        const dom = this.$refs.myBtn
        dom.click()
    }
  ``` 
### 其他组件都是差不多的用法，一个组件可能有多个子组件搭配起来使用
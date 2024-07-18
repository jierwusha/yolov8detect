<template>
  <div id="app" style="padding: 0;margin: 0;">
    <app-header @menuSelect="handleMenuSelect"></app-header>
    <app-content :selectedMenu="selectedMenu"   v-if="selectedMenu==2"></app-content>
	<app-contentVideo :selectedMenu="selectedMenu"  v-if="selectedMenu==3"></app-contentVideo>
	<app-detect :selectedMenu="selectedMenu"  v-if="selectedMenu==4"></app-detect>
    <app-footer></app-footer>
  </div>
</template>

<script>
import Header from "./components/Header";
import Footer from "./components/Footer";
import Content from "./components/Content";
import ContentVideo from "./components/ContentVideo";
import Detect from "./components/detect";
export default {
  name: "Aminos智慧识别",
  data() {
    return {
      selectedMenu: "1", // 初始化选中的菜单项
    };
  },
  components: {
    "app-header": Header,
    "app-footer": Footer,
    "app-content": Content,
	"app-contentVideo": ContentVideo,
	"app-detect": Detect,
  },
  methods: {
    handleMenuSelect(index) {
      this.selectedMenu = index;
    },
  },
};
</script>

<style scope="this api replaced by slot-scope in 2.5.0+">
</style>

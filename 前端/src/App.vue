<template>
  <div id="app" style="padding: 0;margin: 0;">
    <app-header @menuSelect="handleMenuSelect"></app-header>
    <app-content :selectedMenu="selectedMenu"></app-content>
    <app-footer></app-footer>
  </div>
</template>

<script>
import Header from "./components/Header";
import Footer from "./components/Footer";
import Content from "./components/Content";
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

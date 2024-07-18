<template>
	<div id="app" style="padding: 0;margin: 0;">
		<app-header @menuSelect="handleMenuSelect"></app-header>
		<main1 :selectedMenu="selectedMenu" v-if="selectedMenu==1"></main1>
		<app-content :selectedMenu="selectedMenu" v-if="selectedMenu==2"></app-content>
		<app-contentVideo :selectedMenu="selectedMenu" v-if="selectedMenu==3||selectedMenu==4"></app-contentVideo>
		<app-footer></app-footer>
	</div>
</template>

<script>
	import Header from "./components/Header";
	import Footer from "./components/Footer";
	import Content from "./components/Content";
	import ContentVideo from "./components/ContentVideo";
	import main from "./components/main";
	import {
		EventBus
	} from './eventBus.js';

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
			"main1": main,


		},
		methods: {
			handleMenuSelect(index) {
				console.log('receive'+index);
				this.selectedMenu = index;
			},
		},
		mounted() {
			EventBus.$on('boxSelect', this.handleMenuSelect);
		},
		beforeDestroy() {
			EventBus.$off('boxSelect', this.handleMenuSelect);
		},
	};
</script>

<style scope="this api replaced by slot-scope in 2.5.0+">
</style>
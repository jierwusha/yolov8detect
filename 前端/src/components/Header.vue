<template>
	<div id="">



		<div style="
		position: fixed;z-index: 9;
		top: 0;
		background-color: white;
		color: #21b3b9; font-weight: bold
		font-size: 50px;display: flex; 
		justify-content: center; align-items:center;
		overflow: hidden;width: 100%;
		 
		 margin-bottom: 2vh;padding-bottom: 5px;
		 box-shadow: 0px 2px 20px 0 rgba(127, 255, 212, 0.5);
		 box-sizing: border-box;max-height: 10vh;">
			<div style="flex: 1;display: flex;align-items: center;padding-left: 2px;">
				<img id="icon" v-if="sidebarHidden==true" src="../assets/icon-more.png"
					style="height: 40px; width: 40px; padding: 10px;" @click="toggleSidebar">
				<img id="icon" v-if="sidebarHidden==false" src="../assets/icon-back.png"
					style="height: 40px; width: 40px; padding: 10px;" @click="toggleSidebar">
				<img id="myImage" src="../assets/aminuo2.png" alt="" style="height: 50px; width: 50px;"
					@click="toggleSidebar">
				<div style="color: #21b3b9; font-weight: bold; font-size: 50px;">AMINOS</div>
			</div>

			<div style="flex: 1;">
				<div style="color: #21b3b9; font-weight: bold; font-size: 35px; margin: 0 auto;text-align: center;">
					{{ msg }}
				</div>
			</div>

			<div style="flex: 1;"></div>
		</div>
		<div class="sidebar" :class="{ 'sidebar-hidden': sidebarHidden }">
			<el-menu :default-active="activeMenu" class="side-nav" @select="handleMenuSelect">
				<el-menu-item index="1">首页</el-menu-item>
				<el-menu-item index="2">验证码识别</el-menu-item>
				<el-menu-item index="3">车牌识别</el-menu-item>
				<el-menu-item index="4">人物识别</el-menu-item>
			</el-menu>

		</div>


	</div>

</template>
<script>
	import {
		EventBus
	} from '../eventBus.js';
	
	export default {
		name: "Header",
		data() {
			return {
				msg: "",
				activeMenu: '1',
				sidebarHidden: true, // 控制侧边栏的显示和隐藏
				rotated: false,
				iconSrc: '../assets/icon-more.png',
			};
		},
		methods: {
			toggleSidebar() {
				this.sidebarHidden = !this.sidebarHidden;

				// 获取图片元素
				var image = document.getElementById('myImage');
				// image.style.transform = 'rotate(180deg)';
				// 添加点击事件处理程序

				if (!this.rotated) {
					image.style.transform = 'rotate(360deg)';
					this.rotated = true;
				} else {
					image.style.transform = 'rotate(0deg)';
					this.rotated = false
				}
				this.$emit('sidebarToggle');
			},
			handleMenuSelect(index) {
				this.activeMenu = index;
				this.$emit("menuSelect", index);
				if (index == 1) {
					this.msg = ""
				}
				if (index == 2) {
					this.msg = "YOLOv8-验证码识别"
				}
				if (index == 3) {
					this.msg = "YOLOv8-车牌识别统计"
				}
				if (index == 4) {
					this.msg = "YOLOv8-人物识别"
				}
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
<style scoped>
	#myImage {
		transition: transform 0.3s ease;
	}

	#icon {
		/* transition: transform 0.3s; */
	}

	.sidebar {
		width: 200px;
		position: fixed;
		top: 10vh;
		left: 0;
		bottom: 0;
		background-color: #f0f0f0;
		transition: transform 0.3s;
		z-index: 10;
	}

	.sidebar-hidden {
		transform: translateX(-200px);
	}

	.toggle-btn {
		position: fixed;
		top: 20px;
		left: 20px;
		z-index: 9;
		width: 40px;
		height: 40px;
		border-radius: 50%;
		background-color: #f0f0f0;
		border: none;
		outline: none;
		cursor: pointer;
		transition: transform 0.3s;
	}

	.sidebar-hidden .toggle-btn {
		transform: translateX(-200px);
	}
</style>
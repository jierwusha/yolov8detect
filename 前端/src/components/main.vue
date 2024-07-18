<template>
	<!-- <div class="test" style="margin-top: 50vh;">
   	  <span >5555</span>
   </div> -->
	<div class="main" ref="container">
		<h1 class="index-text">YOLOv8目标识别</h1>
		<div class="navs">
			<div class="video-region" @click="triggerBoxSelect(2)">
				<!-- <video ref="video2" class="background-video" loop muted>
					<source src="../assets/license.mp4" type="video/mp4">
				</video> -->
				<img src="../assets/captcha.jpg" alt="" class="background-video" />
				<div class="video-overlay">
					<p class="overlay-text">识别照片</p>
				</div>
			</div>
			<div class="video-region" @mouseover="playVideo('video2')" @mouseleave="pauseVideo('video2')"
				@click="triggerBoxSelect(3)">
				<video ref="video2" class="background-video" loop muted>
					<source src="../assets/license.mp4" type="video/mp4">
				</video>
				<div class="video-overlay">
					<p class="overlay-text">识别视频</p>
				</div>
			</div>
			<div class="video-region" @mouseover="playVideo('video1')" @mouseleave="pauseVideo('video1')"
				@click="triggerBoxSelect(4)">
				<video ref="video1" class="background-video" loop muted>
					<source src="../assets/cs2.mp4" type="video/mp4">
				</video>
				<div class="video-overlay">
					<p class="overlay-text">实时</p>
				</div>
			</div>



			<!-- <div class="video-region" @mouseover="playVideo('video1')" @mouseleave="pauseVideo('video1')">
				<video ref="video1" class="background-video" loop muted>
					<source src="C:\Users\YatHong\Downloads\cs2.mp4" type="video/mp4">
				</video>
			</div> -->
		</div>
	</div>

</template>
<script>
	import {
		EventBus
	} from '../eventBus.js';

	import {
		Select
	} from 'element-ui';
	export default {
		name: "main",
		data() {
			return {

			};
		},
		methods: {
			startGeneratingBoxes() {
				if (this.$refs.container) {
					setInterval(() => {
						this.generateBox();
					}, 100);
				} // 每1000毫秒生成一个方块  
			},
			generateBox() {
				const container = this.$refs.container;
				const box = document.createElement('div');
				box.className = 'blocks';

				// 随机大小  
				const size = Math.random() * 50 + 20; // 20到70px
				const radius = 0.15 * size;
				box.style.width = `${size}px`;
				box.style.height = `${size}px`;
				box.style.borderRadius = `${radius}px`
				box.style.zIndex = 0;
				// 初始位置设定在底部  
				box.style.position = 'absolute';
				box.style.bottom = '0';

				// 设置背景色
				
				box.style.backgroundColor = 'rgba(255, 255, 255, 0.7)';
				// 随机位置  
				if (this.$refs.container) {
					const left = Math.random() * (container.offsetWidth - size);
					box.style.left = `${left}px`;
				}
				// 随机旋转角度  
				const angle = Math.random() * 360;
				box.style.transform = `rotate(${angle}deg)`;
				if (this.$refs.container) {
					container.appendChild(box);
				}
				box.style.animation = 'moveToTop 1s ease-in-out';
				// 动画结束后移除方块  
				box.addEventListener('animationend', () => {
					container.removeChild(box);
				});
			},
			playVideo(videoRef) {
				setTimeout(() => {
					if (this.$refs[videoRef]) {
						this.$refs[videoRef].play();
					}
				}, 200); // 延迟0.2秒  
			},
			pauseVideo(videoRef) {
				setTimeout(() => {
					if (this.$refs[videoRef]) {
						this.$refs[videoRef].pause();
					}
				}, 200); // 延迟0.2秒  
			},
			triggerBoxSelect(index) {
				EventBus.$emit('boxSelect', index);
			},

		},
		mounted() {
			this.startGeneratingBoxes();
		},
	};
</script>
<style>
	.main {
		width: 100%;
		height: 100vh;
		/* position: relative; */
		background-image: linear-gradient(rgba(127, 255, 212, 1),
				white);
		display: flex;
		flex-direction: column;
	}

	.index-text {
		margin-top: 20vh;
		margin-bottom: 20px;
		font-size: 56px;
		text-align: center;
		font-weight: bold;
		color: rgba(255, 255, 255, 1.0);

		z-index: 2;
	}

	/* 	.blocks {
		width: 100px;
		height: 100px;
		border-radius: 15px;
		transform: rotate(45deg);
		background-color: white;
		position: absolute;
		animation: moveToTop 10s linear;
	} */
	@keyframes moveToTop {
		from {
			bottom: 0;
		}

		to {
			bottom: 100vh;
		}
	}

	.navs {
		display: flex;
		justify-content: space-between;
		margin-left: 12vw;
		margin-right: 12vw;
		z-index: 2;
	}

	.video-region {
		width: 32%;
		height: 300px;
		/* Adjust the height as needed */
		position: relative;
		overflow: hidden;
		border-radius: 15px;
		margin: 20px;
		transition: transform 0.5s ease-in-out;
	}

	.video-region:hover {
		transform: scale(1.1);
		/* 放大1.1倍 */
	}

	.background-video {
		position: absolute;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		object-fit: cover;
		/* Adjust as needed to fit the video properly */
	}

	.video-overlay {
		position: absolute;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		display: flex;
		justify-content: center;
		/* 水平居中 */
		align-items: center;
		/* 垂直居中 */
		background-color: rgba(54, 108, 100, 0.5);
		/* 白色半透明遮罩 */
	}

	.overlay-text {
		color: white;
		/* 文字颜色 */
		font-size: 36px;
		/* 文字大小 */
		text-align: center;
		/* 文字居中 */
		font-weight: bold;
		justify-content: center;
	}
</style>
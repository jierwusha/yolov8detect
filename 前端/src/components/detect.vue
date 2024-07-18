<template>
  <div id="Content">
    <div id="CT"  style="display: flex; ">
		<div class="setParam">  <!-- 参数配置框 -->
			<el-card class="setParam-card"> 
				<div style="font-weight: bold;color: #21B3B9;font-size: 20px;display: flex;align-items: center;justify-content: space-between;">
					参数配置
				</div>
				 <el-form style="max-height: 28vh; width: 55vw;">
				   <!-- 模式选择 -->
				   <div style="margin-top: 10px; width: 100%; display: flex; flex-direction: column; align-items: flex-start;">
				     <div style="width: 100%; display: flex; align-items: center;">
				       <div style="width: 7vw;">模式选择：</div>
				       <el-radio v-model="modelSelect" label="0" border size="small" @input="modelSelectChange">摄像头检测</el-radio>
				       <el-radio v-model="modelSelect" label="1" border size="small" @input="modelSelectChange">CS2屏幕检测</el-radio>
				     </div>
				     <div style="width: 100%; display: flex; align-items: center; margin-top: 10px;">
				       <div style="width: 7vw;">详细设置:</div>
				       <div style="display: flex; flex-wrap: wrap;">
				         
				         <el-radio v-if="modelSelect == 0" v-model="detailselect" label="0" border size="small">前置摄像头</el-radio>
				         <el-radio v-if="modelSelect == 0" v-model="detailselect" label="1" border size="small">网络摄像头</el-radio>				 
						 <el-radio v-if="modelSelect== 0" v-model="funcSelect" label="0" border size="small">验证码识别</el-radio>
						 <el-radio v-if="modelSelect == 0" v-model="funcSelect" label="1" border size="small">车牌识别</el-radio>
				         <el-radio v-if="modelSelect == 1" v-model="detailselect" label="0" border size="small">性能优先</el-radio>
				         <el-radio v-if="modelSelect == 1" v-model="detailselect" label="1" border size="small">质量优先</el-radio>
				       </div>
				     </div>
				   </div>
				 </el-form>
			</el-card>
		</div>
		
      <div id="CT_image"><!-- 上传图片框 -->
        <el-card id="CT_image_1"  class="box-card"  style=" border-radius: 8px; height: 360px;width: 60vw;margin-bottom: -30px;box-sizing: border-box;">
			<div>Tips：请保持摄像头或屏幕开启，若无网络摄像头可将手机连接至Windows</div>
		<div style="display: flex;justify-content: center; align-items: center; height: 40vh;">
			<div class="demo-image__preview1">
			  <div v-loading="loading" element-loading-text="上传中"  element-loading-spinner="el-icon-loading" >
			    
			      <div slot="error">
			        <div slot="placeholder" class="error">
			          <el-button  v-show="showbutton" type="primary" icon="el-icon-video-camera"   class="download_bt" v-on:click="activate" >
						<div >启用检测</div>
			          </el-button>
			        </div>
			      </div>
			    
			  </div>
			</div>
			</div>
        </el-card>
      </div>
  </div>
</div>
</template>

<script>
import axios from "axios";
import ScreenShot from "js-web-screen-shot";
export default {
  name: "Content",
  props: {
      selectedMenu: {
        type: String,
        default: "1" // 默认选中的菜单项索引
      }
  },
  data() {
    return {
		funcSelect:'0',
	  detailselect:'0',
	  modelSelect: '0',
      server_url: "http://127.0.0.1:5000/camera",
      activeName: "first",
      active: 0,
      centerDialogVisible: true,
      visible: false,
      loading: false,
      table: false,
      isNav: false,
      showbutton: true,
      percentage: 0,
      fullscreenLoading: false,
      opacitys: {
        opacity: 0,
      },
      dialogTableVisible: false,
	  screenShotHandler:'',
    };
  },
  created: function () {
    document.title = "Aminos智慧识别";
  },
 methods: {
	 
	 modelSelectChange(e){
		 this.modelSelect=e
	 },
	 activate(){
		const data = {
		key1:this.modelSelect,
		key2:this.detailselect,
		key3:this.funcSelect
		}	
		console.log(data)
		axios.post(this.server_url, data, {
		     headers: {
		       'Content-Type': 'application/json'
		     }
		   })
	 }
 },
 
 
 mounted() {
	  
 },
};
</script>

<style>
.el-button {
  padding: 12px 20px !important;
}

#hello p {
  font-size: 15px !important;
  /*line-height: 25px;*/
}

.n1 .el-step__description {
  padding-right: 20%;
  font-size: 14px;
  line-height: 20px;
  /* font-weight: 400; */
}
.el-slider__button {
  width: 10px !important;
  height: 10px !important;
  background-color: #FFFFFF;
  box-shadow: 0px 0px 4px 0px rgba(64,83,159,0.73);
  z-index: 0 !important;
}

</style>

<style scoped>
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

.dialog_info {
  margin: 20px auto;
}

.text {
  font-size: 14px;
}

.item {
  margin-bottom: 18px;
}

.clearfix:before,
.clearfix:after {
  display: table;
  content: "";
}

.clearfix:after {
  clear: both;
}

.box-card {
  width: 680px;
  height: 200px;
  border-radius: 8px;
  margin-top: -20px;
}

.divider {
  width: 50%;
}

#CT {
  display: flex;
  height: auto;
  width: 100%;
  flex-wrap: wrap;
  justify-content: center;
  align-items: center;
  margin: 0 auto;
  margin-right: 0px;
  max-width: 100vw;
}

#CT_image_1 {
  width: 90%;
  height: 40%;
  margin: 0px auto;
  padding: 0px auto;
/*  margin-right: 180px; */
  margin-bottom: 0px;
  border-radius: 4px;
  margin-top: -2vh;
}

#CT_image {
  margin-bottom: 60px;

  margin-top: 5px;
  max-width: 60vw;
}

.image_1 {
  width: 275px;
  height: 260px;
  background: #ffffff;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.img_info_1 {
  height: 30px;
  width: 275px;
  text-align: center;
  background-color: #21b3b9;
  line-height: 30px;
}

.demo-image__preview1 {
  width: 275px;
  height: 290px;

}

.demo-image__preview2 {
  width: 275px;
  height: 290px;


  /* background-color: green; */
}

.error {
  margin: 100px auto;
  width: 50%;
  padding: 10px;
  text-align: center;
}

.block-sidebar {
  position: fixed;
  display: none;
  left: 50%;
  margin-left: 600px;
  top: 350px;
  width: 60px;
  z-index: 99;
}

.block-sidebar .block-sidebar-item {
  font-size: 50px;
  color: lightblue;
  text-align: center;
  line-height: 50px;
  margin-bottom: 20px;
  cursor: pointer;
  display: block;
}

div {
  display: block;
}

.block-sidebar .block-sidebar-item:hover {
  color: #187aab;
}

.download_bt {
  padding: 10px 16px !important;
  display: flex;
}

#upfile {
  width: 104px;
  height: 45px;
  background-color: #187aab;
  color: #fff;
  text-align: center;
  line-height: 45px;
  border-radius: 3px;
  box-shadow: 0 0 2px 0 rgba(0, 0, 0, 0.1), 0 2px 2px 0 rgba(0, 0, 0, 0.2);
  color: #fff;
  font-family: "Source Sans Pro", Verdana, sans-serif;
  font-size: 0.875rem;
}

.file {
  width: 200px;
  height: 130px;
  position: absolute;
  left: -20px;
  top: 0;
  z-index: 1;
  -moz-opacity: 0;
  -ms-opacity: 0;
  -webkit-opacity: 0;
  opacity: 0; /*css属性&mdash;&mdash;opcity不透明度，取值0-1*/
  filter: alpha(opacity=0);
  cursor: pointer;
}

#upload {
  position: relative;
  margin: 0px 0px;
}

#Content {
  width: 85%;
  height: auto;
  background-color: #ffffff;
  margin: 15px auto;
  display: flex;
  min-width: 1200px;
  margin-top: 10vh;

}

.divider {
  background-color: #eaeaea !important;
  height: 2px !important;
  width: 100%;
  margin-bottom: 50px;
}

.divider_1 {
  background-color: #ffffff;
  height: 2px !important;
  width: 100%;
  margin-bottom: 20px;
  margin: 20px auto;
}

.steps {
  font-family: "lucida grande", "lucida sans unicode", lucida, helvetica,
    "Hiragino Sans GB", "Microsoft YaHei", "WenQuanYi Micro Hei", sans-serif;
  color: #21b3b9;
  text-align: center;
  margin: 15px auto;
  font-size: 20px;
  font-weight: bold;
  text-align: center;
}

.step_1 {
  /*color: #303133 !important;*/
  margin: 20px 26px;
}

#info_patient {
  margin-top: 10px;
  width: 60vw;
}


.setParam{
	height: auto;
	width: 60vw;
    margin-top: 2vh;
	
}
.setParam-card{
	border-radius: 8px;
	height: auto;
	width: 60vw;
	box-sizing: border-box;
	margin-top: 2vh;
	background-color: #f9f9f9;
}
.amislider{
	z-index: 0;
}

</style>



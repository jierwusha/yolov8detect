<template>
  <div id="Content">
    <el-dialog
      title="AI预测中"
      :visible.sync="dialogTableVisible"
      :show-close="false"
      :close-on-press-escape="false"
      :append-to-body="true"
      :close-on-click-modal="false"
      :center="true"
    >
      <el-progress :percentage="percentage"></el-progress>
      <span slot="footer" class="dialog-footer">请耐心等待约3秒钟</span>
    </el-dialog>

    <div id="CT"  style="display: flex; ">
		
		<div class="setParam">  <!-- 参数配置框 -->
			<el-card class="setParam-card"> 
				<div style="font-weight: bold;color: #21B3B9;font-size: 20px;display: flex;align-items: center;justify-content: space-between;">
					参数配置
					<el-switch
					  v-model="isBrief"
					  active-text="专家模式"
					  inactive-text="简洁模式">
					</el-switch>
				</div>
				 <el-form  style="max-height: 28vh;width: 55vw;" >
				     <div style="margin-top: 10px;width: 55vw;display: flex;height: 5vh;align-items: center;justify-content: flex-start;">
						 <div style="width: 7vw;">模式选择：</div>
<!-- 				       <el-radio v-model="modelSelect" label="1" border size="small" @input="modelSelectChange">照片模式</el-radio> -->
				       <el-radio v-model="modelSelect" label="1" border size="small" @input="modelSelectChange">视频模式</el-radio>
				     </div>
					 <transition name="el-zoom-in-top">
					         <div v-if="isBrief" style="display: flex;width: 55vw;align-items: center;justify-content: flex-start;height: 5vh" >
					             <div style="width: 7vw;">置信阈值：</div>
					             <el-slider v-model="value1" :step="10" :max="100" :min="10" style="width: 20vw;" class="amislider" > </el-slider>
					         </div>
					 </transition>
					<transition name="el-zoom-in-top">
					       <div v-if="isBrief" style="display: flex;width: 55vw;align-items: center;justify-content: flex-start;height: 5vh">
					           <div style="width: 7vw;">22222：</div>
					           <el-slider v-model="value1" :step="10" :max="100" :min="10" style="width: 20vw;" class="amislider"> </el-slider>
					       </div>
					</transition>
					<transition name="el-zoom-in-top">
					        <div v-if="isBrief" style="display: flex;width: 55vw;align-items: center;justify-content: flex-start;height: 5vh">
					            <div style="width: 7vw;">3333333：</div>
					            <el-slider v-model="value1" :step="10" :max="100" :min="10" style="width: 20vw;" class="amislider"> </el-slider>
					        </div>
					</transition>
				 </el-form>
			</el-card>
		</div>
		
      <div id="CT_image"><!-- 上传图片框 -->
        <el-card id="CT_image_1"  class="box-card"  style=" border-radius: 8px; height: 360px;width: 60vw;margin-bottom: -30px;box-sizing: border-box;">
		<div style="display: flex;justify-content: space-between;padding: 0 10vw;">
			<div class="demo-image__preview1">
			  <div v-loading="loading" element-loading-text="上传中"  element-loading-spinner="el-icon-loading" >
			    <el-image :src="url_1" class="image_1" :preview-src-list="srcList" style="border-radius: 3px 3px 0 0" >
			      <div slot="error">
			        <div slot="placeholder" class="error">
			          <el-button  v-show="showbutton" type="primary" icon="el-icon-upload"   class="download_bt" v-on:click="true_upload" >
						<div >上传视频</div>
						<input  ref="upload" style="display: none" name="file" accept="video/*" type="file" @change="update" />
			          </el-button>
			        </div>
			      </div>
			    </el-image>
			  </div>
			  <div class="img_info_1" style="border-radius: 0 0 5px 5px">
			    <span style="color: white; letter-spacing: 6px">原始素材</span>
			  </div>
			</div>
			<div class="demo-image__preview2">
			  <div  v-loading="loading"   element-loading-text="处理中,请耐心等待" element-loading-spinner="el-icon-loading">
			    <el-image  :src="url_2"  class="image_1" :preview-src-list="srcList1" style="border-radius: 3px 3px 0 0"  >
			      <div slot="error">
			        <div slot="placeholder" class="error">{{ wait_return }}</div>
			      </div>
			    </el-image>
			  </div>
			  <div class="img_info_1" style="border-radius: 0 0 5px 5px">
			    <span style="color: white; letter-spacing: 4px">检测结果</span>
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
	  modelSelect: '1',
	  value1:'',
	  value2:'',
	  value3:'',
	  isBrief:false,
      server_url: "http://127.0.0.1:5003",
      activeName: "first",
      active: 0,
      centerDialogVisible: true,
      url_1: "",
	  url_11: "",
	  url_111: "",
      url_2: "",
	  url_22: "",
	  url_222: "",
      textarea: "",
      srcList: [],
      srcList1: [],
      feature_list: [],
      feature_list_1: [],
      feat_list: [],
      url: "",
      visible: false,
      wait_return: "等待上传",
      wait_upload: "等待上传",
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
	true_upload() {
	  this.$refs.upload.click();
	 
	},
    true_upload2() {
      this.$refs.upload2.click();
    },
    next() {
      this.active++;
    },
    // 获得目标文件
    getObjectURL(file) {
      var url = null;
      if (window.createObjcectURL != undefined) {
        url = window.createOjcectURL(file);
      } else if (window.URL != undefined) {
        url = window.URL.createObjectURL(file);
      } else if (window.webkitURL != undefined) {
        url = window.webkitURL.createObjectURL(file);
      }
      return url;
    },
    // 上传文件
    update(e) {
      this.percentage = 0;
      this.dialogTableVisible = true;
      this.url_1 = "";
      this.url_2 = "";
      this.srcList = [];
      this.srcList1 = [];
      this.wait_return = "";
      this.wait_upload = "";
      this.feature_list = [];
      this.feat_list = [];
      this.fullscreenLoading = true;
      this.loading = true;
      this.showbutton = false;
      let file = e.target.files[0];
      this.url_1 = this.$options.methods.getObjectURL(file);
      let param = new FormData(); //创建form对象
      param.append("file", file, file.name); //通过append向form对象添加数据
      var timer = setInterval(() => {
        this.myFunc();
      }, 30);
      let config = {
        headers: { "Content-Type": "multipart/form-data" },
      }; //添加请求头
      axios
        .post(this.server_url + "/upload", param, config)
        .then((response) => {
          this.percentage = 100;
          clearInterval(timer);
          this.url_1 = response.data.image_url;
          this.srcList.push(this.url_1);
          this.url_2 = response.data.draw_url;
          this.srcList1.push(this.url_2);
          this.fullscreenLoading = false;
          this.loading = false;

          this.feat_list = Object.keys(response.data.image_info);

          for (var i = 0; i < this.feat_list.length; i++) {
            response.data.image_info[this.feat_list[i]][2] = this.feat_list[i];
            this.feature_list.push(response.data.image_info[this.feat_list[i]]);
          }

          this.feature_list.push(response.data.image_info);
          this.feature_list_1 = this.feature_list[0];
          this.dialogTableVisible = false;
          this.percentage = 0;
          this.notice1();
        });
    },
    myFunc() {
      if (this.percentage + 33 < 99) {
        this.percentage = this.percentage + 33;
      } else {
        this.percentage = 99;
      }
    },
    drawChart() {},
    notice1() {
      this.$notify({
        title: "预测成功",
        message: "点击图片可以查看大图",
        duration: 0,
        type: "success",
      });
    },
	takeScreenshot() {
	           new ScreenShot(
	                {
	                  // clickCutFullScreen:true,
	                  wrcWindowMode: true,
					  //enableWebRtc:false,
	                  completeCallback: ({base64, cutInfo}) => {
	                    console.log(base64, cutInfo);
	                  },
	                });
	},
	modelSelectChange(){
		this.url_1="";
		this.url_2="";
		this.showbutton=true;
		this.feature_list="";
		this.srcList = [];
		this.srcList1 = [];
		this.wait_return = "等待上传";
		this.wait_upload = "等待上传";
	},
	updateFolder(e) {
      this.folderUrl = "";
      this.loading = true;
      this.folderProcessed = false;

      let files = e.target.files;
      let param = new FormData();

      for (let i = 0; i < files.length; i++) {
        let file = files[i];
        param.append("files[]", file, file.name);
      }

      let config = {
        headers: { "Content-Type": "multipart/form-data" },
      };

      axios
        .post(this.server_url + "/uploadFolder", param, config)
        .then((response) => {
          this.folderUrl = response.data.folder_url;
          this.loading = false;
          this.folderProcessed = true;
        })
        .catch((error) => {
          console.error(error);
          this.loading = false;
          this.folderProcessed = false;
        });
    }
  },


  mounted() {
    this.drawChart();
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



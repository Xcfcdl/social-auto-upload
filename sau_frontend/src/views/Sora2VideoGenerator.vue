<template>
  <div class="sora2-video-generator">
    <div class="page-header">
      <h1>Sora2视频批量生产</h1>
      <p>通过AI生成高质量视频内容，支持批量生产和管理</p>
    </div>
    
    <el-card class="generator-card">
      <template #header>
        <div class="card-header">
          <el-icon><VideoPlay /></el-icon>
          <span>视频生成配置</span>
        </div>
      </template>
      
      <div class="form-container">
        <el-form :model="formData" :rules="rules" ref="formRef" label-width="120px">
          <el-form-item label="视频主题" prop="theme">
            <el-input
              v-model="formData.theme"
              type="textarea"
              :rows="4"
              placeholder="请输入视频主题描述，越详细生成效果越好"
              show-word-limit
              maxlength="1000"
            />
            <el-button 
              type="danger" 
              plain 
              size="small" 
              @click="clearTheme"
              class="clear-button"
            >
              <el-icon><Delete /></el-icon>
              清空
            </el-button>
          </el-form-item>
          
          <el-form-item label="生成数量" prop="count">
            <div class="count-control">
              <el-button 
                type="primary" 
                plain 
                icon="Minus" 
                @click="decrementCount"
                :disabled="formData.count <= 1"
              />
              <span class="count-display">{{ formData.count }}</span>
              <el-button 
                type="primary" 
                plain 
                icon="Plus" 
                @click="incrementCount"
                :disabled="formData.count >= 20"
              />
              <span class="count-tip">(1-20个视频)</span>
            </div>
          </el-form-item>
          
          <el-form-item label="视频时长">
            <el-radio-group v-model="formData.duration" size="large">
              <el-radio-button value="10">10秒</el-radio-button>
              <el-radio-button value="15">15秒</el-radio-button>
            </el-radio-group>
          </el-form-item>

          <el-form-item label="视频比例">
            <el-radio-group v-model="formData.aspectRatio" size="large">
              <el-radio-button value="16:9">横版 16:9</el-radio-button>
              <el-radio-button value="9:16">竖版 9:16</el-radio-button>
            </el-radio-group>
          </el-form-item>
          
          <el-form-item>
            <el-button 
              type="primary" 
              size="large" 
              :loading="sora2Store.scriptGenerationStatus.loading"
              @click="handleGenerate"
              class="generate-button"
            >
              <el-icon><MagicStick /></el-icon>
              开始生成视频
            </el-button>
          </el-form-item>
        </el-form>
      </div>
      
      <!-- 错误提示 -->
      <el-alert
        v-if="sora2Store.scriptGenerationStatus.error"
        type="error"
        :title="sora2Store.scriptGenerationStatus.error"
        show-icon
        closable
        @close="sora2Store.resetStatus"
      />
    </el-card>
    
    <!-- 任务状态表格 -->
    <el-card class="task-table-card">
      <template #header>
        <div class="card-header">
          <el-icon><DataLine /></el-icon>
          <span>任务状态列表</span>
          <el-button 
            type="primary" 
            plain 
            size="small" 
            @click="refreshTasks"
            :loading="refreshingTasks"
            class="refresh-button"
          >
            <el-icon><Refresh /></el-icon>
            刷新
          </el-button>
        </div>
      </template>
      
      <div class="table-container">
        <el-table 
          v-loading="loadingTasks" 
          :data="sora2Store.tasks" 
          style="width: 100%"
          @row-click="handleRowClick"
        >
          <el-table-column prop="taskId" label="任务ID" width="180" />
          <el-table-column prop="theme" label="视频主题" width="250">
            <template #default="scope">
              <el-tooltip :content="scope.row.theme" placement="top">
                <div class="theme-text">{{ scope.row.theme }}</div>
              </el-tooltip>
            </template>
          </el-table-column>
          <el-table-column prop="count" label="生成数量" width="100" />
          <el-table-column prop="status" label="状态" width="120">
            <template #default="scope">
              <el-tag 
                :type="getStatusType(scope.row.status)"
                effect="light"
              >
                {{ getStatusText(scope.row.status) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="progress" label="进度" width="120">
            <template #default="scope">
              <el-progress 
                v-if="scope.row.progress !== undefined"
                :percentage="scope.row.progress" 
                :status="getProgressStatus(scope.row.status)"
                type="line" 
                :stroke-width="8"
                :show-text="true"
              />
              <span v-else>-</span>
            </template>
          </el-table-column>
          <el-table-column prop="createdAt" label="创建时间" width="180">
            <template #default="scope">
              {{ formatDate(scope.row.createdAt) }}
            </template>
          </el-table-column>
          <el-table-column prop="completedAt" label="完成时间" width="180">
            <template #default="scope">
              {{ scope.row.completedAt ? formatDate(scope.row.completedAt) : '-' }}
            </template>
          </el-table-column>
          <el-table-column label="操作" width="150" fixed="right">
            <template #default="scope">
              <el-button 
                v-if="scope.row.status === 'completed'" 
                type="primary" 
                size="small"
                @click="handleDownload(scope.row)"
              >
                <el-icon><Download /></el-icon>
                下载
              </el-button>
              <el-button 
                v-else-if="['pending', 'processing'].includes(scope.row.status)"
                type="danger" 
                size="small"
                @click="handleCancel(scope.row)"
              >
                <el-icon><CloseBold /></el-icon>
                取消
              </el-button>
              <el-button 
                v-else
                type="info" 
                size="small"
                @click="viewTaskDetails(scope.row)"
              >
                <el-icon><InfoFilled /></el-icon>
                详情
              </el-button>
            </template>
          </el-table-column>
        </el-table>
        
        <!-- 空状态 -->
        <div v-if="!loadingTasks && sora2Store.tasks.length === 0" class="empty-state">
          <el-empty description="暂无任务数据" />
        </div>
      </div>
    </el-card>
    
    <!-- 任务详情对话框 -->
    <el-dialog 
      v-model="showTaskDetail"
      title="任务详情"
      width="70%"
      @close="closeTaskDetail"
    >
      <div v-if="selectedTask" class="task-detail">
        <el-descriptions :column="1" border>
          <el-descriptions-item label="任务ID">{{ selectedTask.taskId }}</el-descriptions-item>
          <el-descriptions-item label="视频主题">{{ selectedTask.theme }}</el-descriptions-item>
          <el-descriptions-item label="生成数量">{{ selectedTask.count }}</el-descriptions-item>
          <el-descriptions-item label="视频时长">{{ selectedTask.duration || '10' }}秒</el-descriptions-item>
          <el-descriptions-item label="视频比例">{{ selectedTask.aspectRatio || '16:9' }}</el-descriptions-item>
          <el-descriptions-item label="当前状态">
            <el-tag :type="getStatusType(selectedTask.status)" effect="light">
              {{ getStatusText(selectedTask.status) }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="进度">
            <el-progress 
              v-if="selectedTask.progress !== undefined"
              :percentage="selectedTask.progress" 
              :status="getProgressStatus(selectedTask.status)"
              type="line" 
              :stroke-width="10"
              :show-text="true"
            />
            <span v-else>-</span>
          </el-descriptions-item>
          <el-descriptions-item label="创建时间">{{ formatDate(selectedTask.createdAt) }}</el-descriptions-item>
          <el-descriptions-item label="完成时间">{{ selectedTask.completedAt ? formatDate(selectedTask.completedAt) : '-' }}</el-descriptions-item>
          <el-descriptions-item v-if="selectedTask.error" label="错误信息" class="error-message">
            {{ selectedTask.error }}
          </el-descriptions-item>
        </el-descriptions>
        
        <!-- 任务日志 -->
        <div class="task-logs">
          <h3>执行日志</h3>
          <div class="logs-container">
            <el-scrollbar height="300px">
              <div v-if="taskLogs.length > 0" class="log-item" v-for="(log, index) in taskLogs" :key="index">
                <span class="log-time">{{ log.time }}</span>
                <span class="log-content" :class="log.level">[{{ log.level }}] {{ log.message }}</span>
              </div>
              <div v-else class="empty-logs">暂无日志信息</div>
            </el-scrollbar>
          </div>
        </div>
        
        <!-- 生成的视频列表 -->
        <div v-if="selectedTask.status === 'completed' && selectedTask.videos" class="video-list">
          <h3>生成的视频</h3>
          <el-carousel :interval="0" type="card" height="200px">
            <el-carousel-item v-for="(video, index) in selectedTask.videos" :key="index">
              <div class="video-item">
                <video :src="video.url" controls :poster="video.thumbnail" style="max-width: 100%; max-height: 180px;"></video>
                <div class="video-info">
                  <p>{{ video.title }}</p>
                  <el-button type="primary" size="small" @click="downloadSingleVideo(video)">
                    <el-icon><Download /></el-icon>
                    下载
                  </el-button>
                </div>
              </div>
            </el-carousel-item>
          </el-carousel>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, onUnmounted, nextTick } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { 
  VideoPlay, Delete, MagicStick, DataLine, Refresh, 
  Download, CloseBold, InfoFilled
} from '@element-plus/icons-vue'
import { useSora2Store } from '@/stores/sora2'
import { sora2Api } from '@/api/sora2'

// 状态管理
const sora2Store = useSora2Store()

// 响应式数据
const formData = reactive({
  theme: '',
  count: 1,
  duration: '10',
  aspectRatio: '16:9'
})

const rules = {
  theme: [
    { required: true, message: '请输入视频主题', trigger: 'blur' },
    { min: 5, message: '主题描述至少5个字符', trigger: 'blur' }
  ],
  count: [
    { required: true, message: '请设置生成数量', trigger: 'change' },
    { type: 'number', min: 1, max: 20, message: '生成数量必须在1-20之间', trigger: 'change' }
  ]
}

const formRef = ref(null)
const loadingTasks = ref(false)
const refreshingTasks = ref(false)
const showTaskDetail = ref(false)
const selectedTask = ref(null)
const taskLogs = ref([])
const logsLoading = ref(false)

// 生命周期
onMounted(() => {
  loadTasks()
})

onUnmounted(() => {
  // 停止所有轮询
  sora2Store.stopAllPolling()
})

// 方法
const clearTheme = () => {
  formData.theme = ''
}

const incrementCount = () => {
  if (formData.count < 20) {
    formData.count++
  }
}

const decrementCount = () => {
  if (formData.count > 1) {
    formData.count--
  }
}

const handleGenerate = async () => {
  if (!formRef.value.validate()) {
    return
  }
  
  try {
    // 生成脚本
    const scriptData = await sora2Store.generateScript(formData.theme, formData.count)
    
    // 创建任务
    const taskData = {
      theme: formData.theme,
      count: formData.count,
      duration: formData.duration,
      aspectRatio: formData.aspectRatio,
      scripts: scriptData.scripts
    }
    
    const task = await sora2Store.createTask(taskData)
    
    // 开始轮询任务状态
    sora2Store.startTaskPolling(task.taskId)
    
    ElMessage.success('视频生成任务已创建，正在处理中...')
    
    // 清空表单
    formRef.value.resetFields()
  } catch (error) {
    console.error('生成视频失败:', error)
    // 添加明确的错误提示给用户
    ElMessage.error(`生成视频失败: ${error.message || '未知错误，请检查网络连接或后端服务'}`)
    
    // 如果store中存储了错误信息，也显示出来
    if (sora2Store.scriptGenerationStatus.error) {
      ElMessage.error(`脚本生成错误: ${sora2Store.scriptGenerationStatus.error}`)
    }
  }
}

const loadTasks = async () => {
  loadingTasks.value = true
  try {
    await sora2Store.fetchTasks()
    
    // 对进行中的任务开始轮询
    sora2Store.tasks.forEach(task => {
      if (['pending', 'processing'].includes(task.status)) {
        sora2Store.startTaskPolling(task.taskId)
      }
    })
  } catch (error) {
    ElMessage.error('加载任务列表失败')
  } finally {
    loadingTasks.value = false
  }
}

const refreshTasks = async () => {
  refreshingTasks.value = true
  try {
    await loadTasks()
    ElMessage.success('任务列表已刷新')
  } finally {
    refreshingTasks.value = false
  }
}

const handleRowClick = (row) => {
  viewTaskDetails(row)
}

const viewTaskDetails = async (task) => {
  selectedTask.value = task
  showTaskDetail.value = true
  
  // 加载任务日志
  await loadTaskLogs(task.taskId)
  
  // 如果任务正在处理中，开始轮询
  if (['pending', 'processing'].includes(task.status)) {
    sora2Store.startTaskPolling(task.taskId)
  }
}

const loadTaskLogs = async (taskId) => {
  logsLoading.value = true
  taskLogs.value = []
  try {
    const response = await sora2Api.getTaskLogs(taskId)
    taskLogs.value = response.data || []
  } catch (error) {
    console.error('加载任务日志失败:', error)
  } finally {
    logsLoading.value = false
  }
}

const handleDownload = (task) => {
  if (task.status === 'completed') {
    window.open(sora2Api.downloadVideo(task.taskId), '_blank')
  }
}

const downloadSingleVideo = (video) => {
  window.open(video.url, '_blank')
}

const handleCancel = async (task) => {
  try {
    await ElMessageBox.confirm(
      '确定要取消这个任务吗？',
      '取消任务',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    await sora2Store.cancelTask(task.taskId)
    ElMessage.success('任务已取消')
  } catch (error) {
    // 用户取消操作
  }
}

const closeTaskDetail = () => {
  selectedTask.value = null
  taskLogs.value = []
  showTaskDetail.value = false
}

// 工具函数
const getStatusType = (status) => {
  const statusMap = {
    pending: 'warning',
    processing: 'primary',
    completed: 'success',
    failed: 'danger',
    cancelled: 'info',
    partial_success: 'warning'
  }
  return statusMap[status] || 'info'
}

const getStatusText = (status) => {
  const statusMap = {
    pending: '排队中',
    processing: '处理中',
    completed: '已完成',
    failed: '失败',
    cancelled: '已取消',
    partial_success: '部分完成'
  }
  return statusMap[status] || status
}

const getProgressStatus = (status) => {
  if (status === 'completed') return 'success'
  if (status === 'failed') return 'exception'
  return 'active'
}

const formatDate = (timestamp) => {
  if (!timestamp) return ''
  const date = new Date(timestamp)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  })
}
</script>

<style lang="scss" scoped>
.sora2-video-generator {
  .page-header {
    margin-bottom: 24px;
    h1 {
      font-size: 24px;
      color: #303133;
      margin-bottom: 8px;
    }
    p {
      color: #606266;
      font-size: 14px;
    }
  }
  
  .generator-card {
    margin-bottom: 24px;
    
    .card-header {
      display: flex;
      align-items: center;
      gap: 8px;
      font-weight: bold;
      font-size: 16px;
    }
    
    .form-container {
      margin-top: 16px;
    }
    
    .clear-button {
      margin-top: 8px;
    }
    
    .count-control {
      display: flex;
      align-items: center;
      gap: 16px;
      
      .count-display {
        font-size: 18px;
        font-weight: bold;
        min-width: 40px;
        text-align: center;
      }
      
      .count-tip {
        color: #606266;
        font-size: 14px;
      }
    }
    
    .generate-button {
      width: 100%;
      padding: 12px;
      font-size: 16px;
      margin-top: 8px;
    }
  }
  
  .task-table-card {
    .card-header {
      display: flex;
      align-items: center;
      gap: 8px;
      font-weight: bold;
      font-size: 16px;
      justify-content: space-between;
      
      .refresh-button {
        margin-left: auto;
      }
    }
    
    .table-container {
      margin-top: 16px;
      
      .theme-text {
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
      }
      
      .empty-state {
        padding: 60px 0;
      }
    }
  }
  
  .task-detail {
    .el-descriptions__label {
      font-weight: bold;
    }
    
    .error-message {
      color: #f56c6c;
      background-color: #fef0f0;
      padding: 8px;
      border-radius: 4px;
    }
    
    .task-logs {
      margin-top: 24px;
      
      h3 {
        font-size: 16px;
        font-weight: bold;
        margin-bottom: 12px;
        color: #303133;
      }
      
      .logs-container {
        border: 1px solid #ebeef5;
        border-radius: 4px;
        padding: 12px;
        
        .log-item {
          margin-bottom: 8px;
          
          .log-time {
            color: #606266;
            font-size: 12px;
            margin-right: 8px;
          }
          
          .log-content {
            font-family: 'Courier New', monospace;
            
            &.INFO {
              color: #409eff;
            }
            
            &.ERROR {
              color: #f56c6c;
            }
            
            &.SUCCESS {
              color: #67c23a;
            }
            
            &.WARNING {
              color: #e6a23c;
            }
          }
        }
        
        .empty-logs {
          text-align: center;
          color: #606266;
          padding: 40px 0;
        }
      }
    }
    
    .video-list {
      margin-top: 24px;
      
      h3 {
        font-size: 16px;
        font-weight: bold;
        margin-bottom: 12px;
        color: #303133;
      }
      
      .video-item {
        text-align: center;
        
        .video-info {
          margin-top: 8px;
          
          p {
            margin-bottom: 8px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
          }
        }
      }
    }
  }
}
</style>
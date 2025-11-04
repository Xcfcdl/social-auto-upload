import { http } from '@/utils/request'

// Sora2视频生成相关API
export const sora2Api = {
  // 生成视频生产脚本
  generateScript(data) {
    return http.post('/sora2/generate-script', data)
  },
  
  // 提交视频生成任务
  submitVideoTask(data) {
    return http.post('/sora2/create-task', data)
  },
  
  // 查询任务状态
  getTaskStatus(taskId) {
    return http.get(`/sora2/task-status/${taskId}`)
  },
  
  // 获取任务列表
  getTaskList(params) {
    return http.get('/sora2/task-list', params)
  },
  
  // 取消任务
  cancelTask(taskId) {
    return http.post(`/sora2/cancel-task/${taskId}`)
  },
  
  // 获取任务日志
  getTaskLogs(taskId) {
    return http.get(`/sora2/task-logs/${taskId}`)
  },
  
  // 下载生成的视频
  downloadVideo(taskId) {
    return `${import.meta.env.VITE_API_BASE_URL || 'http://localhost:5409'}/sora2/download/${taskId}`
  }
}
import { defineStore } from 'pinia'
import { ref } from 'vue'
import { sora2Api } from '@/api/sora2'

export const useSora2Store = defineStore('sora2', () => {
  // 任务列表
  const tasks = ref([])
  
  // 当前任务状态
  const currentTaskStatus = ref({})
  
  // 生成脚本状态
  const scriptGenerationStatus = ref({
    loading: false,
    error: null,
    success: false
  })
  
  // 任务创建状态
  const taskCreationStatus = ref({
    loading: false,
    error: null,
    success: false
  })
  
  // 轮询状态
  const pollingTasks = ref(new Map())
  
  // 设置任务列表
  const setTasks = (taskList) => {
    tasks.value = taskList
  }
  
  // 添加新任务
  const addTask = (task) => {
    tasks.value.unshift(task)
  }
  
  // 更新任务状态
  const updateTaskStatus = (taskId, status) => {
    const index = tasks.value.findIndex(t => t.taskId === taskId)
    if (index > -1) {
      tasks.value[index] = { ...tasks.value[index], ...status }
    }
    
    if (currentTaskStatus.value.taskId === taskId) {
      currentTaskStatus.value = { ...currentTaskStatus.value, ...status }
    }
  }
  
  // 设置当前任务状态
  const setCurrentTaskStatus = (status) => {
    currentTaskStatus.value = status
  }
  
  // 生成视频脚本
  const generateScript = async (theme, count) => {
    scriptGenerationStatus.value.loading = true
    scriptGenerationStatus.value.error = null
    scriptGenerationStatus.value.success = false
    
    try {
      const response = await sora2Api.generateScript({ theme, count })
      scriptGenerationStatus.value.success = true
      return response.data
    } catch (error) {
      scriptGenerationStatus.value.error = error.message || '生成脚本失败'
      throw error
    } finally {
      scriptGenerationStatus.value.loading = false
    }
  }
  
  // 创建视频生成任务
  const createTask = async (taskData) => {
    taskCreationStatus.value.loading = true
    taskCreationStatus.value.error = null
    taskCreationStatus.value.success = false
    
    try {
      const response = await sora2Api.submitVideoTask(taskData)
      taskCreationStatus.value.success = true
      addTask(response.data)
      return response.data
    } catch (error) {
      taskCreationStatus.value.error = error.message || '创建任务失败'
      throw error
    } finally {
      taskCreationStatus.value.loading = false
    }
  }
  
  // 获取任务列表
  const fetchTasks = async () => {
    try {
      const response = await sora2Api.getTaskList()
      setTasks(response.data)
      return response.data
    } catch (error) {
      console.error('获取任务列表失败:', error)
      throw error
    }
  }
  
  // 获取任务状态
  const fetchTaskStatus = async (taskId) => {
    try {
      const response = await sora2Api.getTaskStatus(taskId)
      // 处理新的API响应格式
      const taskData = response.data
      // 确保前端store使用正确的字段名称
      const storeTaskData = {
        taskId: taskData.id,
        status: taskData.status,
        progress: taskData.progress,
        // 如果有result，提取videos
        videos: taskData.result?.videos || []
      }
      updateTaskStatus(taskId, storeTaskData)
      return taskData
    } catch (error) {
      console.error('获取任务状态失败:', error)
      throw error
    }
  }
  
  // 开始任务轮询
  const startTaskPolling = (taskId, interval = 5000) => {
    // 停止之前的轮询
    stopTaskPolling(taskId)
    
    const poll = async () => {
      try {
        await fetchTaskStatus(taskId)
      } catch (error) {
        console.error(`轮询任务 ${taskId} 状态失败:`, error)
      }
    }
    
    // 立即执行一次
    poll()
    
    // 设置定时器
    const timerId = setInterval(poll, interval)
    pollingTasks.value.set(taskId, timerId)
  }
  
  // 停止任务轮询
  const stopTaskPolling = (taskId) => {
    if (pollingTasks.value.has(taskId)) {
      clearInterval(pollingTasks.value.get(taskId))
      pollingTasks.value.delete(taskId)
    }
  }
  
  // 停止所有轮询
  const stopAllPolling = () => {
    pollingTasks.value.forEach((timerId) => {
      clearInterval(timerId)
    })
    pollingTasks.value.clear()
  }
  
  // 取消任务
  const cancelTask = async (taskId) => {
    try {
      await sora2Api.cancelTask(taskId)
      stopTaskPolling(taskId)
      updateTaskStatus(taskId, { status: 'cancelled' })
      return true
    } catch (error) {
      console.error('取消任务失败:', error)
      throw error
    }
  }
  
  // 重置状态
  const resetStatus = () => {
    scriptGenerationStatus.value = {
      loading: false,
      error: null,
      success: false
    }
    taskCreationStatus.value = {
      loading: false,
      error: null,
      success: false
    }
  }
  
  return {
    tasks,
    currentTaskStatus,
    scriptGenerationStatus,
    taskCreationStatus,
    setTasks,
    addTask,
    updateTaskStatus,
    setCurrentTaskStatus,
    generateScript,
    createTask,
    fetchTasks,
    fetchTaskStatus,
    startTaskPolling,
    stopTaskPolling,
    stopAllPolling,
    cancelTask,
    resetStatus
  }
})
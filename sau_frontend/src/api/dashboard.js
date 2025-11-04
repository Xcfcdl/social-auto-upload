import { http } from '@/utils/request'

// Dashboard统计数据API
export const dashboardApi = {
  // 获取Dashboard统计数据
  getStats() {
    return http.get('/dashboard/stats')
  }
}

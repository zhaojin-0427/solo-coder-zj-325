import axios from 'axios'
import { ElMessage } from 'element-plus'
import mockData from '@/mock/data'

const USE_MOCK = false

const request = axios.create({
  baseURL: '/api',
  timeout: 10000
})

request.interceptors.request.use(
  config => {
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

request.interceptors.response.use(
  response => {
    return response.data
  },
  error => {
    ElMessage.error(error.message || '请求失败')
    return Promise.reject(error)
  }
)

function mockRequest(method, url, data, params) {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve(mockData.handleRequest(method, url, data, params))
    }, 300)
  })
}

export function apiRequest(method, url, data = null, params = null) {
  if (USE_MOCK) {
    return mockRequest(method, url, data, params)
  }
  const config = { method, url }
  if (data) config.data = data
  if (params) config.params = params
  return request(config)
}

export default request

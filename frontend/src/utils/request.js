import axios from 'axios'

const request = axios.create({
  baseURL: '/api',
  timeout: 150000
})

request.interceptors.response.use(
  response => {
    if (response.config.responseType === 'blob') {
      return response
    }

    return response.data
  },
  error => Promise.reject(error)
)

export default request

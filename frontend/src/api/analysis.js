import axios from 'axios'

export function getAnalysisSummary() {
  return axios.get('http://127.0.0.1:8000/api/summary/')
}
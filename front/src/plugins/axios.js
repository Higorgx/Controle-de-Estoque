import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  }
})

export default {
  install: (app) => {
    // Disponibiliza globalmente como $api
    app.config.globalProperties.$api = api
    
    // Ou adiciona ao provide/inject
    app.provide('api', api)
  }
}
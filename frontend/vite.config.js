import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  base: './',   // 👈 关键就是这个
  plugins: [vue()]
})
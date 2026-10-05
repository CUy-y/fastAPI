import { defineStore } from 'pinia'
import axios from 'axios'
import { apiConfig } from '../../config/api'

export const useNewsStore = defineStore('news', {
  state: () => ({
    newsList: [],
    newsDetail: {},
    categories: [],
    currentCategory: 1,
    loading: false,
    refreshing: false,
    finished: false,
    categoriesLoading: false,
  }),

  actions: {
    async getCategories() {
      if (this.categoriesLoading) return
      this.categoriesLoading = true
      try {
        const { data } = await axios.get(`${apiConfig.baseURL}/api/news/categories`)
        if (data?.code !== 200) throw new Error(data?.message || '获取分类失败')

        this.categories = data.data || []
        if (!this.categories.some((item) => item.id === this.currentCategory)) {
          this.currentCategory = this.categories[0]?.id ?? null
        }
      } catch (error) {
        console.error('获取新闻分类失败:', error)
        this.categories = []
      } finally {
        this.categoriesLoading = false
      }
    },

    changeCategory(categoryId) {
      if (!categoryId || this.currentCategory === categoryId) return
      this.currentCategory = categoryId
      this.newsList = []
      this.finished = false
      this.getNewsList(true)
    },

    async getNewsList(isRefresh = false) {
      if (this.loading || (!this.currentCategory && this.currentCategory !== 0)) return
      if (isRefresh) {
        this.newsList = []
        this.finished = false
        this.refreshing = true
      }

      this.loading = true
      const page = isRefresh ? 1 : Math.floor(this.newsList.length / 10) + 1
      try {
        const { data } = await axios.get(`${apiConfig.baseURL}/api/news/list`, {
          params: { categoryId: this.currentCategory, page, pageSize: 10 },
        })
        if (data?.code !== 200) throw new Error(data?.message || '获取新闻失败')

        const pageData = data.data || { list: [], hasMore: false }
        const items = pageData.list || []
        this.newsList = isRefresh ? items : [...this.newsList, ...items]
        this.finished = !pageData.hasMore
      } catch (error) {
        console.error('获取新闻列表失败:', error)
        this.finished = true
      } finally {
        this.loading = false
        this.refreshing = false
      }
    },

    async getNewsDetail(id) {
      try {
        const { data } = await axios.get(`${apiConfig.baseURL}/api/news/detail`, {
          params: { id },
        })
        if (data?.code !== 200) throw new Error(data?.message || '获取新闻详情失败')
        this.newsDetail = data.data
        return data.data
      } catch (error) {
        console.error('获取新闻详情失败:', error)
        this.newsDetail = {}
        return null
      }
    },

    getCategoryName(categoryId) {
      return this.categories.find((item) => item.id === categoryId)?.name || '未知'
    },
  },
})

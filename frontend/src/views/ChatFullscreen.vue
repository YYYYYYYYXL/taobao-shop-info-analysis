<template>
  <div class="chat-page-fullscreen">
    <!-- 左侧边栏 -->
    <div class="chat-sidebar">
      <!-- Logo -->
      <div class="sidebar-logo">
        <div class="logo-icon">
          <img :src="logoImg" alt="Logo" />
        </div>
        <span class="logo-text">智能助手</span>
        <i class="el-icon-more-outline logo-menu" @click="showConfigDialog = true"></i>
      </div>

      <!-- 新对话按钮 -->
      <div class="new-chat-btn" @click="startNewChat">
        <i class="el-icon-plus"></i>
        <span>开启新对话</span>
        <span class="shortcut">Ctrl+J</span>
      </div>

      <!-- 历史对话列表 -->
      <div class="chat-history">
        <div class="history-title">历史对话</div>
        <div v-if="chatHistoryList.length === 0" class="no-history">
          <i class="el-icon-chat-dot-round"></i>
          <p>暂无历史对话</p>
        </div>
        <div v-else class="history-list">
          <div
            v-for="(item, index) in chatHistoryList"
            :key="index"
            class="history-item"
            :class="{ active: currentChatIndex === index }"
            @click="loadChatHistory(index)"
          >
            <i class="el-icon-chat-line-round"></i>
            <span class="history-title-text">{{ item.title || `对话 ${index + 1}` }}</span>
            <i class="el-icon-close history-delete" @click.stop="deleteHistory(index)"></i>
          </div>
        </div>
      </div>

      <!-- 用户信息 -->
      <div class="user-info">
        <div class="user-avatar">{{ userInitial }}</div>
        <span class="user-email">{{ userEmail }}</span>
      </div>
    </div>

    <!-- 主内容区域 -->
    <div class="chat-main">
      <!-- 消息区域 -->
      <div class="chat-messages" ref="messagesContainer">
        <!-- 欢迎消息 -->
        <div v-if="messages.length === 0" class="welcome-message">
          <div class="welcome-logo">
            <img :src="logoImg" alt="Logo" />
          </div>
          <h2 class="welcome-text">今天有什么可以帮到你?</h2>
        </div>

        <!-- 消息列表 -->
        <div
          v-for="(message, index) in messages"
          :key="index"
          :class="['message-item', message.role]"
        >
          <div v-if="message.role === 'assistant'" class="message-avatar assistant-avatar">
            <img :src="logoImg" alt="Logo" />
          </div>
          <div v-else class="message-avatar user-avatar">
            {{ userInitial }}
          </div>
          <div class="message-content">
            <div class="message-text" v-html="formatMessage(message.content)"></div>
          </div>
        </div>

        <!-- 加载中 -->
        <div v-if="isLoading" class="message-item assistant">
          <div class="message-avatar assistant-avatar">
            <img :src="logoImg" alt="Logo" />
          </div>
          <div class="message-content">
            <div class="loading-indicator">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        </div>
      </div>

      <!-- 输入区域 -->
      <div class="chat-input-container">
        <!-- 功能按钮 -->
        <div class="feature-buttons">
          <button
            class="feature-btn"
            :class="{ active: enableDeepThinking }"
            @click="enableDeepThinking = !enableDeepThinking"
          >
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
              <rect x="2" y="2" width="12" height="12" stroke="currentColor" stroke-width="1.5" fill="none" rx="1"/>
              <line x1="5" y1="5" x2="11" y2="11" stroke="currentColor" stroke-width="1.5"/>
            </svg>
            <span>深度思考</span>
          </button>
          <button
            class="feature-btn"
            :class="{ active: enableWebSearch }"
            @click="enableWebSearch = !enableWebSearch"
          >
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M8 1C4.13 1 1 4.13 1 8C1 11.87 4.13 15 8 15C11.87 15 15 11.87 15 8C15 4.13 11.87 1 8 1ZM8 14C4.69 14 2 11.31 2 8C2 4.69 4.69 2 8 2C11.31 2 14 4.69 14 8C14 11.31 11.31 14 8 14Z" fill="currentColor"/>
              <path d="M8 3C5.24 3 3 5.24 3 8C3 10.76 5.24 13 8 13C10.76 13 13 10.76 13 8C13 5.24 10.76 3 8 3ZM8 12C5.79 12 4 10.21 4 8C4 5.79 5.79 4 8 4C10.21 4 12 5.79 12 8C12 10.21 10.21 12 8 12Z" fill="currentColor"/>
              <path d="M5 2.5L5.5 1.5L6.5 2.5L5.5 3.5L5 2.5Z" fill="currentColor"/>
              <path d="M11 2.5L11.5 1.5L12.5 2.5L11.5 3.5L11 2.5Z" fill="currentColor"/>
              <path d="M14.5 6L13.5 5.5L14.5 4.5L15.5 5.5L14.5 6Z" fill="currentColor"/>
              <path d="M14.5 10L13.5 9.5L14.5 8.5L15.5 9.5L14.5 10Z" fill="currentColor"/>
              <path d="M11 13.5L11.5 12.5L12.5 13.5L11.5 14.5L11 13.5Z" fill="currentColor"/>
              <path d="M5 13.5L5.5 12.5L6.5 13.5L5.5 14.5L5 13.5Z" fill="currentColor"/>
              <path d="M2 6L1 5.5L2 4.5L3 5.5L2 6Z" fill="currentColor"/>
              <path d="M2 10L1 9.5L2 8.5L3 9.5L2 10Z" fill="currentColor"/>
            </svg>
            <span>联网搜索</span>
          </button>
        </div>

        <!-- 输入框 -->
        <div class="input-wrapper">
          <el-input
            v-model="inputMessage"
            type="textarea"
            :rows="1"
            placeholder="给 DeepSeek 发送消息"
            @keydown.ctrl.enter="sendMessage"
            @keydown.enter.exact.prevent="sendMessage"
            @keydown.ctrl.j.prevent="startNewChat"
            :disabled="isLoading"
            class="chat-input"
            autosize
            :autofocus="true"
          />
          <div class="input-actions">
            <i class="el-icon-paperclip input-icon"></i>
            <button
              class="send-btn"
              :disabled="!inputMessage.trim() || isLoading"
              @click="sendMessage"
            >
              <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                <path d="M2 10L18 2L10 18L8 10L2 10Z" fill="white"/>
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 配置弹窗 -->
    <el-dialog
      title="DeepSeek 配置"
      :visible.sync="showConfigDialog"
      width="500px"
      append-to-body
    >
      <el-form :model="config" label-width="120px">
        <el-form-item label="API 地址">
          <el-input disabled
            v-model="config.apiUrl"
            placeholder="https://api.deepseek.com/v1/chat/completions"
          />
        </el-form-item>
        <el-form-item label="API Key">
          <el-input
            v-model="config.apiKey"
            type="password"
            :show-password="true"
            placeholder="请输入 DeepSeek API Key"
          />
        </el-form-item>
        <el-form-item label="模型名称">
          <el-input disabled
            v-model="config.model"
            placeholder="deepseek-chat"
          />
        </el-form-item>
        <el-form-item label="温度参数">
          <el-slider
            v-model="config.temperature"
            :min="0"
            :max="2"
            :step="0.1"
            show-input
          />
        </el-form-item>
        <el-form-item label="最大令牌数">
          <el-input-number
            v-model="config.maxTokens"
            :min="1"
            :max="4096"
            :step="100"
          />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="showConfigDialog = false">取消</el-button>
        <el-button type="primary" @click="saveConfig">保存</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import logoImg from '@/assets/logo.png'
import { marked } from 'marked'
import DOMPurify from 'dompurify'
// import { hasInviteCode, isValidDate } from '@/utils/inviteCode'

export default {
  name: 'ChatFullscreen',
  data() {
    return {
      messages: [],
      inputMessage: '',
      isLoading: false,
      showConfigDialog: false,
      enableDeepThinking: false,
      enableWebSearch: false,
      chatHistoryList: [],
      currentChatIndex: -1,
      config: {
        apiUrl: 'https://api.deepseek.com/v1/chat/completions',
        apiKey: '',
        model: 'deepseek-chat',
        temperature: 0.7,
        maxTokens: 2048
      },
      userEmail: this.getUserEmail(),
      logoImg: logoImg
    }
  },
  computed: {
    userInitial() {
      if (this.userEmail) {
        return this.userEmail.charAt(0).toUpperCase()
      }
      return 'U'
    }
  },
  mounted() {
    // this.checkInviteCode()
    this.loadConfig()
    this.loadChatHistoryList()
    this.loadMessages()
    this.scrollToBottom()
  },
  methods: {
    /*
    checkInviteCode() {
      if (!isValidDate()) {
        this.$message.error('邀请日期已过期，无法使用系统')
        setTimeout(() => {
          this.$router.push('/login')
        }, 2000)
        return
      }
      
      if (!hasInviteCode()) {
        this.$message.warning('请先验证邀请码')
        setTimeout(() => {
          this.$router.push('/login')
        }, 2000)
        return
      }
    },
    */
    getUserEmail() {
      try {
        const userInfo = JSON.parse(localStorage.getItem('userInfo') || '{}')
        return userInfo.email || userInfo.username || '97*****17@qq.com'
      } catch (e) {
        return '97*****17@qq.com'
      }
    },
    // 开始新对话
    startNewChat() {
      if (this.messages.length > 0) {
        this.$confirm('确定要开始新对话吗？当前对话将被保存。', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'info'
        }).then(() => {
          this.saveCurrentChat()
          this.messages = []
          this.currentChatIndex = -1
          this.saveMessages()
          this.scrollToBottom()
        }).catch(() => {})
      }
    },
    // 保存当前对话
    saveCurrentChat() {
      if (this.messages.length > 0) {
        // 如果当前对话已经在历史记录中，更新它而不是添加新的
        if (this.currentChatIndex >= 0 && this.currentChatIndex < this.chatHistoryList.length) {
          this.chatHistoryList[this.currentChatIndex].messages = [...this.messages]
          this.chatHistoryList[this.currentChatIndex].timestamp = new Date()
        } else {
          // 如果是一个新对话，添加到历史记录中
          const title = this.messages[0]?.content?.substring(0, 20) || `对话 ${this.chatHistoryList.length + 1}`
          const chatItem = {
            title,
            messages: [...this.messages],
            timestamp: new Date()
          }
          this.chatHistoryList.push(chatItem)
        }
        this.saveChatHistoryList()
      }
    },
    // 加载历史对话
    loadChatHistory(index) {
      if (this.currentChatIndex === index) {
        return
      }
      
      if (this.messages.length > 0 && this.currentChatIndex !== -1) {
        this.chatHistoryList[this.currentChatIndex].messages = [...this.messages]
        this.saveChatHistoryList()
      }
      
      this.currentChatIndex = index
      this.messages = [...this.chatHistoryList[index].messages]
      this.saveMessages()
      this.scrollToBottom()
    },
    // 删除历史对话
    deleteHistory(index) {
      this.$confirm('确定要删除这条对话吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.chatHistoryList.splice(index, 1)
        if (this.currentChatIndex === index) {
          this.currentChatIndex = -1
          this.messages = []
        } else if (this.currentChatIndex > index) {
          this.currentChatIndex--
        }
        this.saveChatHistoryList()
        this.saveMessages()
      }).catch(() => {})
    },
    // 保存对话历史列表
    saveChatHistoryList() {
      localStorage.setItem('chat-history-list', JSON.stringify(this.chatHistoryList))
    },
    // 加载对话历史列表
    loadChatHistoryList() {
      const saved = localStorage.getItem('chat-history-list')
      if (saved) {
        try {
          this.chatHistoryList = JSON.parse(saved)
        } catch (e) {
          console.error('加载对话历史失败:', e)
        }
      }
    },
    // 发送消息
    async sendMessage() {
      if (!this.inputMessage.trim() || this.isLoading) return

      const userMessage = {
        role: 'user',
        content: this.inputMessage.trim(),
        timestamp: new Date()
      }

      this.messages.push(userMessage)
      this.saveMessages()
      const messageText = this.inputMessage.trim()
      this.inputMessage = ''
      this.scrollToBottom()

      // 检查配置 - 如果没有 API key，返回固定提示消息
      if (!this.config.apiKey || this.config.apiKey.trim() === '') {
        const fixedMessage = {
          role: 'assistant',
          content: '智能助手是付费功能，请联系最强大神qq: 971118017',
          timestamp: new Date()
        }
        this.messages.push(fixedMessage)
        this.saveMessages()
        this.scrollToBottom()
        
        // 如果是第一条消息，保存到历史记录
        if (this.messages.length === 2 && this.currentChatIndex === -1) {
          const title = messageText.substring(0, 20)
          this.chatHistoryList.unshift({
            title,
            messages: [...this.messages],
            timestamp: new Date()
          })
          this.currentChatIndex = 0
          this.saveChatHistoryList()
        } else if (this.currentChatIndex >= 0) {
          // 更新当前历史记录
          this.chatHistoryList[this.currentChatIndex].messages = [...this.messages]
          this.saveChatHistoryList()
        }
        return
      }

      this.isLoading = true

      try {
        const response = await this.callDeepSeekAPI(userMessage)

        const assistantMessage = {
          role: 'assistant',
          content: response.content || '抱歉，无法获取回答',
          timestamp: new Date()
        }

        this.messages.push(assistantMessage)
        this.saveMessages()
        this.scrollToBottom()
        
        // 如果是第一条消息，保存到历史记录
        if (this.messages.length === 2 && this.currentChatIndex === -1) {
          const title = messageText.substring(0, 20)
          this.chatHistoryList.unshift({
            title,
            messages: [...this.messages],
            timestamp: new Date()
          })
          this.currentChatIndex = 0
          this.saveChatHistoryList()
        } else if (this.currentChatIndex >= 0) {
          // 更新当前历史记录
          this.chatHistoryList[this.currentChatIndex].messages = [...this.messages]
          this.saveChatHistoryList()
        }
      } catch (error) {
        console.error('API调用失败:', error)
        const errorMessage = {
          role: 'assistant',
          content: error.message || '请求失败，请检查配置或网络连接',
          timestamp: new Date()
        }
        this.messages.push(errorMessage)
        this.saveMessages()
        this.scrollToBottom()
        this.$message.error(error.message || '请求失败')
      } finally {
        this.isLoading = false
      }
    },

    // 调用 DeepSeek API
    async callDeepSeekAPI(userMessage) {
      const messagesHistory = [
        ...this.messages.map(msg => ({
          role: msg.role,
          content: msg.content
        })),
        {
          role: userMessage.role,
          content: userMessage.content
        }
      ]

      const response = await fetch(this.config.apiUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.config.apiKey}`
        },
        body: JSON.stringify({
          model: this.config.model,
          messages: messagesHistory,
          temperature: this.config.temperature,
          max_tokens: this.config.maxTokens
        })
      })

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))
        throw new Error(errorData.error?.message || `HTTP error! status: ${response.status}`)
      }

      const data = await response.json()
      return {
        content: data.choices[0].message.content
      }
    },

    // 格式化消息内容 - 使用 Markdown 语法
    formatMessage(content) {
      if (!content) return ''
      
      try {
        // 使用 marked 解析 Markdown
        const html = marked(content, {
          breaks: true, // 支持换行符
          gfm: true, // 支持 GitHub Flavored Markdown
          headerIds: false, // 不生成 header ID
          mangle: false
        })
        
        // 使用 DOMPurify 清理 HTML 以确保安全
        return DOMPurify.sanitize(html, {
          ALLOWED_TAGS: [
            'p', 'br', 'strong', 'em', 'u', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
            'ul', 'ol', 'li', 'blockquote', 'code', 'pre', 'a', 'img',
            'table', 'thead', 'tbody', 'tr', 'th', 'td', 'hr', 'del'
          ],
          ALLOWED_ATTR: ['href', 'src', 'alt', 'title', 'target', 'class']
        })
      } catch (error) {
        console.error('Markdown 解析失败:', error)
        // 如果解析失败，返回原始内容
        return content.replace(/\n/g, '<br>')
      }
    },

    // 滚动到底部
    scrollToBottom() {
      this.$nextTick(() => {
        const container = this.$refs.messagesContainer
        if (container) {
          container.scrollTop = container.scrollHeight
        }
      })
    },

    // 保存配置
    saveConfig() {
      localStorage.setItem('deepseek-config', JSON.stringify(this.config))
      this.showConfigDialog = false
      this.$message.success('配置已保存')
    },

    // 加载配置
    loadConfig() {
      const saved = localStorage.getItem('deepseek-config')
      if (saved) {
        try {
          this.config = { ...this.config, ...JSON.parse(saved) }
        } catch (e) {
          console.error('加载配置失败:', e)
        }
      }
    },

    // 保存消息
    saveMessages() {
      localStorage.setItem('chat-messages', JSON.stringify(this.messages))
    },

    // 加载消息
    loadMessages() {
      const saved = localStorage.getItem('chat-messages')
      if (saved) {
        try {
          this.messages = JSON.parse(saved)
          this.scrollToBottom()
        } catch (e) {
          console.error('加载消息失败:', e)
        }
      }
    }
  }
}
</script>

<style lang="less" scoped>
.chat-page-fullscreen {
  width: 100vw;
  height: 100vh;
  background: #ffffff;
  display: flex;
  margin: 0;
  padding: 0;
  overflow: hidden;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif;
}

/* 左侧边栏 */
.chat-sidebar {
  width: 280px;
  height: 100vh;
  background: #ffffff;
  border-right: 1px solid #e5e7eb;
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
}

.sidebar-logo {
  padding: 20px 16px;
  display: flex;
  align-items: center;
  gap: 8px;
  border-bottom: 1px solid #f3f4f6;

  .logo-icon {
    display: flex;
    align-items: center;
    color: #0066FF;
    
    img {
      width: 24px;
      height: 24px;
      object-fit: contain;
    }
  }

  .logo-text {
    font-size: 18px;
    font-weight: 600;
    color: #0066FF;
    flex: 1;
  }

  .logo-menu {
    font-size: 18px;
    color: #6b7280;
    cursor: pointer;
    padding: 4px;
    border-radius: 4px;
    transition: all 0.2s;

    &:hover {
      background: #f3f4f6;
    }
  }
}

.new-chat-btn {
  margin: 16px;
  padding: 12px 16px;
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  transition: all 0.2s;
  font-size: 14px;
  color: #374151;

  &:hover {
    background: #f3f4f6;
    border-color: #d1d5db;
  }

  i {
    font-size: 16px;
  }

  .shortcut {
    margin-left: auto;
    font-size: 12px;
    color: #9ca3af;
  }
}

.chat-history {
  flex: 1;
  overflow-y: auto;
  padding: 0 16px;
  margin-bottom: 16px;

  &::-webkit-scrollbar {
    width: 6px;
  }

  &::-webkit-scrollbar-thumb {
    background: #d1d5db;
    border-radius: 3px;
  }

  .history-title {
    font-size: 12px;
    font-weight: 600;
    color: #6b7280;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    padding: 8px 0;
    margin-bottom: 8px;
  }

  .no-history {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 40px 20px;
    color: #9ca3af;

    i {
      font-size: 48px;
      margin-bottom: 12px;
      opacity: 0.5;
    }

    p {
      font-size: 14px;
      margin: 0;
    }
  }

  .history-list {
    .history-item {
      padding: 10px 12px;
      margin-bottom: 4px;
      border-radius: 8px;
      display: flex;
      align-items: center;
      gap: 8px;
      cursor: pointer;
      transition: all 0.2s;
      position: relative;

      &:hover {
        background: #f3f4f6;

        .history-delete {
          opacity: 1;
        }
      }

      &.active {
        background: #eff6ff;
        color: #0066FF;
      }

      i {
        font-size: 16px;
        flex-shrink: 0;
      }

      .history-title-text {
        flex: 1;
        font-size: 14px;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
      }

      .history-delete {
        opacity: 0;
        font-size: 14px;
        padding: 4px;
        transition: opacity 0.2s;

        &:hover {
          color: #ef4444;
        }
      }
    }
  }
}

.user-info {
  padding: 12px 16px;
  border-top: 1px solid #f3f4f6;
  display: flex;
  align-items: center;
  gap: 10px;

  .user-avatar {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    background: #0066FF;
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 14px;
    font-weight: 600;
    flex-shrink: 0;
  }

  .user-email {
    flex: 1;
    font-size: 14px;
    color: #374151;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  .user-menu {
    font-size: 18px;
    color: #6b7280;
    cursor: pointer;
    padding: 4px;
    border-radius: 4px;
    transition: all 0.2s;

    &:hover {
      background: #f3f4f6;
    }
  }
}

/* 主内容区域 */
.chat-main {
  flex: 1;
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: #ffffff;
  overflow: hidden;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 40px 24px;
  background: #ffffff;

  &::-webkit-scrollbar {
    width: 6px;
  }

  &::-webkit-scrollbar-thumb {
    background: #d1d5db;
    border-radius: 3px;
  }
}

.welcome-message {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  padding: 40px 20px;

  .welcome-logo {
    margin-bottom: 24px;
    opacity: 0.9;
    
    img {
      width: 48px;
      height: 48px;
      object-fit: contain;
    }
  }

  .welcome-text {
    font-size: 24px;
    font-weight: 500;
    color: #1f2937;
    margin: 0;
  }
}

.message-item {
  display: flex;
  gap: 12px;
  margin-bottom: 24px;
  animation: fadeIn 0.3s ease;

  &.user {
    flex-direction: row-reverse;

    .message-content {
      background: #f3f4f6;
      color: #1f2937;
      border-radius: 16px 16px 4px 16px;
    }
  }

  &.assistant {
    .message-content {
      background: #ffffff;
      color: #1f2937;
      border-radius: 16px 16px 16px 4px;
      border: 1px solid #e5e7eb;
    }
  }
}

.message-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;

  &.assistant-avatar {
    background: #eff6ff;
    color: #0066FF;
    
    img {
      width: 32px;
      height: 32px;
      object-fit: contain;
      border-radius: 50%;
    }
  }

  &.user-avatar {
    background: #0066FF;
    color: white;
    font-size: 14px;
    font-weight: 600;
  }
}

.message-content {
  max-width: 70%;
  padding: 12px 16px;

  .message-text {
    font-size: 15px;
    line-height: 1.8;
    word-wrap: break-word;

    /* 段落样式 */
    :deep(p) {
      margin: 8px 0;
      
      &:first-child {
        margin-top: 0;
      }
      
      &:last-child {
        margin-bottom: 0;
      }
    }

    /* 标题样式 */
    :deep(h1), :deep(h2), :deep(h3), :deep(h4), :deep(h5), :deep(h6) {
      margin: 16px 0 8px 0;
      font-weight: 600;
      line-height: 1.4;
      
      &:first-child {
        margin-top: 0;
      }
    }

    :deep(h1) { font-size: 24px; }
    :deep(h2) { font-size: 20px; }
    :deep(h3) { font-size: 18px; }
    :deep(h4) { font-size: 16px; }
    :deep(h5) { font-size: 15px; }
    :deep(h6) { font-size: 14px; }

    /* 代码样式 */
    :deep(code) {
      background: rgba(0, 0, 0, 0.05);
      padding: 2px 6px;
      border-radius: 4px;
      font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
      font-size: 13px;
      color: #e83e8c;
    }

    :deep(pre) {
      background: #f6f8fa;
      border: 1px solid #e5e7eb;
      border-radius: 8px;
      padding: 12px 16px;
      overflow-x: auto;
      margin: 12px 0;
      
      code {
        background: transparent;
        padding: 0;
        color: inherit;
        font-size: 13px;
      }
    }

    /* 列表样式 */
    :deep(ul), :deep(ol) {
      margin: 8px 0;
      padding-left: 24px;
    }

    :deep(li) {
      margin: 4px 0;
    }

    /* 引用样式 */
    :deep(blockquote) {
      border-left: 4px solid #0066FF;
      padding-left: 16px;
      margin: 12px 0;
      color: #6b7280;
      font-style: italic;
    }

    /* 链接样式 */
    :deep(a) {
      color: #0066FF;
      text-decoration: none;
      
      &:hover {
        text-decoration: underline;
      }
    }

    /* 表格样式 */
    :deep(table) {
      border-collapse: collapse;
      width: 100%;
      margin: 12px 0;
    }

    :deep(th), :deep(td) {
      border: 1px solid #e5e7eb;
      padding: 8px 12px;
      text-align: left;
    }

    :deep(th) {
      background: #f9fafb;
      font-weight: 600;
    }

    /* 分割线 */
    :deep(hr) {
      border: none;
      border-top: 1px solid #e5e7eb;
      margin: 16px 0;
    }

    /* 文本样式 */
    :deep(strong) {
      font-weight: 600;
    }

    :deep(em) {
      font-style: italic;
    }

    :deep(u) {
      text-decoration: underline;
    }

    :deep(del) {
      text-decoration: line-through;
      opacity: 0.7;
    }

    /* 图片样式 */
    :deep(img) {
      max-width: 100%;
      height: auto;
      border-radius: 8px;
      margin: 8px 0;
    }
  }
}

.loading-indicator {
  display: flex;
  gap: 4px;
  padding: 8px 0;

  span {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #9ca3af;
    animation: loading 1.4s infinite ease-in-out;

    &:nth-child(1) {
      animation-delay: -0.32s;
    }

    &:nth-child(2) {
      animation-delay: -0.16s;
    }
  }
}

@keyframes loading {
  0%, 80%, 100% {
    transform: scale(0);
    opacity: 0.5;
  }
  40% {
    transform: scale(1);
    opacity: 1;
  }
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 输入区域 */
.chat-input-container {
  padding: 20px 24px;
  background: #ffffff;
  border-top: 1px solid #e5e7eb;
}

.feature-buttons {
  display: flex;
  gap: 8px;
  margin-bottom: 12px;

  .feature-btn {
    padding: 8px 12px;
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 14px;
    color: #374151;
    cursor: pointer;
    transition: all 0.2s;

    &:hover {
      background: #f9fafb;
      border-color: #d1d5db;
    }

    &.active {
      background: #eff6ff;
      border-color: #0066FF;
      color: #0066FF;
    }

    svg, i {
      width: 16px;
      height: 16px;
      flex-shrink: 0;
    }
  }
}

.input-wrapper {
  position: relative;
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 16px;
  padding: 12px 16px;
  display: flex;
  align-items: flex-end;
  gap: 12px;
  transition: all 0.2s;

  &:focus-within {
    border-color: #0066FF;
    box-shadow: 0 0 0 3px rgba(0, 102, 255, 0.1);
  }

  .chat-input {
    flex: 1;

    :deep(.el-textarea__inner) {
      border: none;
      background: transparent;
      padding: 0;
      font-size: 15px;
      line-height: 1.5;
      resize: none;
      box-shadow: none;

      &:focus {
        border: none;
        box-shadow: none;
      }
    }
  }

  .input-actions {
    display: flex;
    align-items: center;
    gap: 8px;
    flex-shrink: 0;
    padding-bottom: 2px;

    .input-icon {
      font-size: 20px;
      color: #6b7280;
      cursor: pointer;
      padding: 4px;
      border-radius: 4px;
      transition: all 0.2s;

      &:hover {
        background: #e5e7eb;
        color: #374151;
      }
    }

    .send-btn {
      width: 36px;
      height: 36px;
      border-radius: 50%;
      background: #0066FF;
      border: none;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      transition: all 0.2s;
      flex-shrink: 0;

      &:hover:not(:disabled) {
        background: #0052CC;
        transform: scale(1.05);
      }

      &:disabled {
        opacity: 0.5;
        cursor: not-allowed;
      }

      svg {
        width: 20px;
        height: 20px;
      }
    }
  }
}

:deep(.el-dialog) {
  border-radius: 16px;
}

:deep(.el-form-item__label) {
  font-weight: 500;
  color: #374151;
}

:deep(.el-input__inner) {
  border-radius: 8px;
  border-color: #e5e7eb;

  &:focus {
    border-color: #0066FF;
  }
}
</style>

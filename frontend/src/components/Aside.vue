 <script setup>
  import '../assets/iconfont.css'
  </script>

  <template>
    <div>
      <el-menu
        ref="menu"
        :default-active="$route.path"
        class="el-menu-vertical"
        :collapse-transition="false"
        background-color="transparent"
        text-color="#606266"
        active-text-color="#fff"
        @select="handleMenuSelect"
      >
        <div v-for="item in userMenuList" :key="item.id">
          <div v-if="item.path">
            <el-menu-item :index="item.path">
              <i :class="getIconClass(item.icon)"></i>
              <span>{{ item.name }}</span>
            </el-menu-item>
          </div>

          <div v-else>
            <el-submenu :index="String(item.id)">
              <template slot="title">
                <i :class="getIconClass(item.icon)"></i>
                <span>{{ item.name }}</span>
              </template>

              <div v-for="subItem in item.children" :key="subItem.id">
                <el-menu-item :index="subItem.path">
                  <i :class="getIconClass(subItem.icon)"></i>
                  <span>{{ subItem.name }}</span>
                </el-menu-item>
              </div>
            </el-submenu>
          </div>
        </div>
      </el-menu>
    </div>
  </template>

  <script>
  import { getIconByKey } from '../utils/iconMapping.js'
  import { staticMenuList } from '../utils/staticMenu'

  export default {
    name: 'AsideMenu',
    data() {
      return {
        userMenuList: staticMenuList,
        userInfo: {},
        path: this.$route.path
      }
    },
    created() {
      this.userInfo = localStorage.getItem('userInfo')
        ? JSON.parse(localStorage.getItem('userInfo'))
        : {}
      this.refreshMenu()
    },
    methods: {
      getIconClass(iconKey) {
        if (!iconKey) return 'el-icon-menu'
        return getIconByKey(iconKey)
      },
      refreshMenu() {
        this.userMenuList = staticMenuList
        localStorage.setItem('userMenuList', JSON.stringify(staticMenuList))
      },
      handleMenuSelect(index) {
        if (index && typeof index === 'string' && !/^\d+$/.test(index) && this.$route.path !== index)
  {
          this.$router.push(index).catch(err => {
            if (err.name !== 'NavigationDuplicated') {
              console.error(err)
            }
          })
        }
      },
    },
    watch: {
      $route(to) {
        this.$nextTick(() => {
          if (this.$refs.menu) {
            this.$refs.menu.activeIndex = to.path
          }
        })
      }
    }
  }
  </script>

  <style lang="less" scoped>
  .el-menu-vertical {
    border-right: none;
    padding: 16px 12px;
    background: linear-gradient(90deg, #4a90e2 0%, #e8f4fd 100%);
    min-height: 100vh;
  }

  .el-menu-item {
    height: 48px;
    line-height: 48px;
    border-radius: 8px;
    margin-bottom: 4px;
    color: #4a5568;
    font-size: 14px;
    font-weight: 400;
    padding: 0 16px !important;
    transition: all 0.3s ease;
    background-color: transparent;

    &:hover {
      color: #4a5568;
      background-color: rgba(255, 255, 255, 0.3) !important;
    }

    &.is-active {
      color: #fff;
      background: #4a90e2 !important;
      font-weight: 600;
      box-shadow: 0 2px 8px rgba(74, 144, 226, 0.3);
      position: relative;

      &::before {
        content: '';
        position: absolute;
        left: 0;
        top: 50%;
        transform: translateY(-50%);
        width: 4px;
        height: 24px;
        background: #fff;
        border-radius: 0 2px 2px 0;
      }
    }
  }

  .el-submenu ::v-deep .el-submenu__title {
    height: 48px;
    line-height: 48px;
    border-radius: 8px;
    color: #4a5568;
    font-size: 14px;
    font-weight: 400;
    padding: 0 16px !important;
    margin-bottom: 4px;
    transition: all 0.3s ease;
    background-color: transparent;

    &:hover {
      color: #4a5568;
      background-color: rgba(255, 255, 255, 0.3) !important;
    }
  }

  .el-submenu.is-opened ::v-deep .el-submenu__title {
    color: #fff;
    background-color: rgba(255, 255, 255, 0.2) !important;
  }

  .el-submenu ::v-deep .el-menu--inline {
    padding-left: 0;
    background-color: transparent;
    margin-top: 4px;
    margin-bottom: 8px;

    .el-menu-item {
      height: 44px;
      line-height: 44px;
      padding-left: 48px !important;
      background-color: transparent;
      margin-bottom: 2px;
      color: #4a5568;
      border-radius: 6px;

      &:hover {
        color: #4a5568;
        background-color: rgba(255, 255, 255, 0.2) !important;
      }

      &.is-active {
        color: #fff;
        background: #4a90e2 !important;
        font-weight: 600;
        width: 100%;
        box-shadow: 0 2px 6px rgba(74, 144, 226, 0.25);
        position: relative;

        &::before {
          content: '';
          position: absolute;
          left: 0;
          top: 50%;
          transform: translateY(-50%);
          width: 3px;
          height: 20px;
          background: #fff;
          border-radius: 0 2px 2px 0;
        }
      }
    }
  }

  .el-menu-item [class^='el-icon-'],
  .el-submenu [class^='el-icon-'] {
    font-size: 18px;
    margin-right: 12px;
    color: #718096;
    transition: color 0.3s ease;
  }

  .el-menu-item:hover [class^='el-icon-'],
  .el-submenu:hover [class^='el-icon-'] {
    color: #4a5568;
  }

  .el-menu-item.is-active [class^='el-icon-'] {
    color: #fff;
  }

  .el-submenu.is-opened [class^='el-icon-'],
  .el-submenu.is-opened ::v-deep .el-submenu__title [class^='el-icon-'] {
    color: #fff;
  }

  .el-submenu ::v-deep .el-submenu__icon-arrow {
    color: #718096;
    font-size: 12px;
    margin-top: -6px;
    transition: all 0.3s ease;
    right: 16px;
  }

  .el-submenu:hover ::v-deep .el-submenu__icon-arrow {
    color: #4a5568;
  }

  .el-submenu.is-opened ::v-deep .el-submenu__icon-arrow {
    color: #fff;
    transform: rotate(180deg);
  }
  </style>
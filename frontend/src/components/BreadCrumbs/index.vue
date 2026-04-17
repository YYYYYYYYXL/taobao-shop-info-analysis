  <template>
    <div class="breadcrumbs">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item
          v-for="(item, index) in breadcrumbList"
          :key="item.path || index"                                      
        >                                                                
          <span                                                          
            v-if="index === breadcrumbList.length - 1"                   
            class="current"                                              
          >                                                              
            {{ item.title }}                                             
          </span>                                                        
          <a                                                             
            v-else                                                       
            href="javascript:;"                                          
            class="link"                                                 
            @click="handleNavigate(item)"                                
          >                                                              
            {{ item.title }}                                             
          </a>                                                           
        </el-breadcrumb-item>                                            
      </el-breadcrumb>                                                   
    </div>                                                               
  </template>                                                            
                                                                         
  <script>                                                               
  export default {                                                       
    name: 'BreadCrumbs',                                                 
    computed: {                                                          
      breadcrumbList() {                                                 
        const matched = this.$route.matched || []                        
                                                                         
        const list = matched                                             
          .filter(item => item.path && item.meta && item.meta.title)     
          .map(item => ({                                                
            path: item.path,                                             
            title: item.meta.title                                       
          }))                                                            

        if (!list.length && this.$route.meta && this.$route.meta.title) {          return [                                                       
            {                                                            
              path: this.$route.path,                                    
              title: this.$route.meta.title                              
            }                                                            
          ]                                                              
        }                                                                
                                                                         
        return list                                                      
      }                                                                  
    },                                                                   
    methods: {                                                           
      handleNavigate(item) {                                             
        if (!item || !item.path || item.path === this.$route.path) {     
          return                                                         
        }                                                                
                                                                         
        this.$router.push(item.path).catch(err => {                      
          if (err.name !== 'NavigationDuplicated') {                     
            console.error('路由跳转失败:', err)                          
          }                                                              
        })                                                               
      }                                                                  
    }                                                                    
  }                                                                      
  </script>                                                              
                                                                         
  <style lang="less" scoped>                                             
  .breadcrumbs {                                                         
    display: flex;                                                       
    align-items: center;                                                 
    min-width: 0;                                                        
  }                                                                      
                                                                         
  .link {                                                                
    color: #409eff;                                                      
    text-decoration: none;                                               
    cursor: pointer;                                                     
  }                                                                      
                                                                         
  .current {                                                             
    color: #606266;
    font-weight: 500;                                                    
  }                                                                      
  </style>    
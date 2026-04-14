<template>
    <div class="menu-manager">
        <!-- 数据统计卡片 -->
        <div class="statistics-cards">
            <el-row :gutter="20">
                <el-col :span="8">
                    <el-card shadow="hover" class="stat-card">
                        <div class="stat-content">
                            <div class="stat-left">
                                <div class="stat-icon"><i class="el-icon-menu"></i></div>
                                <div class="stat-title">总菜单数</div>
                            </div>
                            <div class="stat-value">
                                <count-to :startVal="0" :endVal="menuStats.totalMenus" :duration="2000">
                                </count-to>
                            </div>
                        </div>
                    </el-card>
                </el-col>
                <el-col :span="8">
                    <el-card shadow="hover" class="stat-card">
                        <div class="stat-content">
                            <div class="stat-left">
                                <div class="stat-icon"><i class="el-icon-folder"></i></div>
                                <div class="stat-title">一级菜单</div>
                            </div>
                            <div class="stat-value">
                                <count-to :startVal="0" :endVal="menuStats.firstLevelMenus" :duration="2000">
                                </count-to>
                            </div>
                        </div>
                    </el-card>
                </el-col>
                <el-col :span="8">
                    <el-card shadow="hover" class="stat-card">
                        <div class="stat-content">
                            <div class="stat-left">
                                <div class="stat-icon"><i class="el-icon-folder-opened"></i></div>
                                <div class="stat-title">二级菜单</div>
                            </div>
                            <div class="stat-value">
                                <count-to :startVal="0" :endVal="menuStats.secondLevelMenus" :duration="2000">
                                </count-to>
                            </div>
                        </div>
                    </el-card>
                </el-col>
            </el-row>
        </div>

        <div class="content-box">
            <!-- 操作栏 -->
            <el-card class="operation-area" shadow="hover">
                <div class="control-btns">
                    <div class="right-btns">
                        <el-button type="primary" plain size="medium" @click="exportVisible = true">
                            <i class="el-icon-download"></i> 导出数据
                        </el-button>
                        <el-button type="primary" plain size="medium" @click="openDialog('add')">
                            <i class="el-icon-plus"></i> 新增菜单项
                        </el-button>
                        <el-button plain size="medium" @click="fetchData">
                            <i class="el-icon-refresh"></i> 刷新
                        </el-button>
                    </div>
                </div>
            </el-card>

            <!-- 表格区域 -->
            <el-card class="table-card" shadow="hover">
                <el-table ref="multipleTable" v-loading="listLoading" :data="tableData"
                          row-key="id" tooltip-effect="dark" style="width: 100%"
                     size="medium" class="card-table">
                    <el-table-column prop="id" label="ID" width="80" align="center"></el-table-column>
                    <el-table-column prop="name" label="菜单名称" min-width="120" show-overflow-tooltip	></el-table-column>
                    <el-table-column prop="path" label="菜单路径" min-width="120" show-overflow-tooltip	></el-table-column>
                    <el-table-column label="菜单图标" width="100" align="center">
                        <template slot-scope="scope">
                            <i :class="getIconClass(scope.row.icon)" style="font-size: 18px;"></i>
                        </template>
                    </el-table-column>
                    <el-table-column prop="description" label="菜单描述" min-width="150"></el-table-column>
                    <el-table-column prop="pagePath" label="页面路径" min-width="120" show-overflow-tooltip	></el-table-column>
                    <el-table-column prop="role" label="菜单权限" min-width="120" show-overflow-tooltip	>
                        <template slot-scope="scope">
                            <el-tag v-if="scope.row.role.includes('ADMIN')" size="small" type="warning">管理员</el-tag>
                            <el-tag v-if="scope.row.role.includes('USER')" size="small" type="info">普通用户</el-tag>
                        </template>
                    </el-table-column>
                    <el-table-column prop="sortNum" label="排序" width="80" align="center"></el-table-column>
                    <el-table-column label="操作" width="300" align="center" >
                        <template slot-scope="scope">
                            <el-button v-if="!scope.row.pid && !scope.row.path" 
                                     size="mini" type="success" plain
                                     @click="addChildMenu(scope.row.id)">
                                <i class="el-icon-plus"></i> 子菜单
                            </el-button>
                            <el-button size="mini" type="primary" plain @click="openDialog('edit', scope.row)">
                                <i class="el-icon-edit"></i> 编辑
                            </el-button>
                            <el-button size="mini" type="danger" plain @click="handleDelete(scope.$index, scope.row)">
                                <i class="el-icon-delete"></i> 删除
                            </el-button>
                        </template>
                    </el-table-column>
                </el-table>
            </el-card>

            <!-- 新增/编辑菜单项 弹出框 -->
            <el-dialog :title="dialogMode === 'add' ? '新增菜单项' : '修改菜单项'" :visible.sync="formVisible" width="500px"
                :close-on-click-modal="false" append-to-body>
                <el-form :model="dialogForm" :rules="formRules" ref="dialogForm" label-width="100px">
                    <el-form-item label="菜单名称" prop="name">
                        <el-input v-model="dialogForm.name" placeholder="请输入菜单名称"></el-input>
                    </el-form-item>
                    <el-form-item label="菜单路径">
                        <el-input v-model="dialogForm.path" placeholder="请输入菜单路径"></el-input>
                    </el-form-item>
                    <el-form-item label="菜单图标" prop="icon">
                        <el-select v-model="dialogForm.icon" filterable placeholder="请选择图标" style="width: 100%;">
                            <el-option v-for="dict in iconDict" :key="dict.itemValue" :label="dict.itemKey"
                                :value="dict.itemValue">
                                <i :class="dict.iconClass"></i>
                                <span style="margin-left: 10px;">{{ dict.itemKey }}</span>
                            </el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item label="页面路径">
                        <el-input v-model="dialogForm.pagePath" placeholder="请输入页面路径"></el-input>
                    </el-form-item>
                    <el-form-item label="排序" prop="sortNum">
                        <el-input-number v-model="dialogForm.sortNum" :min="0" controls-position="right" style="width: 100%;"></el-input-number>
                    </el-form-item>
                    <el-form-item label="菜单权限" prop="role">
                        <el-checkbox-group v-model="checkList">
                            <el-checkbox label="管理员" key="ADMIN"></el-checkbox>
                            <el-checkbox label="普通用户" key="USER"></el-checkbox>
                        </el-checkbox-group>
                    </el-form-item>
                    <el-form-item label="描述">
                        <el-input type="textarea" v-model="dialogForm.description" placeholder="请输入描述信息"></el-input>
                    </el-form-item>
                </el-form>
                <div slot="footer" class="dialog-footer">
                    <el-button @click="formVisible = false" plain>取 消</el-button>
                    <el-button type="primary" :loading="isSubmit" @click="handleSave('dialogForm')" plain>确 定</el-button>
                </div>
            </el-dialog>

            <!-- 导出数据 弹出栏 -->
            <el-dialog title="导出数据" :visible.sync="exportVisible" width="600px" :close-on-click-modal="false" append-to-body>
                <div class="export-data">
                    <el-button type="primary" plain @click="exportTable('xlsx')" :disabled="isExporting">
                        <i class="el-icon-document"></i> EXCEL格式
                    </el-button>
                    <el-button type="primary" plain @click="exportTable('csv')" :disabled="isExporting">
                        <i class="el-icon-document"></i> CSV格式
                    </el-button>
                    <el-button type="primary" plain @click="exportTable('txt')" :disabled="isExporting">
                        <i class="el-icon-document"></i> TXT格式
                    </el-button>
                </div>
                <div v-if="isExporting" class="export-progress">
                    <el-progress :percentage="exportProgress" :status="exportProgress === 100 ? 'success' : null" :stroke-width="20"></el-progress>
                    <div class="progress-text">{{ exportProgressText }}</div>
                </div>
                <div class="hints">提示：请选择要导出数据的格式</div>
            </el-dialog>
        </div>
    </div>
</template>

<script>
import excel from '../utils/excel.js'
import Request from '../utils/request.js'
import { getIconList, getIconByKey } from '../utils/iconMapping.js'
import CountTo from 'vue-count-to'

export default {
    name: 'MenuManager',
    components: {
        CountTo
    },
    data() {
        return {
            // 数据列表加载动画
            listLoading: true,
            formLabelWidth: '80px',
            iconDict: [],
            checkList: [],
            // 新增/编辑提交表单对象
            dialogForm: {
                name: undefined,
                description: undefined,
            },
            // 数据总条数
            total: 0,
            // 表格数据数组
            tableData: [],
            // 新增/编辑 弹出框显示/隐藏
            formVisible: false,
            // 当前对话框模式
            dialogMode: 'add', // 'add' or 'edit'
            // 导出数据 弹出框显示/隐藏
            exportVisible: false,
            // 导出进度
            exportProgress: 0,
            // 是否正在导出
            isExporting: false,
            // 导出进度文本
            exportProgressText: '',
            // 防止多次连续提交表单
            isSubmit: false,
            // 菜单统计数据
            menuStats: {
                totalMenus: 0,
                firstLevelMenus: 0,
                secondLevelMenus: 0
            },
            // 表单校验 trigger: ['blur', 'change'] 为多个事件触发
            formRules: {
                // 验证规则
                name: [
                    { required: true, message: '请填写菜单名称', trigger: 'blur' }
                ],
                sortNum: [
                    { required: true, message: '排序不能为空', trigger: 'blur' },
                ],
                icon: [
                    { required: true, message: '请选择菜单图标', trigger: 'change' }
                ]
            }
        }
    },
    created() {
        this.fetchData()
        this.loadIconList()
    },
    methods: {
        // 根据图标key获取对应的图标类
        getIconClass(iconKey) {
            if (!iconKey) return 'el-icon-menu'
            return getIconByKey(iconKey)
        },
        handleDelete(index, row) {
            // console.log(index, row)
            this.$confirm('此操作将删除选中数据, 是否继续?', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            }).then(() => {
                Request.delete("/menu/deleteById/" + row.id).then(response => {
                    if (response.code == 0) {
                        this.$message({
                            type: 'success',
                            message: '删除成功!'
                        })
                        this.fetchData()
                    } else {
                        this.$message({
                            type: 'error',
                            errpr: '删除失败!'
                        })
                    }
                });

            }).catch(() => {
                this.$message({
                    type: 'info',
                    message: '已取消删除'
                })
            })
        },
        addChildMenu(pid) {
            this.dialogMode = 'add';
            this.formVisible = true;
            this.dialogForm = {
                pid: pid,
                name: '',
                path: '',
                icon: '',
                pagePath: '',
                description: '',
                sortNum: 0
            };
            this.checkList = [];
            this.loadIconList();
        },
        loadIconList() {
            try {
                // 使用 iconMapping.js 中的 getIconList 函数获取图标列表
                this.iconDict = getIconList();
            } catch (error) {
                // 静默处理加载图标列表失败
                this.$message({
                    type: 'error',
                    message: '加载图标列表失败!'
                });
                this.iconDict = [];
            }
        },
        // 获取数据列表
        async fetchData() {
            this.listLoading = true
            try {
                const res = await Request.get("/menu/findAll")
                if (res.code === '0') {
                    this.tableData = res.data || []
                    this.total = this.tableData.length
                    this.calculateMenuStats()
                } else {
                }
            } catch (error) {
            } finally {
                this.listLoading = false
            }
        },

        openDialog(mode, row = {}) {
            this.dialogMode = mode;
            this.formVisible = true;
            this.loadIconList();
            if (mode === 'edit') {
                this.dialogForm = JSON.parse(JSON.stringify(row));
                this.checkList = this.formatRolesToChinese(row.role);
            } else {
                this.dialogForm = {};
                this.checkList = [];
            }
        },
        // 保存新增/编辑数据
        handleSave(formName) {
            this.dialogForm.role = this.formatRolesToEnglish(this.checkList);
            this.$refs[formName].validate(valid => {
                if (valid) {
                    const saveData = {
                        ...this.dialogForm,
                        pid: this.dialogForm.pid || null
                    };

                    const request = this.dialogMode === 'add' 
                        ? Request.post("/menu/save", saveData) 
                        : Request.put("/menu/" + this.dialogForm.id, saveData);

                    request.then(response => {
                        if (response.code === '0') {
                            this.$message({
                                showClose: true,
                                message: this.dialogMode === 'add' ? '添加成功' : '更新成功',
                                type: 'success',
                            });
                            this.$emit('update:user', this.userInfo);
                            this.formVisible = false;
                            this.fetchData();
                        } else {
                            this.$message({
                                showClose: true,
                                message: response.msg || (this.dialogMode === 'add' ? '添加失败' : '更新失败'),
                                type: 'error',
                            });
                        }
                    }).catch(error => {
                        // 静默处理保存失败
                        this.$message.error('操作失败，请重试');
                    }).finally(() => {
                        this.isSubmit = false;
                    });
                } else {
                    this.isSubmit = false;
                }
            });
        },

        // 导出数据--excle格式
        async exportTable(type) {
            if (this.tableData.length) {
                try {
                    // 初始化导出状态
                    this.isExporting = true
                    this.exportProgress = 0
                    this.exportProgressText = '准备导出...'
                    
                    // 进度更新回调函数
                    const updateProgress = (progress, text) => {
                        this.exportProgress = progress
                        this.exportProgressText = text
                    }
                    
                    // 格式化数据（占0-70%）
                    updateProgress(10, '正在格式化数据...')
                    const exportData = []
                    
                    // 扁平化菜单树数据
                    const flattenMenus = (menus) => {
                        let result = []
                        const traverse = (items) => {
                            items.forEach(item => {
                                result.push(item)
                                if (item.children && item.children.length > 0) {
                                    traverse(item.children)
                                }
                            })
                        }
                        traverse(menus)
                        return result
                    }
                    
                    const flatData = flattenMenus(this.tableData)
                    
                    for (let i = 0; i < flatData.length; i++) {
                        const menu = flatData[i]
                        exportData.push({
                            id: menu.id || '',
                            name: menu.name || '',
                            path: menu.path || '',
                            icon: menu.icon || '',
                            description: menu.description || '',
                            pid: menu.pid || '',
                            pagePath: menu.pagePath || '',
                            sortNum: menu.sortNum || 0,
                            role: menu.role || ''
                        })
                        
                        // 每处理10条更新一次进度
                        if ((i + 1) % 10 === 0 || i === flatData.length - 1) {
                            const progress = 10 + Math.round(((i + 1) / flatData.length) * 60)
                            updateProgress(progress, `正在格式化数据: ${i + 1}/${flatData.length}`)
                            // 使用 setTimeout 让 UI 有机会更新
                            await new Promise(resolve => setTimeout(resolve, 0))
                        }
                    }
                    
                    // 导出文件（占70%-100%）
                    updateProgress(75, '正在生成文件...')
                    const params = {
                        header: ['菜单ID', '菜单名', '菜单路径', '菜单图标', '描述', '父级菜单ID', '页面路径', '排序', '菜单所属角色'],
                        key: ['id', 'name', 'path', 'icon', 'description', 'pid', 'pagePath', 'sortNum', 'role'],
                        data: exportData,
                        autoWidth: true,
                        fileName: '菜单数据表',
                        bookType: type
                    }
                    
                    // 使用 setTimeout 确保进度条更新
                    await new Promise(resolve => setTimeout(resolve, 100))
                    updateProgress(90, '正在保存文件...')
                    
                    excel.exportDataToExcel(params)
                    
                    // 完成
                    updateProgress(100, '导出完成！')
                    await new Promise(resolve => setTimeout(resolve, 500))
                    
                    this.isExporting = false
                    this.exportProgress = 0
                    this.exportProgressText = ''
                    this.exportVisible = false
                    this.$message.success('导出成功')
                } catch (error) {
                    console.error('导出失败:', error)
                    this.isExporting = false
                    this.exportProgress = 0
                    this.exportProgressText = ''
                    this.$message.error('导出失败，请稍后重试')
                }
            } else {
                this.$message.warning('暂无数据可导出')
            }
        },
        getMenuRole(role) {
            const roleMap = {
                USER: '普通用户',
                ADMIN: '管理员'
            };

            // 如果role为空，则返回空字符串
            if (!role) {
                return '';
            }

            // 将角色字符串按照逗号分割成数组
            const roles = role.split(',');

            // 使用 map 方法将数组中的每个英文角色转换为中文角色
            const chineseRoles = roles.map((singleRole) => roleMap[singleRole]);

            // 使用 join 方法将转换后的中文角色数组连接成一个逗号分隔的字符串
            return chineseRoles.join(',');
        },
        formatRolesToChinese(role) {
            const roleMap = {
                USER: '普通用户',
                ADMIN: '管理员'
            };

            // 如果role为空，则返回空数组
            if (!role) {
                return [];
            }

            // 将角色字符串按照逗号分割成数组，并去除单引号
            const roles = role.split(',').map(singleRole => singleRole.trim().replace(/'/g, ''));

            // 使用 map 方法将数组中的每个英文角色转换为中文角色
            const chineseRoles = roles.map(singleRole => roleMap[singleRole]);

            // 过滤掉未找到映射的项（如果英文角色不在roleMap中）
            const validChineseRoles = chineseRoles.filter(role => role !== undefined);

            // 返回中文角色数组
            return validChineseRoles;
        },


        formatRolesToEnglish(chineseRoles) {
            const roleMap = {
                普通用户: 'USER',
                管理员: 'ADMIN'
            };

            // 如果输入数组为空，则返回空字符串
            if (!chineseRoles || chineseRoles.length === 0) {
                return '';
            }

            // 使用 map 方法将数组中的每个中文角色转换为英文角色
            const englishRoles = chineseRoles.map(singleRole => roleMap[singleRole.trim()]);

            // 使用 join 方法将转换后的英文角色数组连接成一个逗号分隔的字符串
            return englishRoles.join(',');
        },
        // 计算菜单统计数据
        calculateMenuStats() {
            // 统计各级菜单数量
            let firstLevelCount = 0
            let secondLevelCount = 0
            let totalCount = 0
            
            // 递归遍历菜单树
            const traverseMenus = (menus, level = 1) => {
                menus.forEach(menu => {
                    totalCount++
                    
                    if (level === 1) {
                        firstLevelCount++
                    } else if (level === 2) {
                        secondLevelCount++
                    }
                    
                    // 递归遍历子菜单
                    if (menu.children && menu.children.length > 0) {
                        traverseMenus(menu.children, level + 1)
                    }
                })
            }
            
            // 开始遍历
            traverseMenus(this.tableData)
            
            this.menuStats = {
                totalMenus: totalCount,
                firstLevelMenus: firstLevelCount,
                secondLevelMenus: secondLevelCount
            }
        }
    }
}
</script>

<style lang="less" scoped>
.menu-manager {
    padding: 12px;
    background: linear-gradient(to bottom, #f5f7fa 0%, #ffffff 100%);
    min-height: calc(100vh - 70px);
    position: relative;

    &::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-image: 
            radial-gradient(circle at 20% 50%, rgba(102, 126, 234, 0.03) 0%, transparent 50%),
            radial-gradient(circle at 80% 80%, rgba(118, 75, 162, 0.03) 0%, transparent 50%);
        pointer-events: none;
        z-index: 0;
    }

    > * {
        position: relative;
        z-index: 1;
    }
}

.statistics-cards {
    margin-bottom: 24px;
}

.stat-card {
    border-radius: 12px;
    transition: all 0.3s ease;
    border: none;
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.9) 0%, rgba(255, 255, 255, 0.95) 100%);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
    position: relative;
    overflow: hidden;
    backdrop-filter: blur(10px);

    &::before {
        display: none;
    }

    &:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
    }

    :deep(.el-card__body) {
        padding: 0;
    }
}

.stat-content {
    padding: 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.stat-left {
    display: flex;
    align-items: center;
    gap: 14px;
}

.stat-icon {
    font-size: 28px;
    color: #4a90e2;
    opacity: 0.9;
    width: 52px;
    height: 52px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 12px;
    background: linear-gradient(135deg, rgba(74, 144, 226, 0.1) 0%, rgba(74, 144, 226, 0.05) 100%);
    transition: all 0.3s ease;
}

.stat-card:nth-child(1) .stat-icon {
    background: linear-gradient(135deg, rgba(74, 144, 226, 0.12) 0%, rgba(74, 144, 226, 0.06) 100%);
    color: #4a90e2;
}

.stat-card:nth-child(2) .stat-icon {
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.12) 0%, rgba(102, 126, 234, 0.06) 100%);
    color: #667eea;
}

.stat-card:nth-child(3) .stat-icon {
    background: linear-gradient(135deg, rgba(139, 92, 246, 0.12) 0%, rgba(139, 92, 246, 0.06) 100%);
    color: #8b5cf6;
}

.stat-card:hover .stat-icon {
    transform: scale(1.05);
}

.stat-title {
    font-size: 14px;
    color: #6b7280;
    font-weight: 500;
    letter-spacing: 0.2px;
}

.stat-value {
    font-size: 28px;
    font-weight: 700;
    color: #1f2937;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    letter-spacing: 0.5px;
    
    &::after {
        display: none;
    }
}

.page-header {
    display: flex;
    align-items: center;
    margin-bottom: 20px;

    h2 {
        font-size: 18px;
        font-weight: 600;
        color: #1f2937;
        margin: 0;
        margin-right: 15px;
        letter-spacing: 0.3px;
    }
}

.operation-area {
    background: white;
    border-radius: 16px;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.04);
    margin-bottom: 16px;
    padding: 20px;
    border: none;

    :deep(.el-card__body) {
        padding: 0;
    }
}

.table-card {
    border-radius: 16px;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.04);
    background: white;
    border: none;

    :deep(.el-card__body) {
        padding: 20px;
    }
}

.control-btns {
    display: flex;
    justify-content: flex-start;
    align-items: center;

    .right-btns {
        display: flex;
        gap: 12px;
    }
}

:deep(.el-table) {
    border-radius: 12px;
    overflow: visible;
    box-shadow: none;
    border: none;
    background: transparent;

    .el-table__header-wrapper {
        th {
            background-color: transparent;
            font-weight: 600;
            color: #374151;
            padding: 16px 12px;
            font-size: 14px;
            border-bottom: none;
        }
    }

    .el-table__body-wrapper {
        .el-table__body {
            tr {
                background: white;
                border-radius: 8px;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
                transition: all 0.3s ease;
                
                &:hover {
                    transform: translateY(-2px);
                    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
                    background: white;
                }
                
                td {
                    padding: 16px 12px;
                    color: #4b5563;
                    font-size: 14px;
                    border-bottom: none;
                    background: white;
                }
                
                &:first-child td:first-child {
                    border-top-left-radius: 8px;
                }
                
                &:first-child td:last-child {
                    border-top-right-radius: 8px;
                }
                
                &:last-child td:first-child {
                    border-bottom-left-radius: 8px;
                }
                
                &:last-child td:last-child {
                    border-bottom-right-radius: 8px;
                }
            }
        }
    }
    
    &::before {
        display: none;
    }
    
    .el-table__header,
    .el-table__body {
        border: none;
    }
    
    .el-table__header th,
    .el-table__body td {
        border: none;
    }
}

.card-table {
    :deep(.el-table__body-wrapper) {
        padding: 12px 0;
        
        .el-table__body {
            border-collapse: separate;
            border-spacing: 0 12px;
            
            tr {
                background: white;
                border-radius: 8px;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
                transition: all 0.3s ease;
                
                &:hover {
                    transform: translateY(-2px);
                    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
                }
                
                td {
                    border-bottom: none;
                    background: white;
                    padding: 16px 12px;
                    
                    &:first-child {
                        border-top-left-radius: 8px;
                        border-bottom-left-radius: 8px;
                    }
                    
                    &:last-child {
                        border-top-right-radius: 8px;
                        border-bottom-right-radius: 8px;
                    }
                }
            }
        }
    }
    
    :deep(.el-table__header-wrapper) {
        .el-table__header {
            border-collapse: separate;
            
            th {
                background-color: transparent;
                border-bottom: none;
                padding: 16px 12px;
            }
        }
    }
}

.el-tag {
    margin-right: 6px;
    
    &:last-child {
        margin-right: 0;
    }
}

:deep(.el-dialog) {
    border-radius: 16px;
    overflow: hidden;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12);
}

:deep(.el-dialog__header) {
    padding: 20px 24px;
    border-bottom: 1px solid #e5e7eb;
    margin: 0;
    background: #f9fafb;
}

:deep(.el-dialog__title) {
    font-size: 18px;
    font-weight: 600;
    color: #1f2937;
    letter-spacing: 0.3px;
}

:deep(.el-dialog__body) {
    padding: 24px;
}

:deep(.el-dialog__footer) {
    padding: 16px 24px;
    border-top: 1px solid #e5e7eb;
    background: #f9fafb;
}

.export-data {
    display: flex;
    justify-content: space-around;
    margin-bottom: 20px;
    gap: 12px;
}

.export-progress {
    margin: 20px 0;
    padding: 20px;
    background: #f9fafb;
    border-radius: 8px;
    
    .progress-text {
        text-align: center;
        margin-top: 12px;
        color: #374151;
        font-size: 14px;
        font-weight: 500;
    }
}

.hints {
    text-align: center;
    color: #6b7280;
    font-size: 13px;
}

:deep(.el-input__inner) {
    border-radius: 8px;
    border-color: #e5e7eb;
    transition: all 0.3s ease;

    &:focus {
        border-color: #667eea;
    }
}

:deep(.el-button) {
    border-radius: 8px;
    font-weight: 500;
    transition: all 0.3s ease;

    // 主要按钮 - 浅色风格
    &.el-button--primary.is-plain {
        border-color: rgba(74, 144, 226, 0.3);
        color: #4a90e2;
        background: rgba(74, 144, 226, 0.08);

        &:hover:not(:disabled) {
            background: rgba(74, 144, 226, 0.15);
            border-color: rgba(74, 144, 226, 0.4);
            color: #3d7bc8;
            transform: translateY(-1px);
            box-shadow: 0 2px 8px rgba(74, 144, 226, 0.2);
        }

        &:disabled {
            border-color: rgba(74, 144, 226, 0.15);
            color: rgba(74, 144, 226, 0.4);
            background: rgba(74, 144, 226, 0.04);
            cursor: not-allowed;
        }
    }

    // 普通按钮 - 浅色风格
    &.el-button--default.is-plain {
        border-color: rgba(0, 0, 0, 0.15);
        color: #6b7280;
        background: rgba(0, 0, 0, 0.04);

        &:hover:not(:disabled) {
            background: rgba(0, 0, 0, 0.08);
            border-color: rgba(0, 0, 0, 0.2);
            color: #374151;
            transform: translateY(-1px);
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        }

        &:disabled {
            border-color: rgba(0, 0, 0, 0.08);
            color: rgba(0, 0, 0, 0.25);
            background: rgba(0, 0, 0, 0.02);
            cursor: not-allowed;
        }
    }

    // 普通按钮（非plain）- 浅色风格
    &.el-button--default:not(.is-plain) {
        border-color: rgba(0, 0, 0, 0.15);
        color: #6b7280;
        background: rgba(0, 0, 0, 0.04);

        &:hover:not(:disabled) {
            background: rgba(0, 0, 0, 0.08);
            border-color: rgba(0, 0, 0, 0.2);
            color: #374151;
            transform: translateY(-1px);
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        }
    }

    // 成功按钮 - 浅色风格
    &.el-button--success.is-plain {
        border-color: rgba(16, 185, 129, 0.3);
        color: #10b981;
        background: rgba(16, 185, 129, 0.08);

        &:hover:not(:disabled) {
            background: rgba(16, 185, 129, 0.15);
            border-color: rgba(16, 185, 129, 0.4);
            color: #059669;
            transform: translateY(-1px);
            box-shadow: 0 2px 8px rgba(16, 185, 129, 0.2);
        }
    }

    // 危险按钮 - 浅色风格
    &.el-button--danger.is-plain {
        border-color: rgba(239, 68, 68, 0.3);
        color: #ef4444;
        background: rgba(239, 68, 68, 0.08);

        &:hover:not(:disabled) {
            background: rgba(239, 68, 68, 0.15);
            border-color: rgba(239, 68, 68, 0.4);
            color: #dc2626;
            transform: translateY(-1px);
            box-shadow: 0 2px 8px rgba(239, 68, 68, 0.2);
        }
    }

    // 主要按钮（非plain）- 浅色风格
    &.el-button--primary:not(.is-plain) {
        background: rgba(74, 144, 226, 0.2);
        border-color: rgba(74, 144, 226, 0.3);
        color: #4a90e2;

        &:hover:not(:disabled) {
            background: rgba(74, 144, 226, 0.3);
            border-color: rgba(74, 144, 226, 0.4);
            color: #3d7bc8;
            transform: translateY(-1px);
            box-shadow: 0 2px 8px rgba(74, 144, 226, 0.2);
        }
    }

    // 所有尺寸统一样式
    &.el-button--mini,
    &.el-button--small,
    &.el-button--medium {
        border-radius: 6px;
        font-weight: 500;
    }
}
</style>
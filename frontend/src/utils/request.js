import axios from 'axios'
import router from "../router";
import { getDeviceId } from './deviceId';
import { Message, MessageBox } from 'element-ui';

const request = axios.create({
    baseURL: '/api',
    timeout: 150000
})

// 添加错误状态标记和计时器存储
let errorFlags = {
    401: false, // 未授权
    403: false, // 禁止访问
    500: false, // 服务器错误
    408: false, // 超时
    'network': false // 网络错误
};

let errorTimers = {};


// 修改重置错误标记的函数
const resetErrorFlags = (specificError = null) => {
    if (specificError) {
        // 重置特定错误
        errorFlags[specificError] = false;
        if (errorTimers[specificError]) {
            clearTimeout(errorTimers[specificError]);
            delete errorTimers[specificError];
        }
    } else {
        // 重置所有错误
        Object.keys(errorFlags).forEach(key => {
            errorFlags[key] = false;
            if (errorTimers[key]) {
                clearTimeout(errorTimers[key]);
                delete errorTimers[key];
            }
        });
    }
};

// 设置错误标记的函数
const setErrorFlag = (status) => {
    if (errorFlags.hasOwnProperty(status)) {
        errorFlags[status] = true;
        
        // 清除之前的计时器（如果存在）
        if (errorTimers[status]) {
            clearTimeout(errorTimers[status]);
        }
        
        // 设置新的计时器，3秒后自动重置该错误状态
        errorTimers[status] = setTimeout(() => {
            resetErrorFlags(status);
        }, 3000);
    }
};

window.onerror = function(message, url, lineNumber) {
    // 静默处理未捕获的错误
};
  
request.interceptors.request.use(
    config => {
        // 检查是否有任何错误标记被设置
        const hasError = Object.values(errorFlags).some(flag => flag);
        if (hasError) {
            resetErrorFlags();
            // 使用 router 来处理重定向，而不是直接刷新页面
            router.push('/login');
            return Promise.reject('系统错误，请重新登录');
        }

        const user = localStorage.getItem('userInfo');
        if (user) {
            config.headers['token'] = JSON.parse(user).token;
        }
        
        const deviceId = getDeviceId();
        if (deviceId) {
            config.headers['X-Device-Id'] = deviceId;
        }
        
        return config;
    },
    error => {
        return Promise.reject(error);
    }
);

request.interceptors.response.use(
    response => {
        if (response.config.responseType === 'blob') {
            return response;
        }

        let res = response.data;
        if (typeof res === 'string') {
            res = JSON.parse(res);
        }
        
        if (res && res.deviceId) {
            const clientDeviceId = getDeviceId();
            if (clientDeviceId && res.deviceId === clientDeviceId) {
            } else {
                localStorage.removeItem('userInfo');
            }
        } else {
            localStorage.removeItem('userInfo');
        }
        
        return res;
    },
    error => {
        let status, data;
        
        if (error.response) {
            ({ status, data } = error.response);
            
            // 检查是否是已定义的错误状态码
            if (errorFlags.hasOwnProperty(status)) {
                if (!errorFlags[status]) {
                    setErrorFlag(status);
                    
                    // 清除用户信息（仅在401时）
                    if (status === 401) {
                        localStorage.removeItem('userInfo');
                        localStorage.removeItem('userMenuList');
                        localStorage.removeItem('deviceId');
                        localStorage.removeItem('token');
                        router.push('/login');
                    }
                    handleErrorResponse(status, data);
                }
                return Promise.reject(error);
            }
        } else {
            // 处理网络错误
            if (!errorFlags.network) {
                setErrorFlag('network');
                handleErrorResponse('network', error.message);
            }
        }
        return Promise.reject(error);
    }
);

function handleErrorResponse(status, data) {
    let message = '';
    let type = 'error';
    
    switch (status) {
        case 500:
            message = '服务器内部错误，请稍后再试！';
            type = 'error';
            break;
        case 403:
            message = '您没有权限访问该资源！联系原创作者QQ: 971118017';
            type = 'warning';
            break;
        case 408:
            message = '请求超时，请检查您的网络连接！';
            type = 'warning';
            break;
        case 401:
            message = '登录失效，请重新登录！';
            type = 'warning';
            router.push('/login');
            break;
        case 'network':
            message = '网络连接错误，请检查网络设置！';
            type = 'error';
            break;
        default:
            message = '请求发生错误，请稍后再试！';
            type = 'error';
            break;
    }
    
    if (status === 403) {
        MessageBox.prompt('请输入管理员密码二次验证', '权限验证', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            inputType: 'password',
            inputPlaceholder: '请输入管理员密码',
            customClass: 'admin-password-box',
            center: false,
            showCancelButton: true
        }).then(({ value }) => {
            MessageBox.alert('密码输入错误！'+message, '验证失败', {
                type: 'error',
                confirmButtonText: '确定',
                customClass: 'error-message-box',
                center: false
            });
        }).catch(() => {
        });
    }
}

// 重置方法
request.resetAuth = () => {
    resetErrorFlags();
    // 可以在这里添加其他需要重置的状态
};

export default request


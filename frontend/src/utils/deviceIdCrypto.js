const DEFAULT_DEVICE_ID = '93FE72006BDB11EE85170BD978A71700';
const AES_ALGORITHM = 'AES-CBC';
const KEY_LENGTH = 256;
const IV_LENGTH = 16;
const CACHE_EXPIRE_TIME = 3600000;

const deviceCache = new Map();
const deviceTimestamp = new Map();

function generateKeyFromString(input, keyLength) {
    try {
        const encoder = new TextEncoder();
        const data = encoder.encode(input);
        
        return crypto.subtle.digest('SHA-256', data).then(hash => {
            const hashArray = Array.from(new Uint8Array(hash));
            const key = new Uint8Array(keyLength);
            
            if (keyLength <= hashArray.length) {
                for (let i = 0; i < keyLength; i++) {
                    key[i] = hashArray[i];
                }
            } else {
                for (let i = 0; i < hashArray.length; i++) {
                    key[i] = hashArray[i];
                }
                for (let i = hashArray.length; i < keyLength; i++) {
                    key[i] = hashArray[i % hashArray.length];
                }
            }
            
            return key;
        });
    } catch (error) {
        console.error('生成密钥失败:', error);
        const encoder = new TextEncoder();
        const key = encoder.encode(input);
        return Promise.resolve(new Uint8Array(key.slice(0, keyLength)));
    }
}

export function generateDeviceId() {
    const uuid = 'xxxxxxxxxxxx4xxxyxxxxxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        const r = Math.random() * 16 | 0;
        const v = c === 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16).toUpperCase();
    });
    return uuid.replace(/-/g, '');
}

export function generateDeviceIdFromInfo(userAgent, ipAddress, screenInfo) {
    try {
        const combined = `${userAgent || ''}|${ipAddress || ''}|${screenInfo || ''}|${Date.now()}`;
        const encoder = new TextEncoder();
        const data = encoder.encode(combined);
        
        return crypto.subtle.digest('SHA-256', data).then(hash => {
            const hashArray = Array.from(new Uint8Array(hash));
            let deviceId = '';
            
            for (let i = 0; i < 16; i++) {
                deviceId += hashArray[i].toString(16).padStart(2, '0').toUpperCase();
            }
            
            return deviceId;
        }).catch(() => {
            return generateDeviceId();
        });
    } catch (error) {
        console.error('基于设备信息生成ID失败:', error);
        return Promise.resolve(generateDeviceId());
    }
}

async function calculateMD5(input) {
    const encoder = new TextEncoder();
    const data = encoder.encode(input);
    const hashBuffer = await crypto.subtle.digest('MD5', data);
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
}

async function calculateSHA256(input) {
    const encoder = new TextEncoder();
    const data = encoder.encode(input);
    const hashBuffer = await crypto.subtle.digest('SHA-256', data);
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
}

async function calculateChecksum(input) {
    try {
        const hash = await calculateMD5(input);
        return hash.substring(0, 8).toUpperCase();
    } catch (error) {
        console.error('计算校验码失败:', error);
        return '00000000';
    }
}

export async function encryptDeviceId(deviceId, secret = DEFAULT_DEVICE_ID) {
    if (!deviceId || deviceId.length === 0) {
        throw new Error('设备ID不能为空');
    }
    
    try {
        const cacheKey = `encrypt_${deviceId}`;
        if (deviceCache.has(cacheKey)) {
            const cached = deviceCache.get(cacheKey);
            const timestamp = deviceTimestamp.get(cacheKey);
            if (Date.now() - timestamp < CACHE_EXPIRE_TIME) {
                return cached;
            }
        }
        
        const keyData = await generateKeyFromString(secret, KEY_LENGTH / 8);
        const cryptoKey = await crypto.subtle.importKey(
            'raw',
            keyData,
            { name: AES_ALGORITHM },
            false,
            ['encrypt']
        );
        
        const ivArray = new Uint8Array(IV_LENGTH);
        const secretBytes = new TextEncoder().encode(secret);
        for (let i = 0; i < IV_LENGTH; i++) {
            ivArray[i] = secretBytes[i % secretBytes.length];
        }
        
        const encoder = new TextEncoder();
        const data = encoder.encode(deviceId);
        const encrypted = await crypto.subtle.encrypt(
            {
                name: AES_ALGORITHM,
                iv: ivArray
            },
            cryptoKey,
            data
        );
        
        const encryptedArray = Array.from(new Uint8Array(encrypted));
        const encryptedStr = btoa(String.fromCharCode.apply(null, encryptedArray));
        
        const timestamp = Date.now();
        const checksum = await calculateChecksum(encryptedStr + timestamp);
        const result = `${encryptedStr}|${timestamp}|${checksum}`;
        
        deviceCache.set(cacheKey, result);
        deviceTimestamp.set(cacheKey, timestamp);
        
        return result;
    } catch (error) {
        console.error('加密设备ID失败:', error);
        throw new Error('加密设备ID失败');
    }
}

export async function decryptDeviceId(encryptedDeviceId, secret = DEFAULT_DEVICE_ID) {
    if (!encryptedDeviceId || encryptedDeviceId.length === 0) {
        throw new Error('加密的设备ID不能为空');
    }
    
    try {
        const cacheKey = `decrypt_${encryptedDeviceId}`;
        if (deviceCache.has(cacheKey)) {
            return deviceCache.get(cacheKey);
        }
        
        const parts = encryptedDeviceId.split('|');
        if (parts.length !== 3) {
            throw new Error('加密的设备ID格式不正确');
        }
        
        const encryptedStr = parts[0];
        const timestamp = parseInt(parts[1], 10);
        const checksum = parts[2];
        
        const expectedChecksum = await calculateChecksum(encryptedStr + timestamp);
        if (checksum !== expectedChecksum) {
            throw new Error('设备ID校验失败');
        }
        
        const currentTime = Date.now();
        if (currentTime - timestamp > CACHE_EXPIRE_TIME * 24) {
            console.warn('设备ID已过期，时间戳:', timestamp);
        }
        
        const keyData = await generateKeyFromString(secret, KEY_LENGTH / 8);
        const cryptoKey = await crypto.subtle.importKey(
            'raw',
            keyData,
            { name: AES_ALGORITHM },
            false,
            ['decrypt']
        );
        
        const ivArray = new Uint8Array(IV_LENGTH);
        const secretBytes = new TextEncoder().encode(secret);
        for (let i = 0; i < IV_LENGTH; i++) {
            ivArray[i] = secretBytes[i % secretBytes.length];
        }
        
        const binaryString = atob(encryptedStr);
        const encrypted = new Uint8Array(binaryString.length);
        for (let i = 0; i < binaryString.length; i++) {
            encrypted[i] = binaryString.charCodeAt(i);
        }
        
        const decrypted = await crypto.subtle.decrypt(
            {
                name: AES_ALGORITHM,
                iv: ivArray
            },
            cryptoKey,
            encrypted
        );
        
        const decoder = new TextDecoder();
        const deviceId = decoder.decode(decrypted);
        
        deviceCache.set(cacheKey, deviceId);
        
        return deviceId;
    } catch (error) {
        console.error('解密设备ID失败:', error);
        throw new Error('解密设备ID失败');
    }
}

export function validateDeviceId(deviceId) {
    if (!deviceId || deviceId.length === 0) {
        return false;
    }
    
    if (deviceId.length !== 32) {
        return false;
    }
    
    const hexPattern = /^[0-9A-Fa-f]{32}$/;
    return hexPattern.test(deviceId);
}

export async function validateEncryptedDeviceId(encryptedDeviceId) {
    try {
        const parts = encryptedDeviceId.split('|');
        if (parts.length !== 3) {
            return false;
        }
        
        const timestamp = parseInt(parts[1], 10);
        const currentTime = Date.now();
        if (timestamp < 0 || timestamp > currentTime + 60000) {
            return false;
        }
        
        const expectedChecksum = await calculateChecksum(parts[0] + parts[1]);
        return expectedChecksum === parts[2];
    } catch (error) {
        console.error('验证加密设备ID失败:', error);
        return false;
    }
}

export async function generateDeviceFingerprint(userAgent, language, timezone, platform) {
    try {
        const combined = `${userAgent || ''}|${language || ''}|${timezone || ''}|${platform || ''}`;
        const hash = await calculateSHA256(combined);
        return hash;
    } catch (error) {
        console.error('生成设备指纹失败:', error);
        return generateDeviceId();
    }
}

export function obfuscateDeviceId(deviceId) {
    if (!deviceId || deviceId.length !== 32) {
        throw new Error('设备ID格式不正确');
    }
    
    let result = '';
    for (let i = 0; i < deviceId.length; i++) {
        result += deviceId.charAt(i);
        if ((i + 1) % 4 === 0 && i < deviceId.length - 1) {
            const randomChar = String.fromCharCode(65 + Math.floor(Math.random() * 26));
            result += randomChar;
        }
    }
    
    return result;
}

export function deobfuscateDeviceId(obfuscatedDeviceId) {
    if (!obfuscatedDeviceId || obfuscatedDeviceId.length < 32) {
        throw new Error('混淆的设备ID格式不正确');
    }
    
    let result = '';
    let charCount = 0;
    
    for (let i = 0; i < obfuscatedDeviceId.length; i++) {
        const c = obfuscatedDeviceId.charAt(i);
        if ((c >= '0' && c <= '9') || (c >= 'A' && c <= 'F')) {
            result += c;
            charCount++;
            if (charCount === 32) {
                break;
            }
        }
    }
    
    if (result.length !== 32) {
        throw new Error('无法正确反混淆设备ID');
    }
    
    return result;
}

export function encodeDeviceId(deviceId) {
    return btoa(unescape(encodeURIComponent(deviceId)));
}

export function decodeDeviceId(encodedDeviceId) {
    return decodeURIComponent(escape(atob(encodedDeviceId)));
}

export async function hashDeviceIdMD5(deviceId) {
    try {
        const hash = await calculateMD5(deviceId);
        return hash.toUpperCase();
    } catch (error) {
        console.error('MD5哈希计算失败:', error);
        return deviceId;
    }
}

export async function hashDeviceIdSHA256(deviceId) {
    try {
        const hash = await calculateSHA256(deviceId);
        return hash.toUpperCase();
    } catch (error) {
        console.error('SHA256哈希计算失败:', error);
        return deviceId;
    }
}

export function getDeviceInfo() {
    const screen = window.screen || {};
    const navigator = window.navigator || {};
    
    return {
        userAgent: navigator.userAgent || '',
        language: navigator.language || navigator.userLanguage || '',
        platform: navigator.platform || '',
        screenWidth: screen.width || 0,
        screenHeight: screen.height || 0,
        colorDepth: screen.colorDepth || 0,
        timezone: Intl.DateTimeFormat().resolvedOptions().timeZone || '',
        cookieEnabled: navigator.cookieEnabled || false,
        online: navigator.onLine || false
    };
}

export function clearExpiredCache() {
    const currentTime = Date.now();
    const keysToDelete = [];
    
    deviceTimestamp.forEach((timestamp, key) => {
        if (currentTime - timestamp > CACHE_EXPIRE_TIME) {
            keysToDelete.push(key);
        }
    });
    
    keysToDelete.forEach(key => {
        deviceCache.delete(key);
        deviceTimestamp.delete(key);
    });
    
    console.log(`已清除过期缓存，剩余缓存数量: ${deviceCache.size}`);
}

export function getCacheStats() {
    return {
        cacheSize: deviceCache.size,
        timestampSize: deviceTimestamp.size,
        cacheExpireTime: CACHE_EXPIRE_TIME
    };
}

export function startCacheCleanup(interval = 3600000) {
    setInterval(() => {
        clearExpiredCache();
    }, interval);
}

startCacheCleanup();



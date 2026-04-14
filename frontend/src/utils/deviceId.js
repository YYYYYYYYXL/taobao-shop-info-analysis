
export const DEVICE_ID = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX';

export function getDeviceId() {
    try {
        let deviceId = localStorage.getItem('deviceId');
        
        if (!deviceId) {
            deviceId = DEVICE_ID;
            localStorage.setItem('deviceId', deviceId);
        }
        
        return deviceId;
    } catch (error) {
        return DEVICE_ID;
    }
}

export function getFullDeviceId() {
    try {
        return localStorage.getItem('deviceId') || DEVICE_ID;
    } catch (error) {
        return DEVICE_ID;
    }
}

export function setDeviceId(id) {
    try {
        localStorage.setItem('deviceId', id);
    } catch (error) {
    }
}

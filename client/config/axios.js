import axios from 'axios'

// Create axios client, pre-configured with baseURL
let api = axios.create({
    baseURL: 'http://192.168.0.162:5000',
    timeout: 10000,
});

// Set JSON Web Token in Client to be included in all calls
export const setClientToken = token => {
    api.interceptors.request.use(function(config) {
        config.headers.Authorization = `Bearer ${token}`;
        return config;
    });
};

export default api;

import axios from 'axios'


/**
 * Backend Connection configuration
 * Replace the below baseUrl with your local IP to connect to local backend server
 **/
let api = axios.create({
    //baseURL: 'http://ec2-user@ec2-3-25-170-12.ap-southeast-2.compute.amazonaws.com:5000',
    baseURL:'http://192.168.1.106:5000',
    timeout: 10000,
});

// Set JSON Web Token in Client to be included in all calls
export const setClientToken = token => {
    api.interceptors.request.use(function(config) {
        config.headers.Authorization = token;
        return config;
    });
};

export default api;

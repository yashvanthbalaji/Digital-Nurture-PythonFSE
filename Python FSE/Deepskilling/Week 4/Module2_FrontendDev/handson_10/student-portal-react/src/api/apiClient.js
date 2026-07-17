import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'https://jsonplaceholder.typicode.com',
  timeout: 5000,
  headers: {
    'Content-Type': 'application/json'
  }
});

// request interceptor: attaches an auth header to EVERY request automatically
apiClient.interceptors.request.use((config) => {
  config.headers.Authorization = 'Bearer mock-token-12345';
  return config;
});

// response interceptor:
// (a) unwraps response.data so callers get plain data, not the axios wrapper
// (b) turns any error into one standard shape with a message + statusCode
apiClient.interceptors.response.use(
  (response) => response.data,
  (error) => {
    const standardError = new Error(
      error.response ? 'Request failed with status ' + error.response.status : 'Network error'
    );
    standardError.statusCode = error.response ? error.response.status : null;
    return Promise.reject(standardError);
  }
);

export default apiClient;
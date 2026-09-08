import axios from "axios";
import {
  API_BASE_URL,
  TOKEN_KEY
} from "../utils/constants";

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json"
  },
  timeout: 10000
});

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem(TOKEN_KEY);

    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    return config;
  },
  (error) => Promise.reject(error)
);

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem(TOKEN_KEY);
      localStorage.removeItem("devops_monitoring_user");
    }

    return Promise.reject(error);
  }
);

export const authApi = {
  login: async (username, password) => {
    const formData = new URLSearchParams();

    formData.append("username", username);
    formData.append("password", password);

    const response = await api.post(
      "/auth/login",
      formData,
      {
        headers: {
          "Content-Type":
            "application/x-www-form-urlencoded"
        }
      }
    );

    return response.data;
  },

  register: async (data) => {
    const response = await api.post(
      "/auth/register",
      data
    );

    return response.data;
  },

  me: async () => {
    const response = await api.get(
      "/auth/me"
    );

    return response.data;
  }
};

export const serversApi = {
  list: async () => {
    const response = await api.get(
      "/servers"
    );

    return response.data;
  },

  get: async (id) => {
    const response = await api.get(
      `/servers/${id}`
    );

    return response.data;
  },

  create: async (data) => {
    const response = await api.post(
      "/servers",
      data
    );

    return response.data;
  },

  update: async (id, data) => {
    const response = await api.put(
      `/servers/${id}`,
      data
    );

    return response.data;
  },

  remove: async (id) => {
    const response = await api.delete(
      `/servers/${id}`
    );

    return response.data;
  }
};

export const metricsApi = {
  list: async (params = {}) => {
    const response = await api.get(
      "/metrics",
      { params }
    );

    return response.data;
  },

  create: async (data) => {
    const response = await api.post(
      "/metrics",
      data
    );

    return response.data;
  }
};

export const alertsApi = {
  list: async (params = {}) => {
    const response = await api.get(
      "/alerts",
      { params }
    );

    return response.data;
  },

  create: async (data) => {
    const response = await api.post(
      "/alerts",
      data
    );

    return response.data;
  },

  update: async (id, data) => {
    const response = await api.patch(
      `/alerts/${id}`,
      data
    );

    return response.data;
  }
};

export const incidentsApi = {
  list: async (params = {}) => {
    const response = await api.get(
      "/incidents",
      { params }
    );

    return response.data;
  },

  get: async (id) => {
    const response = await api.get(
      `/incidents/${id}`
    );

    return response.data;
  },

  create: async (data) => {
    const response = await api.post(
      "/incidents",
      data
    );

    return response.data;
  },

  update: async (id, data) => {
    const response = await api.patch(
      `/incidents/${id}`,
      data
    );

    return response.data;
  },
};

export const applicationsApi = {
  list: async () => {
    const response = await api.get(
      "/applications"
    );

    return response.data;
  },

  create: async (data) => {
    const response = await api.post(
      "/applications",
      data
    );

    return response.data;
  }
};

export const logsApi = {
  list: async (params = {}) => {
    const response = await api.get(
      "/logs",
      { params }
    );

    return response.data;
  },

  create: async (data) => {
    const response = await api.post(
      "/logs",
      data
    );

    return response.data;
  }
};
export default api;


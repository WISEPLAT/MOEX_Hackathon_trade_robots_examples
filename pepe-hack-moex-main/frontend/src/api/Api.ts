const baseUrl = "http://127.0.0.1:8000/";

const {fetch: originalFetch} = window;

window.fetch = async (...args) => {
    const [resource, config] = args;
    const response = await originalFetch(resource, config);
    if (response.status === 401 && resource !== `${baseUrl}auth/refresh_token`) {
        const accessToken = await authAPI.putRefreshToken();
        return await originalFetch(resource, {
            ...config,
            headers: {
                "Access-Token": accessToken,
            },
        });
    }
    return response;
};

export const authAPI = {
    async postAuthLogin(
        data: any,
        checkResponse?: (response: Response) => void,
    ) {
        return await fetch(`${baseUrl}auth/login`, {
            method: "POST",
            headers: {"Content-Type": "application/json; charset=utf-8"},
            credentials: "include",
            body: JSON.stringify(data),
        })
            .then((response) => {
                if (checkResponse) {
                    checkResponse(response);
                }
                return response.json();
            })
            .then((data) => {
                window.localStorage.setItem("access_token", data.access_token);
            });
    },
    async deleteAuthLogin() {
        return await fetch(`${baseUrl}auth/logout`, {
            method: "DELETE",
            headers: {
                "Access-Token": window.localStorage.getItem("access_token") || "",
            },
        })
            .then((response) => response.json())
            .then((data) => {
                window.localStorage.setItem("access_token", data.access_token);
            })
            .catch((error) => console.error(error));
    },
    async postAuthRegister(data: any) {
        return await fetch(`${baseUrl}auth/registration`, {
            method: "POST",
            headers: {"Content-Type": "application/json; charset=utf-8"},
            body: JSON.stringify(data),
        })
            .then((response) => response.json())
            .catch((error) => console.error(error));
    },
    async putRefreshToken() {
        return await fetch(`${baseUrl}auth/refresh_token`, {
            method: "PUT",
            credentials: "include",
        })
            .then((response) => response.json())
            .then((data) => {
                window.localStorage.setItem("access_token", data.access_token);
                return data.access_token;
            })
            .catch((error) => console.error(error));
    },
    getAuthMe: async (checkResponse?: (response: Response) => void) => {
        return await fetch(`${baseUrl}auth/isAuth`, {
            method: "GET",
            headers: {
                "Access-Token": window.localStorage.getItem("access_token") || "",
            },
        })
            .then((response) => {
                if (checkResponse) {
                    checkResponse(response);
                }
                return response.json();
            })
            .catch((error) => console.error(error));
    },
};

export const mainApi = {
    async getStocksCatalog({searchValue, pageSize, page}: any) {
        return await fetch(`${baseUrl}stocks-catalog/?limit=${pageSize}&page=${page}&search_value=${searchValue || ''}`, {
            method: "GET",
            headers: {
                "Access-Token": window.localStorage.getItem("access_token") || "",
            },
        })
            .then((response) => response.json())
            .catch((error) => console.error(error));
    },
    async getStocks(typeStocks: number) {
        return await fetch(`${baseUrl}stocks/${typeStocks}`, {
            method: "GET",
            headers: {
                "Access-Token": window.localStorage.getItem("access_token") || "",
            },
        })
            .then((response) => response.json())
            .catch((error) => console.error(error));
    },
    async getStock(id: number) {
        return await fetch(`${baseUrl}stock/${id}`, {
            method: "GET",
            headers: {
                "Access-Token": window.localStorage.getItem("access_token") || "",
            },
        })
            .then((response) => response.json())
            .catch((error) => console.error(error));
    },
    async getChartStock(id: number, dateRange: any) {
        const startDate = dateRange[0] || '2023-02-01';
        const endDate = dateRange[1] || '2024-01-01';
        return await fetch(`${baseUrl}stockchart/${id}?date_from=${startDate}&date_to=${endDate}`, {
            method: "GET",
            headers: {
                "Access-Token": window.localStorage.getItem("access_token") || "",
            },
        })
            .then((response) => response.json())
            .catch((error) => console.error(error));
    },
};


export const botApi = {
    async startBot({date_to, risk_level}: any) {
        return await fetch(`${baseUrl}bot/start?` + new URLSearchParams({date_to, risk_level, user_id: '0'}), {
            method: "POST",
            headers: {
                "Access-Token": window.localStorage.getItem("access_token") || "",
            },
        })
            .then((response) => response.json())
            .catch((error) => console.error(error));
    },
    async stopBot() {
        return await fetch(`${baseUrl}bot/stop?` + new URLSearchParams({user_id: '0'}), {
            method: "POST",
            headers: {
                "Access-Token": window.localStorage.getItem("access_token") || "",
            },
        })
            .then((response) => response.json())
            .catch((error) => console.error(error));
    },
    async getBotInfo() {
        return await fetch(`${baseUrl}bot/?` + new URLSearchParams({user_id: '0'}), {
            method: "GET",
            headers: {
                "Access-Token": window.localStorage.getItem("access_token") || "",
            },
        })
            .then((response) => response.json())
            .catch((error) => console.error(error));
    },
    async getBotHistory() {
        return await fetch(`${baseUrl}bot/history?` + new URLSearchParams({user_id: '0'}), {
            method: "GET",
            headers: {
                "Access-Token": window.localStorage.getItem("access_token") || "",
            },
        })
            .then((response) => response.json())
            .catch((error) => console.error(error));
    },
};

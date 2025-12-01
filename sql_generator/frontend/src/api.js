import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

export const generateSQL = async (query) => {
    try {
        const response = await axios.post(`${API_URL}/generate_sql`, { query });
        return response.data.sql;
    } catch (error) {
        console.error("Error generating SQL:", error);
        throw error;
    }
};

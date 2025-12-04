import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

export const generateSQL = async (query, history = []) => {
    try {
        const response = await axios.post(`${API_URL}/generate_sql`, { query, history });
        return response.data.sql;
    } catch (error) {
        console.error("Error generating SQL:", error);
        throw error;
    }
};

export const executeSQL = async (sql) => {
    try {
        const response = await axios.post(`${API_URL}/execute_sql`, { sql });
        return response.data;
    } catch (error) {
        console.error('Error executing SQL:', error);
        throw error;
    }
};

export const sendFeedback = async (query, sql, rating) => {
    try {
        await axios.post(`${API_URL}/feedback`, { query, sql, rating });
    } catch (error) {
        console.error("Error sending feedback:", error);
    }
};

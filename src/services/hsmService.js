import { API_BASE_URL } from '../config/api';

export const checkHSMHealth = async () => {
  const response = await fetch(`${API_BASE_URL}/hsm/health`);
  if (!response.ok) {
    throw new Error('Failed to check HSM health');
  }
  return response.json();
};

export const configureHSM = async (ipAddress, certificateFile) => {
  const formData = new FormData();
  formData.append('ip_address', ipAddress);
  formData.append('certificate', certificateFile);

  const response = await fetch(`${API_BASE_URL}/hsm/configure`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    throw new Error('Failed to configure HSM');
  }
  
  return response.json();
};

export const testHSMConnection = async () => {
  const response = await fetch(`${API_BASE_URL}/hsm/test-connection`, {
    method: 'POST',
  });

  if (!response.ok) {
    throw new Error('Failed to test HSM connection');
  }
  
  return response.json();
};